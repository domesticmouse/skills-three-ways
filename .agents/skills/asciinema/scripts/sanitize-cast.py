#!/usr/bin/env python3
"""
sanitize-cast.py: Sanitize and redact asciicast (.cast) recording files.

Removes sensitive data risks:
1. Strips stdin ('i') keystroke events (removes captured passwords and secrets).
2. Cleans sensitive environment variables from the header (line 1), preserving only safe keys.
3. Redacts specified patterns or tokens from terminal stdout ('o') output streams.
"""

import argparse
import json
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sanitize asciinema .cast files by stripping stdin events and redacting secrets."
    )
    parser.add_argument("input", help="Path to raw input .cast file")
    parser.add_argument("output", help="Path to write sanitized .cast file")
    parser.add_argument(
        "--redact",
        nargs="*",
        default=[],
        help="Pairs of target=replacement strings to redact (e.g. 'secret_key=REDACTED')",
    )
    parser.add_argument(
        "--redact-file",
        help="Path to a text file containing strings to redact (one per line, replaced with [REDACTED])",
    )
    parser.add_argument(
        "--keep-stdin",
        action="store_true",
        help="Do not strip stdin ('i') events (NOT recommended if passwords were typed)",
    )
    parser.add_argument(
        "--keep-env",
        action="store_true",
        help="Preserve all environment variables in the header without scrubbing",
    )
    return parser.parse_args()


def load_redact_patterns(cli_patterns, file_path):
    patterns = {}
    for item in cli_patterns:
        if "=" in item:
            key, val = item.split("=", 1)
            patterns[key] = val
        else:
            patterns[item] = "[REDACTED]"

    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                target = line.strip()
                if target and not target.startswith("#"):
                    if "=" in target:
                        k, v = target.split("=", 1)
                        patterns[k] = v
                    else:
                        patterns[target] = "[REDACTED]"
    return patterns


def sanitize(input_path, output_path, redact_map, strip_stdin=True, scrub_env=True):
    stripped_stdin_count = 0
    redacted_occurrences = 0

    with open(input_path, "r", encoding="utf-8") as infile, open(
        output_path, "w", encoding="utf-8"
    ) as outfile:
        # 1. Process header line
        first_line = infile.readline()
        if not first_line:
            sys.stderr.write("Error: Input file is empty.\n")
            sys.exit(1)

        try:
            header = json.loads(first_line)
        except json.JSONDecodeError as err:
            sys.stderr.write(f"Error: Could not parse header JSON: {err}\n")
            sys.exit(1)

        if scrub_env and "env" in header and isinstance(header["env"], dict):
            safe_env_keys = {"TERM", "SHELL"}
            header["env"] = {k: v for k, v in header["env"].items() if k in safe_env_keys}

        outfile.write(json.dumps(header) + "\n")

        # 2. Process event stream
        for line_num, line in enumerate(infile, start=2):
            trimmed = line.strip()
            if not trimmed:
                continue

            # Pass comments through cleanly (v3)
            if trimmed.startswith("#"):
                outfile.write(line)
                continue

            try:
                event = json.loads(trimmed)
            except json.JSONDecodeError:
                # If a line cannot be parsed, pass it through
                outfile.write(line)
                continue

            if not isinstance(event, list) or len(event) < 3:
                outfile.write(line)
                continue

            event_time, event_type, event_data = event[0], event[1], event[2]

            # Strip stdin keystroke events
            if strip_stdin and event_type == "i":
                stripped_stdin_count += 1
                continue

            # Redact patterns in stdout data
            if event_type == "o" and isinstance(event_data, str) and redact_map:
                for target, replacement in redact_map.items():
                    if target in event_data:
                        count = event_data.count(target)
                        redacted_occurrences += count
                        event_data = event_data.replace(target, replacement)
                event[2] = event_data

            outfile.write(json.dumps(event) + "\n")

    print(
        f"Sanitization complete: {output_path}\n"
        f"  - Stdin ('i') events stripped: {stripped_stdin_count}\n"
        f"  - Secret pattern replacements: {redacted_occurrences}"
    )


def main():
    args = parse_args()
    redact_map = load_redact_patterns(args.redact, args.redact_file)
    sanitize(
        args.input,
        args.output,
        redact_map,
        strip_stdin=not args.keep_stdin,
        scrub_env=not args.keep_env,
    )


if __name__ == "__main__":
    main()
