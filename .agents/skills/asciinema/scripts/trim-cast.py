#!/usr/bin/env python3
"""
trim-cast.py: Inspect timing and strip trailing exit sequences from asciicast (.cast) recordings.

Capabilities:
1. Inspect timing: Computes raw duration, playback duration (accounting for idle_time_limit),
   and event breakdown across asciicast v2 and v3 formats.
2. Strip trailing exit sequences: Detects and cuts Ctrl+D sequences, "press ctrl+d again to exit"
   warnings, shell drop-backs, and trailing subshell exits.
3. Holds final frame: Appends a clean exit code event ('x') with a configurable trailing hold
   (default: 3.0s), preventing abrupt video/animation cutoffs or instant replay loops.
4. Preserves formatting: Keeps unmodified recording lines byte-for-byte identical.
"""

import argparse
import json
import os
import re
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Inspect asciicast duration and strip trailing Ctrl+D / exit sequences."
    )
    parser.add_argument("input", help="Path to input .cast file")
    parser.add_argument(
        "output",
        nargs="?",
        default=None,
        help="Path to output .cast file (omit if only inspecting or using --in-place)",
    )
    parser.add_argument(
        "-i",
        "--in-place",
        action="store_true",
        help="Modify the input file in place",
    )
    parser.add_argument(
        "--info",
        action="store_true",
        help="Only display duration and timing information without modifying file",
    )
    parser.add_argument(
        "--hold",
        type=float,
        default=3.0,
        help="Duration (seconds) to hold final frame before process exit (default: 3.0)",
    )
    parser.add_argument(
        "--idle-limit",
        type=float,
        default=None,
        help="Override idle_time_limit from cast header for playback duration calculation",
    )
    parser.add_argument(
        "--cut-at",
        type=str,
        default=None,
        help="Explicit substring in stdout ('o') data to trigger cutting (cut includes this event and all following)",
    )
    parser.add_argument(
        "--cut-regex",
        type=str,
        default=None,
        help="Regex pattern in stdout ('o') data to trigger cutting",
    )
    parser.add_argument(
        "--cut-index",
        type=int,
        default=None,
        help="Explicit 0-based event index to cut at (cuts this event and all following)",
    )
    return parser.parse_args()


# Common terminal exit prompts / warnings to match automatically
DEFAULT_EXIT_PATTERNS = [
    re.compile(r"press ctrl\+d again to exit", re.IGNORECASE),
    re.compile(r"Resume with -c \(or command below\):", re.IGNORECASE),
    re.compile(r"\bexit\r?\n", re.IGNORECASE),
]


