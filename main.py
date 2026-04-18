import json
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


def normalize_expected_label(label):
    if label == "+":
        return "Cross"
    elif label == "x":
        return "X"
    return "UNKNOWN"


def normalize_filter_key(key):
    if key == "cross":
        return "Cross"
    elif key == "x":
        return "X"
    return "UNKNOWN"


def decide_label(score_cross, score_x):
    if abs(score_cross - score_x) < EPSILON:
        return "UNDECIDED"
    elif score_cross > score_x:
        return "Cross"
    else:
        return "X"


def load_json_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)


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
    data = load_json_file("data.json")

    filters = data["filters"]
    patterns = data["patterns"]

    print()
    print("#---------------------------------------")
    print("# [1] 필터 로드")
    print("#---------------------------------------")

    loaded_filters = {}

    for size_key, filter_group in filters.items():
        loaded_filters[size_key] = {}

        for filter_key, filter_matrix in filter_group.items():
            label = normalize_filter_key(filter_key)
            loaded_filters[size_key][label] = filter_matrix

        print(f"✓ {size_key} 필터 로드 완료")

    print()
    print("#---------------------------------------")
    print("# [2] 패턴 분석")
    print("#---------------------------------------")

    total_count = 0
    pass_count = 0
    fail_count = 0

    for pattern_key, pattern_info in patterns.items():
        total_count += 1

        pattern_input = pattern_info["input"]
        expected_raw = pattern_info["expected"]
        expected_label = normalize_expected_label(expected_raw)

        parts = pattern_key.split("_")
        size_number = parts[1]
        size_key = f"size_{size_number}"

        cross_filter = loaded_filters[size_key]["Cross"]
        x_filter = loaded_filters[size_key]["X"]

        score_cross = mac(pattern_input, cross_filter)
        score_x = mac(pattern_input, x_filter)
        result_label = decide_label(score_cross, score_x)

        if result_label == expected_label:
            test_result = "PASS"
            pass_count += 1
        else:
            test_result = "FAIL"
            fail_count += 1

        print(f"--- {pattern_key} ---")
        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")
        print(f"판정: {result_label} | expected: {expected_label} | {test_result}")
        print()

    print("#---------------------------------------")
    print("# [3] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {total_count}개")
    print(f"통과: {pass_count}개")
    print(f"실패: {fail_count}개")


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