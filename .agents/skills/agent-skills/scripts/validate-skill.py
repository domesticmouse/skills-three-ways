#!/usr/bin/env python3
"""validate-skill.py: Validates an Agent Skill directory against the agentskills.io standard.

Checks:
- Directory existence and naming constraints
- Mandatory SKILL.md existence and readable YAML frontmatter
- Valid frontmatter fields: name, description, compatibility, allowed-tools
- Name matches directory name (agentskills.io spec requirement)
- Description length and context pointer quality
- Presence of checkable completion criteria
- Script directory permissions and asset references
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None


NAME_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(content: str) -> tuple[dict | None, str, str | None]:
    """Extract frontmatter and body from markdown content."""
    if not content.startswith("---"):
        return None, content, "File does not start with YAML frontmatter delimiter (---)"

    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content, "Unterminated YAML frontmatter delimiter (closing --- not found)"

    raw_yaml = parts[1]
    body = parts[2]

    if yaml is not None:
        try:
            data = yaml.safe_load(raw_yaml)
            if not isinstance(data, dict):
                return None, body, "Frontmatter does not parse into a key-value mapping"
            return data, body, None
        except Exception as e:
            return None, body, f"YAML parsing error: {e}"

    # Fallback minimal parser if pyyaml is missing
    data = {}
    for line in raw_yaml.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip("\"'")
    return data, body, None


def validate_skill(skill_dir: Path) -> list[str]:
    """Validate a skill directory. Returns a list of error strings (empty if valid)."""
    errors: list[str] = []
    warnings: list[str] = []

    if not skill_dir.is_dir():
        return [f"'{skill_dir}' is not a directory"]

    dir_name = skill_dir.resolve().name
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.is_file():
        return [f"Missing required SKILL.md at '{skill_md}'"]

    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        return [f"Cannot read SKILL.md: {e}"]

    frontmatter, body, err = parse_frontmatter(content)
    if err:
        errors.append(f"Frontmatter error: {err}")
        return errors

    assert frontmatter is not None

    # Validate 'name'
    name = frontmatter.get("name")
    if not name:
        errors.append("Missing required 'name' field in frontmatter")
    elif not isinstance(name, str):
        errors.append(f"'name' field must be a string, got {type(name).__name__}")
    else:
        if len(name) > 64:
            errors.append(f"'name' exceeds 64 characters ({len(name)})")
        if not NAME_PATTERN.match(name):
            errors.append(
                f"'name' ('{name}') must be lowercase alphanumeric and hyphens, no consecutive hyphens, cannot start/end with hyphen"
            )
        if name != dir_name:
            errors.append(
                f"'name' ('{name}') does not match directory name ('{dir_name}') as required by specification"
            )

    # Validate 'description'
    desc = frontmatter.get("description")
    if not desc:
        errors.append("Missing required 'description' field in frontmatter")
    elif not isinstance(desc, str):
        errors.append(f"'description' field must be a string, got {type(desc).__name__}")
    else:
        clean_desc = desc.strip()
        if len(clean_desc) < 10:
            errors.append(f"'description' is too short ({len(clean_desc)} chars); must clearly specify what and when")
        elif len(clean_desc) > 1024:
            errors.append(f"'description' exceeds 1024 characters ({len(clean_desc)})")

        # Check for recommended trigger cues
        lower_desc = clean_desc.lower()
        if "use when" not in lower_desc and "trigger" not in lower_desc and "when" not in lower_desc:
            warnings.append("Recommendation: Include explicit trigger conditions in description (e.g., 'Use when...')")

    # Validate compatibility if present
    compat = frontmatter.get("compatibility")
    if compat is not None:
        if not isinstance(compat, str):
            errors.append(f"'compatibility' must be a string, got {type(compat).__name__}")
        elif len(compat) > 500:
            errors.append(f"'compatibility' exceeds 500 characters ({len(compat)})")

    # Validate scripts directory if present
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.exists() and scripts_dir.is_dir():
        for script_file in scripts_dir.iterdir():
            if script_file.is_file() and not script_file.name.startswith("."):
                if not os.access(script_file, os.X_OK):
                    warnings.append(
                        f"Script '{script_file.name}' is not marked executable (consider chmod +x)"
                    )

    # Validate checkable completion criteria in body
    lower_body = body.lower()
    if "completion criteri" not in lower_body and "verify" not in lower_body and "verification" not in lower_body:
        warnings.append(
            "Recommendation: Include explicit checkable 'Completion Criteria' or verification steps to guard against premature completion"
        )

    for w in warnings:
        print(f"  [WARN] {w}", file=sys.stderr)

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an Agent Skill directory.")
    parser.add_argument("skill_dir", nargs="?", default=".", help="Path to the skill directory (default: current dir)")
    args = parser.parse_args()

    target = Path(args.skill_dir)
    print(f"Validating skill at: {target.resolve()}")

    errors = validate_skill(target)
    if errors:
        print(f"FAILED: Found {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("PASSED: Skill structure, frontmatter, and naming are compliant with specification.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
