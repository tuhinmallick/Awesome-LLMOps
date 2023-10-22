#!/usr/bin/env python3

import sys
import shutil

filename = "README.md"
filename_backup = "README.md.backup"


def is_link_line(line) -> bool:
    """Return true if the line is a link line."""
    return len(line) >= 3 and line[:3] == "- ["

def is_github_project(line) -> bool:
    return "https://github.com" in line

def contains_star_badge(line) -> bool:
    return "https://img.shields.io/github/stars" in line


def generate_badge_link(line) -> str:
    first_right_middle_bracket = line.find("]")
    # The text should be `](https://github.com/<>/<>)`
    right_bracket = line[first_right_middle_bracket:].find(")") + first_right_middle_bracket
    project = line[first_right_middle_bracket+2+19:right_bracket]
    print(f"The project handle of this line is {project}")
    badge_link = (
        f" ![](https://img.shields.io/github/stars/{project}.svg?style=social)"
    )
    if line[right_bracket+1] != " ":
        badge_link += " "
    newline = line[:right_bracket+1] + badge_link + line[right_bracket+1:]
    print(f"The new line is {newline}")
    return newline


def generate_star_badge(line) -> str:
    """Add the GitHub star badge if it does not exist."""
    if not is_link_line(line) or not is_github_project(line):
        "Return other lines unchanged."
        return line
    if contains_star_badge(line):
        return line
    print(f"This line does not contain the star badge: {line}")
    return generate_badge_link(line)


def main() -> int:
    """Echo the input arguments to standard output"""
    lines = []
    with open(filename, "r") as f:
        lines.extend(generate_star_badge(line) for line in f)
    shutil.copyfile(filename, filename_backup)
    with open(filename, "w") as f:
        for line in lines:
            f.write(line)
    return 0


if __name__ == '__main__':
    sys.exit(main())  # next section explains the use of sys.exit
