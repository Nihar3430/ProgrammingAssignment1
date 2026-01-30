import random
import time
import matplotlib.pyplot as plt

from GaleShapley import gale_shapley
from verifier import check_validity, check_stability


def create_preferences(num):
    hospital_preferences = []
    student_preferences = []

    for i in range(num):
        hospital_preferences.append(random.sample(range(1, num + 1), num))

    for i in range(num):
        student_preferences.append(random.sample(range(1, num + 1), num))

    return hospital_preferences, student_preferences


def build_matching_pairs(hospital_pairings):
    pairs = []
    for h in range(1, len(hospital_pairings) + 1):
        pairs.append((h, hospital_pairings[h - 1]))
    return pairs


def measure_running_time_and_graph():
    nums = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    times = []

    for i in nums:
        hospital_preferences, student_preferences = create_preferences(i)

        hospital_pairings = gale_shapley(i, hospital_preferences, student_preferences)
        matching_pairs = build_matching_pairs(hospital_pairings)

        start = time.perf_counter()

        valid, vmsg, h_to_s, s_to_h = check_validity(i, matching_pairs)

        if valid:
            check_stability(i, hospital_preferences, student_preferences, h_to_s, s_to_h)

        end = time.perf_counter()

        true_time = end - start
        times.append(true_time)

    plt.figure()
    plt.plot(nums, times, marker='o')
    plt.xlabel('Number of Hospitals/Students')
    plt.ylabel('Running Time (seconds)')
    plt.title('Verifier (Validity + Stability) Running Time')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    measure_running_time_and_graph()



