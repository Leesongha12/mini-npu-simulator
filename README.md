# Mini NPU Simulator

## 1. 프로젝트 소개

이 프로젝트는 MAC(Multiply-Accumulate) 연산의 원리를 직접 구현해 보는 Mini NPU Simulator입니다.
컴퓨터는 사람이처럼 이미지를 직관적으로 이해하지 못하고, 숫자 배열 형태로 입력된 데이터만 처리할 수 있습니다.
따라서 십자가(Cross), X와 같은 패턴도 2차원 배열로 변환한 뒤, 필터와의 유사도를 계산해야 합니다.

이 프로그램은 입력 패턴과 필터를 같은 위치끼리 곱하고 모두 더하는 방식으로 점수를 계산하며, 더 높은 점수를 받은 필터를 기준으로 패턴을 판별합니다.
또한 사용자 입력 모드와 `data.json` 분석 모드를 제공하여, 직접 입력한 데이터와 파일 기반 테스트 데이터를 모두 처리할 수 있도록 구현했습니다.

---

## 2. 개발 환경

* Python 3.8 이상
* 운영체제: Windows (Galaxy Book)
* 사용 도구: Git Bash, VSCode
* 외부 라이브러리: 사용하지 않음
* 사용 라이브러리: json, time

---

## 3. 실행 방법

### 3-1. 프로젝트 폴더로 이동

```bash
cd ~/mini-npu-simulator
```

또는

```bash
cd ~/Desktop/mini-npu-simulator
```

### 3-2. 프로그램 실행

```bash
python main.py
```

### 3-3. 모드 선택

```text
=== Mini NPU Simulator ===

[모드 선택]
1. 사용자 입력 (3x3)
2. data.json 분석
0. 종료
선택:
```

---

## 4. 파일 구성

```text
mini-npu-simulator/
├─ main.py
├─ data.json
└─ README.md
```

---

## 5. 구현 기능 요약

### 5-1. 사용자 입력 모드

* 3x3 필터 A, B 입력
* 3x3 패턴 입력
* 입력 검증 (숫자 개수, 형식 오류)
* 잘못 입력 시 재입력 유도

---

### 5-2. MAC 연산

* 동일 위치 값끼리 곱셈 후 누적 합
* 이중 반복문으로 직접 구현
* 외부 라이브러리 사용 없음

---

### 5-3. 판정 로직

* 점수 비교 기반 판정
* epsilon(1e-9) 기반 동점 처리

판정 규칙:

* |A - B| < epsilon → UNDECIDED
* A > B → A (또는 Cross)
* B > A → B (또는 X)

---

### 5-4. JSON 분석 모드

* data.json 로드
* filters / patterns 구조 파싱
* 패턴 이름에서 size 추출
* 필터 매칭 후 MAC 계산
* expected와 비교하여 PASS / FAIL 출력

---

### 5-5. 라벨 정규화

* "+" → Cross
* "x" → X
* "cross" → Cross
* "x" → X

내부 기준을 통일하여 비교 안정성 확보

---

### 5-6. 성능 분석

* time.perf_counter() 사용
* 10회 반복 후 평균 시간(ms) 계산
* N×N → 연산 횟수 N² 출력

---

## 6. 실행 예시

### 사용자 입력 모드

```text
A 점수: 1.0
B 점수: 5.0
연산 시간: 0.010 ms
판정: B
```

---

### JSON 분석 모드

```text
--- size_5_1 ---
판정: Cross | expected: Cross | PASS

--- size_5_2 ---
판정: X | expected: X | PASS

총 테스트: 2
통과: 2
실패: 0
```

---

## 7. 결과 리포트

본 프로젝트는 사용자 입력과 JSON 분석 두 가지 모드를 통해 MAC 연산 기반 패턴 판별을 구현하였다.
입력 검증을 통해 프로그램 안정성을 확보하였고, 잘못된 입력에도 프로그램이 종료되지 않도록 설계하였다.

JSON 분석에서는 필터와 패턴을 분리된 구조로 처리하고, 패턴 이름에서 크기 정보를 추출하여 적절한 필터를 선택하도록 구현하였다.
또한 라벨 정규화를 통해 데이터 표현 방식의 차이를 내부적으로 통일하였다.

부동소수점 비교 문제를 해결하기 위해 epsilon 기반 비교를 적용하였다.
이를 통해 미세한 오차로 인한 잘못된 판정을 방지하였다.

현재 데이터 기준 실패 케이스는 0개이며, 이는 정규화와 비교 정책이 안정적으로 동작했기 때문이다.

---

## 8. 시간 복잡도 분석

MAC 연산은 N×N 행렬 전체를 순회하므로 시간 복잡도는 O(N²)이다.

예시:

* 3x3 → 9
* 5x5 → 25
* 13x13 → 169
* 25x25 → 625

입력 크기가 증가할수록 연산량은 제곱 단위로 증가한다.
이는 실제 AI 연산에서도 동일하게 나타나는 특징이며, NPU가 필요한 이유를 설명한다.

---

## 9. 커밋 기록

```bash
chore: initialize project structure
feat: add main menu
feat: implement MAC operation
feat: add user input mode
feat: add decision logic
feat: add execution time measurement
refactor: add mode structure
feat: add json analysis
feat: enhance json analysis
docs: complete README
```

---

## 10. 느낀 점

이번 과제를 통해 단순 구현을 넘어 입력 검증, 데이터 처리, 성능 분석, 문서화까지 포함한 전체 개발 과정을 경험할 수 있었다.
특히 README 작성을 통해 코드의 동작 원리를 설명하는 과정이 중요하다는 점을 느꼈다.