def format_duration(seconds):
    seconds = max(0.0, seconds)
    mins = int(seconds // 60)
    rem_secs = seconds % 60
    if mins > 0:
        return f"{mins}m {rem_secs:04.1f}s ({seconds:.2f}s)"
    return f"{seconds:.2f}s"


class CastEvent:
    def __init__(self, parsed, raw_line):
        self.parsed = parsed  # list [time, type, data] or None
        self.raw_line = raw_line

    @property
    def is_event(self):
        return isinstance(self.parsed, list) and len(self.parsed) >= 2


def load_cast(file_path):
    if not os.path.exists(file_path):
        sys.stderr.write(f"Error: File not found: {file_path}\n")
        sys.exit(1)

    events = []
    header = None
    header_raw = None
    with open(file_path, "r", encoding="utf-8") as f:
        first_line = f.readline()
        if not first_line:
            sys.stderr.write("Error: Input file is empty.\n")
            sys.exit(1)

        try:
            header = json.loads(first_line)
            header_raw = first_line
        except json.JSONDecodeError as err:
            sys.stderr.write(f"Error: Invalid header JSON: {err}\n")
            sys.exit(1)

        for line in f:
            trimmed = line.strip()
            if not trimmed:
                continue
            if trimmed.startswith("#"):
                events.append(CastEvent(None, line))
                continue
            try:
                ev = json.loads(trimmed)
                events.append(CastEvent(ev, line))
            except json.JSONDecodeError:
                events.append(CastEvent(None, line))

    return header, header_raw, events


def calculate_durations(header, events, idle_limit_override=None):
    version = header.get("version", 2)
    idle_limit = idle_limit_override
    if idle_limit is None:
        idle_limit = header.get("idle_time_limit")

    event_counts = {"o": 0, "i": 0, "m": 0, "r": 0, "x": 0, "other": 0}

    raw_duration = 0.0
    capped_duration = 0.0

    if version == 3:
        for ev in events:
            if not ev.is_event:
                continue
            ev_type = ev.parsed[1]
            event_counts[ev_type if ev_type in event_counts else "other"] += 1
            dt = float(ev.parsed[0])
            raw_duration += dt
            capped_duration += min(dt, idle_limit) if (idle_limit is not None and idle_limit > 0) else dt
    else:  # version 2 (absolute timestamps)
        prev_time = 0.0
        for ev in events:
            if not ev.is_event:
                continue
            ev_type = ev.parsed[1]
            event_counts[ev_type if ev_type in event_counts else "other"] += 1
            curr_time = float(ev.parsed[0])
            dt = max(0.0, curr_time - prev_time)
            raw_duration = curr_time
            capped_duration += min(dt, idle_limit) if (idle_limit is not None and idle_limit > 0) else dt
            prev_time = curr_time

    return {
        "version": version,
        "raw_duration": raw_duration,
        "capped_duration": capped_duration,
        "idle_limit": idle_limit,
        "event_counts": event_counts,
        "total_events": sum(event_counts.values()),
    }


def find_cut_index(events, cut_at=None, cut_regex=None, cut_index=None):
    if cut_index is not None:
        if 0 <= cut_index < len(events):
            return cut_index
        sys.stderr.write(f"Error: Specified --cut-index {cut_index} is out of bounds (0..{len(events)-1})\n")
        sys.exit(1)

    custom_re = re.compile(cut_regex) if cut_regex else None

    for idx, ev in enumerate(events):
        if not ev.is_event or len(ev.parsed) < 3:
            continue
        ev_type, ev_data = ev.parsed[1], ev.parsed[2]
        if ev_type != "o" or not isinstance(ev_data, str):
            continue

        if cut_at and cut_at in ev_data:
            return idx

        if custom_re and custom_re.search(ev_data):
            return idx

        if not cut_at and not cut_regex:
            for pattern in DEFAULT_EXIT_PATTERNS:
                if pattern.search(ev_data):
                    return idx

    return None


def print_info(title, stats):
    print(f"\n{title}")
    print("=" * len(title))
    print(f"Format Version:       asciicast v{stats['version']}")
    print(f"Total Events:         {stats['total_events']} (stdout: {stats['event_counts']['o']}, stdin: {stats['event_counts']['i']}, markers: {stats['event_counts']['m']}, exit: {stats['event_counts']['x']})")
    print(f"Raw Duration:         {format_duration(stats['raw_duration'])}")
    if stats["idle_limit"]:
        print(f"Playback Duration:    {format_duration(stats['capped_duration'])} (capped at {stats['idle_limit']:.1f}s idle limit)")
    else:
        print(f"Playback Duration:    {format_duration(stats['capped_duration'])} (no idle_time_limit)")


def write_cast(file_path, header_line, events):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(header_line if header_line.endswith("\n") else header_line + "\n")
        for ev in events:
            f.write(ev.raw_line if ev.raw_line.endswith("\n") else ev.raw_line + "\n")


def main():
    args = parse_args()
    header, header_raw, events = load_cast(args.input)

    orig_stats = calculate_durations(header, events, args.idle_limit)

    if args.info or (args.output is None and not args.in_place):
        print_info(f"Asciicast Timing Analysis: {args.input}", orig_stats)
        auto_cut = find_cut_index(events, args.cut_at, args.cut_regex, args.cut_index)
        if auto_cut is not None:
            ev = events[auto_cut]
            sample = repr(ev.parsed[2][:60]) if (ev.is_event and len(ev.parsed) > 2) else ""
            print(f"\nDetected Trailing Exit Sequence at event #{auto_cut}:")
            print(f"  Payload sample: {sample}")
            trimmed = events[:auto_cut]
            trimmed_stats = calculate_durations(header, trimmed, args.idle_limit)
            saved_raw = orig_stats["raw_duration"] - trimmed_stats["raw_duration"]
            print(f"  Duration if trimmed (+{args.hold:.1f}s hold): {format_duration(trimmed_stats['raw_duration'] + args.hold)}")
            print(f"  Time savable: ~{saved_raw:.2f}s")
            print("\nTo strip this sequence, run with --in-place or provide an output path:")
            print(f"  python3 .agents/skills/asciinema/scripts/trim-cast.py {args.input} --in-place")
        else:
            print("\nNo trailing exit sequence pattern detected automatically.")
        return

    # Trim operation
    cut_idx = find_cut_index(events, args.cut_at, args.cut_regex, args.cut_index)
    if cut_idx is None:
        sys.stderr.write("No matching exit sequence found to trim. No changes made.\n")
        sys.exit(1)

    kept_events = list(events[:cut_idx])
    version = orig_stats["version"]

    # Append clean exit event
    if version == 3:
        exit_ev = [round(args.hold, 3), "x", "0"]
        exit_line = json.dumps(exit_ev) + "\n"
        kept_events.append(CastEvent(exit_ev, exit_line))
        header_line = header_raw
    else:
        last_time = 0.0
        for ev in reversed(kept_events):
            if ev.is_event and len(ev.parsed) >= 1:
                last_time = float(ev.parsed[0])
                break
        total_time = round(last_time + args.hold, 3)
        exit_ev = [total_time, "x", "0"]
        exit_line = json.dumps(exit_ev) + "\n"
        kept_events.append(CastEvent(exit_ev, exit_line))
        if "duration" in header:
            header["duration"] = total_time
            header_line = json.dumps(header, ensure_ascii=False) + "\n"
        else:
            header_line = header_raw

    out_path = args.input if args.in_place else args.output
    write_cast(out_path, header_line, kept_events)

    new_stats = calculate_durations(header, kept_events, args.idle_limit)
    print_info(f"Original: {args.input}", orig_stats)
    print_info(f"Trimmed: {out_path}", new_stats)

    saved_raw = orig_stats["raw_duration"] - new_stats["raw_duration"]
    saved_capped = orig_stats["capped_duration"] - new_stats["capped_duration"]
    print("\nSummary:")
    print(f"  Stripped events:       {orig_stats['total_events'] - new_stats['total_events']} trailing events")
    print(f"  Held final frame:      {args.hold:.1f}s")
    print(f"  Net raw time saved:    {saved_raw:.2f}s")
    if orig_stats["idle_limit"]:
        print(f"  Net playback time saved: {saved_capped:.2f}s")


if __name__ == "__main__":
    main()
