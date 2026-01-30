#!/usr/bin/env python3
import sys
import os


def parse_ints_from_line(line, where):
    parts = line.strip().split()
    if len(parts) == 0:
        raise ValueError(f"INVALID (empty line in {where})")
    try:
        return [int(x) for x in parts]
    except ValueError:
        raise ValueError(f"INVALID (non-integer token in {where})")


def is_permutation_1_to_n(values, n):
    if len(values) != n:
        return False
    seen = [False] * (n + 1)
    for v in values:
        if v < 1 or v > n or seen[v]:
            return False
        seen[v] = True
    return True


def file_path_next_to_script(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)


def read_preferences_from_file(filename="input.txt"):
    path = file_path_next_to_script(filename)
    try:
        with open(path, "r") as f:
            raw_lines = [ln for ln in f.read().splitlines() if ln.strip() != ""]
    except OSError:
        raise ValueError(f"INVALID (could not open {filename})")

    if len(raw_lines) == 0:
        raise ValueError("INVALID (empty input file)")

    try:
        n = int(raw_lines[0].strip())
    except ValueError:
        raise ValueError("INVALID (first line must be integer n)")

    if n <= 0:
        raise ValueError("INVALID (n must be >= 1)")

    expected_lines = 1 + 2 * n
    if len(raw_lines) != expected_lines:
        raise ValueError(
            f"INVALID (expected {expected_lines} non-empty lines in {filename}, got {len(raw_lines)})"
        )

    idx = 1

    hospital_prefs = []
    for h in range(1, n + 1):
        vals = parse_ints_from_line(raw_lines[idx], f"hospital preference line {h}")
        if not is_permutation_1_to_n(vals, n):
            raise ValueError(f"INVALID (hospital preference line {h} is not a permutation of 1..{n})")
        hospital_prefs.append(vals)
        idx += 1

    student_prefs = []
    for s in range(1, n + 1):
        vals = parse_ints_from_line(raw_lines[idx], f"student preference line {s}")
        if not is_permutation_1_to_n(vals, n):
            raise ValueError(f"INVALID (student preference line {s} is not a permutation of 1..{n})")
        student_prefs.append(vals)
        idx += 1

    return n, hospital_prefs, student_prefs


def read_matching_from_file(n, filename="output.txt"):
    path = file_path_next_to_script(filename)
    try:
        with open(path, "r") as f:
            lines = [ln for ln in f.read().splitlines() if ln.strip() != ""]
    except OSError:
        raise ValueError(f"INVALID (could not open {filename})")

    if len(lines) != n:
        raise ValueError(f"INVALID (expected {n} matching lines in {filename}, got {len(lines)})")

    pairs = []
    for i in range(n):
        parts = lines[i].strip().split()
        if len(parts) != 2:
            raise ValueError(f"INVALID (matching line {i+1} must be 'hospital student')")
        try:
            h = int(parts[0])
            s = int(parts[1])
        except ValueError:
            raise ValueError(f"INVALID (non-integer token in matching line {i+1})")
        pairs.append((h, s))

    return pairs


# ----------------------------
# Part (a) Validity ONLY
# ----------------------------

def check_validity(n, matching_pairs):
    hospital_seen = [False] * (n + 1)
    student_seen = [False] * (n + 1)

    for (h, s) in matching_pairs:
        if not (1 <= h <= n):
            return False, f"INVALID (hospital id out of range: {h})"
        if not (1 <= s <= n):
            return False, f"INVALID (student id out of range: {s})"

        if hospital_seen[h]:
            return False, f"INVALID (duplicate hospital in matching: {h})"
        hospital_seen[h] = True

        if student_seen[s]:
            return False, f"INVALID (duplicate student in matching: {s})"
        student_seen[s] = True

    for h in range(1, n + 1):
        if not hospital_seen[h]:
            return False, f"INVALID (hospital {h} missing from matching)"
    for s in range(1, n + 1):
        if not student_seen[s]:
            return False, f"INVALID (student {s} missing from matching)"

    return True, "VALID"


def main():
    try:
        n, _, _ = read_preferences_from_file("input.txt")
        matching_pairs = read_matching_from_file(n, "output.txt")

        valid, msg = check_validity(n, matching_pairs)
        print(msg)

    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    main()

