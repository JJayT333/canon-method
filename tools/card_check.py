"""Check the mechanically verifiable parts of a worker card (canon method v1).

Usage: python tools/card_check.py <CARD.md> [--withhold-words]

Exit 0 and PASS when every mechanical rule holds; exit 1 and one FAIL line per
rule broken otherwise. The MANUAL lines name what a script cannot judge.
--withhold-words is for a card sent to a model the operator does not want quoted:
the objective must then say "Words withheld" instead of quoting them.
"""
import argparse
import re
import sys
from pathlib import Path

FIELDS = ["OBJECTIVE", "STARTING STATE", "SAVE AS YOU GO", "READ FIRST",
          "READ AND SKIP", "SCOPE", "STEPS", "WHAT GOOD LOOKS LIKE",
          "WHAT BAD LOOKS LIKE", "DONE WHEN", "VERIFY", "TIME LIMIT", "RETURN"]
COMMON = {"OBJECTIVE", "SAVE AS YOU GO", "READ FIRST", "SCOPE", "DONE WHEN", "TIME LIMIT", "RETURN"}
# Families: A make or fix, B check, C files and records, D find out, E build with proof,
# F write, G repair a tool. Each adds fields to the common set.
EXTRA = {
    "A": {"STARTING STATE", "STEPS"},
    "B": {"STARTING STATE", "READ AND SKIP", "STEPS", "WHAT GOOD LOOKS LIKE", "WHAT BAD LOOKS LIKE", "VERIFY"},
    "C": {"STARTING STATE"},
    "D": {"READ AND SKIP", "STEPS", "WHAT GOOD LOOKS LIKE", "WHAT BAD LOOKS LIKE", "VERIFY"},
    "E": {"STARTING STATE", "READ AND SKIP", "STEPS", "WHAT GOOD LOOKS LIKE", "WHAT BAD LOOKS LIKE", "VERIFY"},
    "F": {"WHAT GOOD LOOKS LIKE", "WHAT BAD LOOKS LIKE"},
    "G": {"STARTING STATE", "READ AND SKIP", "STEPS", "VERIFY"},
}
NUM = {"OBJECTIVE": 2, "STARTING STATE": 10, "SAVE AS YOU GO": 3,
       "READ FIRST": 4, "READ AND SKIP": 4, "SCOPE": 5, "STEPS": 10,
       "WHAT GOOD LOOKS LIKE": 8, "WHAT BAD LOOKS LIKE": 8,
       "DONE WHEN": 6, "VERIFY": 10, "TIME LIMIT": 7, "RETURN": 9}
WORDS = r"(?:Operator's|The operator's|Operator) words"
MAX_LINES = 60


def check(text, withhold=False):
    lines = text.splitlines()
    failures = []

    def fail(number, message):
        failures.append((number, message))

    if not lines or not re.match(r"^Runs on:\s*\S.*\([^()]*\S[^()]*\)", lines[0]):
        fail(1, "Line one must start Runs on: and include a parenthesized reason.")
    family_lines = [line for line in lines if re.match(r"^Family:", line, re.I)]
    family = "A"
    if family_lines:
        match = re.match(r"^Family:\s*([A-G])(?:\b|$)", family_lines[0], re.I)
        if not match or len(family_lines) != 1:
            fail(10, "Family must be a single Family: A through G line.")
        else:
            family = match.group(1).upper()
    pattern = re.compile(r"^(" + "|".join(re.escape(f) for f in FIELDS) + r"):\s*(.*)$")
    found = {}
    current = None
    previous = -1
    for line_no, line in enumerate(lines, 1):
        m = pattern.match(line)
        if m:
            name, first = m.groups()
            index = FIELDS.index(name)
            if name in found:
                fail(NUM[name], f"Duplicate {name} field at line {line_no}.")
            elif index <= previous:
                fail(NUM[name], f"{name} is out of order at line {line_no}.")
            previous = max(previous, index)
            found[name] = [line_no, first]
            current = name
        elif current:
            found[current][1] += "\n" + line
    for field in FIELDS:
        if field in COMMON | EXTRA[family] and (field not in found or not found[field][1].strip()):
            fail(NUM[field], f"Missing or empty {field} field for family {family}.")

    def value(field):
        return found.get(field, [0, ""])[1]

    objective = value("OBJECTIVE")
    if objective:
        if withhold:
            if "Words withheld" not in objective:
                fail(2, "A withhold-words card must say Words withheld in its OBJECTIVE.")
            if re.search(WORDS + r"\s*\([^)]*\)\s*:\s*[\"“]", text, re.I):
                fail(2, "A withhold-words card appears to quote the operator.")
        elif not re.search(WORDS + r'\s*\([^)]*\d{4}[-/]\d{1,2}[-/]\d{1,2}[^)]*\)\s*:\s*["“][^"”\n]+["”]', objective):
            fail(2, "OBJECTIVE needs Operator's words (date): followed by a quoted line.")
    save = value("SAVE AS YOU GO")
    if save and (not re.search(r'(?:[A-Za-z]:[\\/]|/|(?:[\w.-]+[\\/])+)[^\s,;]+', save) or 'STATUS: RUNNING' not in save):
        fail(3, "SAVE AS YOU GO needs an exact path and STATUS: RUNNING.")
    bad = value("WHAT BAD LOOKS LIKE")
    if bad:
        if not re.search(r'\bBAD EXAMPLE\b', bad, re.I):
            fail(8, "WHAT BAD LOOKS LIKE needs a labeled BAD EXAMPLE.")
        for part in re.split(r'[;\n]', bad):
            if re.search(r'\bdo not\b', part, re.I) and not re.search(r'\binstead\b', part, re.I):
                fail(8, "Each do not in WHAT BAD LOOKS LIKE needs an instead in the same clause.")
    time = value("TIME LIMIT")
    if time:
        match = re.search(r'\b(\d+(?:\.\d+)?)\s+hours?\b', time, re.I)
        if not match or not 0 < float(match.group(1)) <= 12:
            fail(7, "TIME LIMIT must name more than zero and at most 12 hours.")
    ret = value("RETURN")
    if ret and any(not re.search(r'\b' + label + r'\b', ret) for label in ("VERIFIED", "INFERRED", "UNVERIFIED", "NOT FOUND", "MISSING FACTS")):
        fail(9, "RETURN needs VERIFIED, INFERRED, UNVERIFIED, NOT FOUND and MISSING FACTS.")
    if '—' in text or '–' in text:
        fail(12, "Remove em-dashes and en-dashes.")
    if len(lines) > MAX_LINES:
        fail(12, f"Card has {len(lines)} lines; maximum is {MAX_LINES}.")
    return sorted(failures), found


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("card", type=Path)
    parser.add_argument("--withhold-words", action="store_true")
    args = parser.parse_args()
    try:
        text = args.card.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        print(f"FAIL 0: Cannot read card: {exc}")
        return 1
    failures, found = check(text, args.withhold_words)
    for number, message in failures:
        print(f"FAIL {number}: {message}")
    if not failures:
        print("PASS")
    print(f"MANUAL 6: Read DONE WHEN at line {found.get('DONE WHEN', ['missing'])[0]} for checkability.")
    print("MANUAL 11: Read the whole card for added scope and unsupported claims.")
    if args.withhold_words:
        print("MANUAL 2: Read the whole card for quoted operator text.")
    print("MANUAL 10: Read the family's requirements for anything a script cannot judge.")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
