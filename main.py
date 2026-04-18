import time

EPSILON = 1e-9


def parse_row(text, expected_size):
    parts = text.strip().split()
    if len(parts) != expected_size:
        return None

    row = []
    try:
        for value in parts:
            row.append(float(value))
    except ValueError:
        return None
    return row


def input_matrix(size, name):
    print(f"{name} ({size}줄 입력, 공백 구분)")
    matrix = []

    while len(matrix) < size:
        row_input = input(f"{len(matrix)+1}번째 줄: ")
        row = parse_row(row_input, size)

        if row is None:
            print(f"입력 형식 오류: 각 줄에 {size}개의 숫자를 공백으로 구분해 입력하세요.")
            continue

        matrix.append(row)

    return matrix


def mac(matrix_a, matrix_b):
    total = 0.0
    for i in range(len(matrix_a)):
        for j in range(len(matrix_a[i])):
            total += matrix_a[i][j] * matrix_b[i][j]
    return total


def measure_mac_time(matrix_a, matrix_b, repeat=10):
    total_time = 0.0

    for _ in range(repeat):
        start = time.perf_counter()
        mac(matrix_a, matrix_b)
        end = time.perf_counter()
        total_time += (end - start)

    avg_time = (total_time / repeat) * 1000  # ms 변환
    return avg_time


def decide(score_a, score_b):
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"


def main():
    print("=== Mini NPU Simulator ===")

    filter_a = input_matrix(3, "필터 A")
    filter_b = input_matrix(3, "필터 B")
    pattern = input_matrix(3, "패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    time_a = measure_mac_time(pattern, filter_a)
    time_b = measure_mac_time(pattern, filter_b)
    avg_time = (time_a + time_b) / 2

    result = decide(score_a, score_b)

    print()
    print("=== MAC 결과 ===")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {avg_time:.6f} ms")
    print(f"판정: {result}")


if __name__ == "__main__":
    main()