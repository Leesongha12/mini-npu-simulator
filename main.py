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
        row_input = input(f"{len(matrix) + 1}번째 줄: ")
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

    avg_time = (total_time / repeat) * 1000
    return avg_time


def decide(score_a, score_b):
    if abs(score_a - score_b) < EPSILON:
        return "UNDECIDED"
    elif score_a > score_b:
        return "A"
    else:
        return "B"


def run_user_input_mode():
    print()
    print("#---------------------------------------")
    print("# [1] 필터 입력")
    print("#---------------------------------------")
    filter_a = input_matrix(3, "필터 A")
    filter_b = input_matrix(3, "필터 B")

    print()
    print("#---------------------------------------")
    print("# [2] 패턴 입력")
    print("#---------------------------------------")
    pattern = input_matrix(3, "패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    time_a = measure_mac_time(pattern, filter_a)
    time_b = measure_mac_time(pattern, filter_b)
    avg_time = (time_a + time_b) / 2

    result = decide(score_a, score_b)

    print()
    print("#---------------------------------------")
    print("# [3] MAC 결과")
    print("#---------------------------------------")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")
    print(f"연산 시간(평균/10회): {avg_time:.6f} ms")
    print(f"판정: {result}")


def run_json_mode():
    print()
    print("data.json 분석 모드는 다음 단계에서 구현합니다.")


def main():
    while True:
        print("=== Mini NPU Simulator ===")
        print()
        print("[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("0. 종료")

        choice = input("선택: ").strip()

        if choice == "1":
            run_user_input_mode()
            break
        elif choice == "2":
            run_json_mode()
            break
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택하세요.")
            print()


if __name__ == "__main__":
    main()