import os

def gale_shapley(n, hospital_preferences, student_preferences):
    # from slides: initialize each person and hospital to be free

    hospital_pairings = [0] * (n+1)
    student_pairings = [0] * (n+1)
    next_proposal = [0] * (n+1)

    free_hospitals_stack = list(range(1, n+1))

    while free_hospitals_stack:  #some hospital is free and hasn’t been matched/assigned to every applicant)
        current_hospital = free_hospitals_stack.pop()

        # 1st applicant on h's list to whom h has not been matched
        applicant = hospital_preferences[current_hospital - 1][next_proposal[current_hospital]]
        next_proposal[current_hospital] += 1

        #if applicant is free assign hospital to applicant
        if student_pairings[applicant] == 0:
            student_pairings[applicant] = current_hospital
            hospital_pairings[current_hospital] = applicant
        else: #a prefers h to her/his current assignment h'
            assigned_hospital = student_pairings[applicant]

            prefers_new_hospital = False
            for preferred_hospital in student_preferences[applicant - 1]:
                if preferred_hospital == current_hospital:
                    prefers_new_hospital = True
                    break
                if preferred_hospital == assigned_hospital:
                    prefers_new_hospital = False
                    break

            if prefers_new_hospital:
                hospital_pairings[assigned_hospital] = 0
                student_pairings[applicant] = current_hospital
                hospital_pairings[current_hospital] = applicant

                if next_proposal[assigned_hospital] < n:
                    free_hospitals_stack.append(assigned_hospital)

            else:
                if next_proposal[current_hospital] < n:
                    free_hospitals_stack.append(current_hospital)

    return hospital_pairings[1:]

def file_path_next_to_script(filename):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, filename)

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


def write_matching_to_file(n, hospital_pairings, filename="output.txt"):
    path = file_path_next_to_script(filename)
    with open(path, "w") as f:
        for h in range(1, n + 1):
            s = hospital_pairings[h - 1]
            f.write(f"{h} {s}\n")


def main():
    n, hospital_prefs, student_prefs = read_preferences_from_file("input.txt")
    matching_pairs = gale_shapley(n, hospital_prefs, student_prefs)
    write_matching_to_file(n, matching_pairs, "output_gale_shapley.txt")


if __name__ == "__main__":
    main()
