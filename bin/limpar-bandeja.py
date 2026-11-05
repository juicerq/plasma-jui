#!/usr/bin/env python3
import os
import re
import sys

CONFIG = os.path.expanduser("~/.config/plasma-org.kde.plasma.desktop-appletsrc")

HIDDEN = [
    "org.kde.plasma.brightness",
    "org.kde.kscreen",
    "org.kde.plasma.mediacontroller",
    "org.kde.plasma.clipboard",
    "org.kde.plasma.cameraindicator",
    "org.kde.plasma.devicenotifier",
    "org.kde.plasma.keyboardlayout",
    "org.kde.plasma.manage-inputmethod",
    "org.kde.kdeconnect",
    "org.kde.plasma.keyboardindicator",
    "org.kde.plasma.weather",
    "org.kde.plasma.bluetooth",
    "org.kde.plasma.networkmanagement",
    "plasmashell_microphone",
]

VOL = "dev.juicerq.vol"


def systray_sections(lines):
    section = None
    found = {}

    for index, line in enumerate(lines):
        header = re.match(r"^\[(.+)\]$", line)

        if header:
            section = header.group(1)
            continue

        if line.startswith("knownItems=") and section:
            found[section] = index

    return found


def set_key(lines, start, end, key, value):
    target = next(
        (i for i in range(start, end) if lines[i].startswith(key + "=")),
        None,
    )

    if target is None:
        lines.insert(end, f"{key}={value}")
        return end + 1

    lines[target] = f"{key}={value}"
    return end


def read_key(lines, start, end, key):
    for i in range(start, end):
        if lines[i].startswith(key + "="):
            return [item for item in lines[i].split("=", 1)[1].split(",") if item]

    return []


def main():
    vol = "--vol" in sys.argv[1:]
    hidden = HIDDEN + ["org.kde.plasma.volume"] if vol else HIDDEN

    if not os.path.exists(CONFIG):
        sys.exit(f"config nao encontrada: {CONFIG}")

    lines = open(CONFIG).read().splitlines()
    sections = systray_sections(lines)

    if not sections:
        sys.exit("nenhuma bandeja do sistema encontrada")

    changed = 0

    for known_index in sorted(sections.values(), reverse=True):
        start = known_index

        while start > 0 and not lines[start].startswith("["):
            start -= 1

        end = start + 1

        while end < len(lines) and not lines[end].startswith("["):
            end += 1

        while end > start + 1 and not lines[end - 1].strip():
            end -= 1

        end = set_key(lines, start, end, "hiddenItems", ",".join(hidden))

        if vol:
            extra = read_key(lines, start, end, "extraItems")

            if extra and VOL not in extra:
                end = set_key(lines, start, end, "extraItems", ",".join(extra + [VOL]))

            shown = read_key(lines, start, end, "shownItems")

            if VOL not in shown:
                end = set_key(lines, start, end, "shownItems", ",".join(shown + [VOL]))

        changed += 1

    open(CONFIG, "w").write("\n".join(lines) + "\n")
    print(f"bandeja limpa em {changed} secao(oes)")


if __name__ == "__main__":
    main()
