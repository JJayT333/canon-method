"""Check the mechanically verifiable parts of a worker card (canon method v1).

Usage: python tools/card_check.py <CARD.md> [--form codex|claude|auto] [--withhold-words]

Two forms. The Codex form (line one Runs on:, then OBJECTIVE to RETURN) is the default and is
what launchers/fire-codex-job.ps1 runs. The Claude lane form (line one # CARD:, a Model: line,
an Operator's words, verbatim: block, ## sections) is what skills/fire-opus-worker fires with the
Agent tool; launchers/check_card.ps1 is its gate. --form auto picks by line one.

Exit 0 and PASS when every mechanical rule holds; exit 1 and one FAIL line per rule broken
otherwise. The MANUAL lines name what a script cannot judge. --withhold-words is for a Codex-form
card sent to a model the operator does not want quoted: the objective must then say "Words withheld".
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
EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)
CARD_PATH = re.compile(r'(?:[A-Za-z]:[\\/]|/|(?:[\w.-]+[\\/])+)[^\s,;]+')


def check(text, withhold=False):
    """Check the Codex form (cards/TEMPLATE-codex-job-card.md and TEMPLATE-acceptance-card.md)."""
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
    if save and (not CARD_PATH.search(save) or 'STATUS: RUNNING' not in save):
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
    if EM_DASH in text or EN_DASH in text:
        fail(12, "Remove em-dashes and en-dashes.")
    if len(lines) > MAX_LINES:
        fail(12, f"Card has {len(lines)} lines; maximum is {MAX_LINES}.")
    return sorted(failures), found


# The Claude lane form (cards/TEMPLATE-claude-lane-card.md).
CLAUDE_TITLE = re.compile(r"^# CARD:\s*\S.*\(\s*\d{4}-\d{2}-\d{2}\b[^()]*\)")
DATED_QUOTE = re.compile(r'(?:\d{4}-\d{2}-\d{2}|\b\d{1,2}:\d{2}\b)[^"“\n]{0,40}["“][^"”\n]+["”]')
NO_COMMIT = re.compile(r"\bno (?:git )?commits?\b|\bnever commits?\b|\bcommit nothing\b", re.I)
WORDS_BLOCK = re.compile(r"^(?:Operator's|The operator's|Operator) words, verbatim\b.*:")


def detect_form(text, withhold=False):
    """The Claude lane form starts '# CARD:'; everything else is read as the Codex form.

    A withhold-words card is always the Codex form, whatever its line one: the Claude lane
    form quotes the operator by design, so auto never selects it for a withheld card.
    """
    if withhold:
        return "codex"
    return "claude" if text.startswith("# CARD:") else "codex"


def check_claude(text):
    """Check the Claude lane card form: title, Model, Operator's words, sections."""
    lines = text.splitlines()
    failures = []

    def fail(number, message):
        failures.append((number, message))

    if not lines or not CLAUDE_TITLE.match(lines[0]):
        fail(1, "Line one must be # CARD: <title> with a parenthesized YYYY-MM-DD date.")
    found = {}
    current = None
    for line_no, line in enumerate(lines, 1):
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading:
            current = heading.group(1).strip()
            if current.lower() in {k.lower() for k in found}:
                current = None
            else:
                found[current] = [line_no, ""]
        elif current:
            found[current][1] += "\n" + line
    first_heading = next((n for n, line in enumerate(lines) if line.startswith("## ")), len(lines))
    models = [(n, line) for n, line in enumerate(lines[:first_heading], 1) if re.match(r"^Model:", line)]
    if len(models) != 1:
        fail(1, "The header (before the first ## heading) needs exactly one Model: line.")
    else:
        named = models[0][1][len("Model:"):].strip()
        if not re.search(r"[A-Za-z]", named) or re.match(r"(?i)(?:inherit|default|same\b|the desk'?s)", named):
            fail(1, "The Model: line must name the model; a lane never inherits the desk's.")
        else:
            found["MODEL"] = [models[0][0], named]
    words_at = next((n for n, line in enumerate(lines) if WORDS_BLOCK.match(line)), None)
    if words_at is None:
        fail(2, "Needs an Operator's words, verbatim: block.")
    else:
        block = [lines[words_at]]
        for line in lines[words_at + 1:]:
            if not line.strip() or line.startswith("#"):
                break
            block.append(line)
        if not DATED_QUOTE.search("\n".join(block)):
            fail(2, "Operator's words, verbatim: needs at least one quote led by its date or clock time.")

    def section(prefix):
        return next((v for k, v in found.items() if k != "MODEL" and k.lower().startswith(prefix)), None)

    what = section("what this is")
    if not what or not what[1].strip():
        fail(2, "Missing or empty ## What this is section.")
    if not any(CARD_PATH.search(line) and re.search(r"\b[\w.-]+\.md\b", line)
               and re.search(r"\bfirst minute\b", line, re.I) and "STATUS: RUNNING" in line for line in lines):
        fail(3, "One line must name the output file path, first minute and STATUS: RUNNING.")
    bounds = section("boundaries")
    if not bounds or not bounds[1].strip():
        fail(5, "Missing or empty ## Boundaries section.")
    commit = section("commit")
    if not (commit and commit[1].strip()) and not NO_COMMIT.search(text):
        fail(5, "Needs a ## Commit section or a no-commit line.")
    shape = section("output.md shape") or section("done") or section("return")
    if not shape or not re.search(r"\bverdict\b|\bSTATUS\b", shape[1], re.I):
        fail(9, "Needs a ## OUTPUT.md shape (or Done when, Return) section naming the verdict or STATUS line.")
    if EM_DASH in text or EN_DASH in text:
        fail(12, "Remove em-dashes and en-dashes.")
    if len(lines) > MAX_LINES:
        fail(12, f"Card has {len(lines)} lines; maximum is {MAX_LINES}.")
    return sorted(failures), found


def check_card(text, withhold=False, form="codex"):
    """Return (failures, found, form) for the named form; auto picks it from line one."""
    if form == "auto":
        form = detect_form(text, withhold)
    if form == "claude":
        return (*check_claude(text), form)
    return (*check(text, withhold), form)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("card", type=Path)
    parser.add_argument("--form", choices=["codex", "claude", "auto"], default="codex",
                        help="codex (default; the Codex launcher), claude (the Claude lane card), auto (by line one)")
    parser.add_argument("--withhold-words", action="store_true")
    args = parser.parse_args()
    if args.withhold_words and args.form == "claude":
        parser.error("--withhold-words cards use the Codex form")
    try:
        text = args.card.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeError) as exc:
        print(f"FAIL 0: Cannot read card: {exc}")
        return 1
    failures, found, form = check_card(text, args.withhold_words, args.form)
    if args.form != "codex":
        print(f"FORM: {form}")
    for number, message in failures:
        print(f"FAIL {number}: {message}")
    if not failures:
        print("PASS")
    if form == "claude":
        print("MANUAL 6: Read the work, Checks and Walk sections for checkability.")
        print("MANUAL 11: Read the whole card for added scope and unsupported claims.")
        print("MANUAL 10: Read the work section for requirements a script cannot judge.")
        return int(bool(failures))
    print(f"MANUAL 6: Read DONE WHEN at line {found.get('DONE WHEN', ['missing'])[0]} for checkability.")
    print("MANUAL 11: Read the whole card for added scope and unsupported claims.")
    if args.withhold_words:
        print("MANUAL 2: Read the whole card for quoted operator text.")
    print("MANUAL 10: Read the family's requirements for anything a script cannot judge.")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
