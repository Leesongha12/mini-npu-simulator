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


def get_operation_count(matrix):
    return len(matrix) * len(matrix[0])


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


def is_square_matrix(matrix):
    if not matrix or not isinstance(matrix, list):
        return False

    size = len(matrix)
    for row in matrix:
        if not isinstance(row, list) or len(row) != size:
            return False
    return True


def get_matrix_size(matrix):
    return len(matrix)


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
    failed_cases = []
    performance_rows = []

    for pattern_key, pattern_info in patterns.items():
        total_count += 1

        pattern_input = pattern_info["input"]
        expected_raw = pattern_info["expected"]
        expected_label = normalize_expected_label(expected_raw)

        parts = pattern_key.split("_")
        size_number = parts[1]
        size_key = f"size_{size_number}"

        fail_reason = None

        if size_key not in loaded_filters:
            fail_reason = f"{size_key} 필터가 존재하지 않음"

        elif not is_square_matrix(pattern_input):
            fail_reason = "입력 패턴이 정사각형 행렬이 아님"

        else:
            cross_filter = loaded_filters[size_key].get("Cross")
            x_filter = loaded_filters[size_key].get("X")

            if cross_filter is None or x_filter is None:
                fail_reason = "Cross 또는 X 필터 누락"

            elif not is_square_matrix(cross_filter) or not is_square_matrix(x_filter):
                fail_reason = "필터가 정사각형 행렬이 아님"

            else:
                pattern_size = get_matrix_size(pattern_input)
                cross_size = get_matrix_size(cross_filter)
                x_size = get_matrix_size(x_filter)

                if pattern_size != cross_size or pattern_size != x_size:
                    fail_reason = "패턴과 필터 크기 불일치"

        print(f"--- {pattern_key} ---")

        if fail_reason is not None:
            fail_count += 1
            failed_cases.append((pattern_key, fail_reason))
            print(f"FAIL 사유: {fail_reason}")
            print()
            continue

        score_cross = mac(pattern_input, cross_filter)
        score_x = mac(pattern_input, x_filter)
        result_label = decide_label(score_cross, score_x)

        time_cross = measure_mac_time(pattern_input, cross_filter)
        time_x = measure_mac_time(pattern_input, x_filter)
        avg_time = (time_cross + time_x) / 2
        operation_count = get_operation_count(pattern_input)

        performance_rows.append(
            (f"{pattern_size}x{pattern_size}", avg_time, operation_count)
        )

        if result_label == expected_label:
            test_result = "PASS"
            pass_count += 1
        else:
            test_result = "FAIL"
            fail_count += 1
            if result_label == "UNDECIDED":
                failed_cases.append((pattern_key, "동점 규칙에 따라 UNDECIDED 처리"))
            else:
                failed_cases.append((pattern_key, f"expected={expected_label}, actual={result_label}"))

        print(f"Cross 점수: {score_cross}")
        print(f"X 점수: {score_x}")
        print(f"판정: {result_label} | expected: {expected_label} | {test_result}")
        print(f"연산 시간(평균/10회): {avg_time:.6f} ms")
        print()

    print("#---------------------------------------")
    print("# [3] 성능 분석")
    print("#---------------------------------------")
    print("크기\t평균 시간(ms)\t연산 횟수(N²)")

    printed_sizes = set()
    for size_text, avg_time, operation_count in performance_rows:
        if size_text not in printed_sizes:
            print(f"{size_text}\t{avg_time:.6f}\t{operation_count}")
            printed_sizes.add(size_text)

    print()
    print("#---------------------------------------")
    print("# [4] 결과 요약")
    print("#---------------------------------------")
    print(f"총 테스트: {total_count}개")
    print(f"통과: {pass_count}개")
    print(f"실패: {fail_count}개")

    if failed_cases:
        print()
        print("실패 케이스:")
        for case_name, reason in failed_cases:
            print(f"- {case_name}: {reason}")


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