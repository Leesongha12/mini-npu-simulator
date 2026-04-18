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


def main():
    print("=== Mini NPU Simulator ===")
    filter_a = input_matrix(3, "필터 A")
    filter_b = input_matrix(3, "필터 B")
    pattern = input_matrix(3, "패턴")

    score_a = mac(pattern, filter_a)
    score_b = mac(pattern, filter_b)

    print()
    print("=== MAC 결과 ===")
    print(f"A 점수: {score_a}")
    print(f"B 점수: {score_b}")


if __name__ == "__main__":
    main()