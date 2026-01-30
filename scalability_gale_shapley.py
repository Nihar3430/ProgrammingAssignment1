import random
import time
import matplotlib.pyplot as plt
from GaleShapley import gale_shapley
def create_preferences(num):
    hospital_preferences = []
    student_preferences = []

    for i in range(num):
        hospital_preferences.append(random.sample(range(1, num + 1), num))

    for i in range(num):
        student_preferences.append(random.sample(range(1, num + 1), num))

    return hospital_preferences, student_preferences


def measure_running_time_and_graph():
    nums = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
    times = []

    for i in nums:
        hospital_preferences, student_preferences = create_preferences(i)
        start = time.perf_counter()
        gale_shapley(i, hospital_preferences, student_preferences)
        end = time.perf_counter()

        true_time = end - start
        times.append(true_time)

    plt.figure()
    plt.plot(nums, times, marker='o')
    plt.xlabel('Number of Hospitals/Students')
    plt.ylabel('Running Time (seconds)')
    plt.title('Gale-Shapley Algorithm Running Time')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    measure_running_time_and_graph()





