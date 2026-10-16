"""
Lab 9: MapReduce Log Analyzer -- grading script (given, do not edit).

Run: python mapper.py < logs.txt | sort | python reducer.py > output.txt
     python check_logs.py output.txt

Independently recomputes the top-10 endpoints from logs.txt (using
Python's collections.Counter, not your mapper/reducer) and diffs
against output.txt. Prints MAPREDUCE_SHUFFLE_VERIFIED on a match.

"""

import re
import sys
from collections import Counter

REQUEST_LINE_RE = re.compile(r'"[A-Z]+ (\S+) HTTP/')
LOG_FILE = "logs.txt"


def independent_top10(log_path: str):
    counts = Counter()
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            match = REQUEST_LINE_RE.search(line)
            if match:
                counts[match.group(1)] += 1
    ranked = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:10]


def parse_output(output_path: str):
    result = []
    with open(output_path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) != 2:
                print(f"  [FAIL] malformed output line (expected 'endpoint<TAB>count'): {line!r}")
                return None
            endpoint, count_str = parts
            try:
                result.append((endpoint, int(count_str)))
            except ValueError:
                print(f"  [FAIL] non-integer count in line: {line!r}")
                return None
    return result


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python check_logs.py output.txt")
        return 1

    expected = independent_top10(LOG_FILE)
    actual = parse_output(sys.argv[1])
    if actual is None:
        return 1

    print(f"Expected top 10 (independently computed from {LOG_FILE}):")
    for endpoint, count in expected:
        print(f"  {endpoint}\t{count}")

    print(f"\nYour output ({sys.argv[1]}):")
    for endpoint, count in actual:
        print(f"  {endpoint}\t{count}")

    match = expected == actual
    print()
    if not match:
        print("  [FAIL] output does not match the independently computed top 10. No token issued.")
        return 1

    print("  [PASS] output matches exactly\n")
    print("=" * 60)
    print("  SUCCESS TOKEN: MAPREDUCE_SHUFFLE_VERIFIED")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())
