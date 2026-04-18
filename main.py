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
            print("사용자 입력 모드를 선택했습니다.")
            break
        elif choice == "2":
            print("data.json 분석 모드를 선택했습니다.")
            break
        elif choice == "0":
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다. 다시 선택하세요.")
            print()


if __name__ == "__main__":
    main()