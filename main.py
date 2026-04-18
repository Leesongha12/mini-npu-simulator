def mac(matrix_a, matrix_b):
    total = 0.0
    for i in range(len(matrix_a)):
        for j in range(len(matrix_a[i])):
            total += matrix_a[i][j] * matrix_b[i][j]
    return total


def main():
    cross = [
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ]

    x_shape = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]

    pattern = [
        [1, 0, 1],
        [0, 1, 0],
        [1, 0, 1]
    ]

    cross_score = mac(pattern, cross)
    x_score = mac(pattern, x_shape)

    print("=== Mini NPU Simulator ===")
    print(f"Cross 점수: {cross_score}")
    print(f"X 점수: {x_score}")


if __name__ == "__main__":
    main()