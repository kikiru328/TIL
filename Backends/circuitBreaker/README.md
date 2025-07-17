# Circuit Breaker

[![CS Knowledge](https://img.shields.io/badge/CS-Backend-blue.svg)]()
[![Pattern](https://img.shields.io/badge/Pattern-Circuit%20Breaker-green.svg)]()
[![Implementation](https://img.shields.io/badge/Implementation-Python-red.svg)]()

> **외부 API 장애로부터 시스템을 보호하는 Circuit Breaker 패턴을 완전히 이해하고 직접 구현**

## 학습 동기

마이크로서비스 환경에서 외부 의존성 장애가 전체 시스템으로 전파되는 문제를 해결하기 위해 Circuit Breaker 패턴을 제대로 이해하고 실제 동작 방식을 확인해보았습니다.

## 핵심 학습 내용

### Circuit Breaker란?

**"외부 서비스 장애 시 추가 호출을 차단해서 시스템을 보호하는 패턴"**

#### 일상생활 비유로 이해하기
- **전기 차단기**: "과부하 감지 시 전원 차단으로 화재 방지"
- **엘리베이터 점검**: "고장 시 '점검 중' 표시하고 사용 금지"
- **ATM 서비스**: "장애 시 '서비스 일시 중단' 안내"
- **친구 전화**: "계속 안 받으면 나중에 다시 걸기"

#### 왜 필요한가?
1. **리소스 보호**: 죽은 API에 계속 요청하며 서버 리소스 낭비 방지
2. **빠른 실패**: 타임아웃까지 기다리지 않고 즉시 실패 처리
3. **사용자 경험**: "로딩 중..." 대신 "일시 중단" 같은 명확한 안내
4. **복구 시간 확보**: 외부 서비스가 회복할 시간을 벌어줌

## 3가지 상태와 전환 메커니즘

### 1. CLOSED (닫힌 상태) - 정상 운영

#### 개념
전기가 정상적으로 흐르는 상태로, 모든 요청을 외부 API로 전달

```
[사용자 요청] → [Circuit Breaker CLOSED] → [외부 API] → [응답]
```

#### 특징
- ✅ 모든 요청 허용
- 📊 실패 횟수 지속적으로 모니터링
- ⚠️ 실패 임계치 도달 시 OPEN으로 전환

### 2. OPEN (열린 상태) - 차단 중

#### 개념
차단기가 열려서 전기가 안 흐르는 상태로, 모든 요청을 즉시 차단

```
[사용자 요청] → [Circuit Breaker OPEN] → [즉시 실패 응답]
```

#### 특징
- 🚫 모든 요청 즉시 차단
- ⚡ 외부 API 호출 없이 빠른 실패 처리
- ⏰ 설정된 시간 후 자동으로 HALF-OPEN으로 전환

### 3. HALF-OPEN (반열린 상태) - 복구 테스트

#### 개념
복구되었는지 조심스럽게 테스트하는 상태로, 제한적 요청만 허용

```
[사용자 요청] → [Circuit Breaker HALF-OPEN] → [테스트 호출] → [성공/실패 판단]
```

#### 특징
- 🧪 제한된 수의 테스트 요청만 허용
- ✅ 성공 시 → CLOSED (완전 복구)
- ❌ 실패 시 → OPEN (다시 차단)

## 상태 전환 시나리오

### 정상에서 장애로
```
CLOSED → 실패 5회 누적 → OPEN
```

### 복구 테스트 시작
```
OPEN → 30초 경과 → HALF-OPEN
```

### 테스트 결과에 따른 분기
```
HALF-OPEN → 성공 → CLOSED (완전 복구)
HALF-OPEN → 실패 → OPEN (아직 장애 중)
```

## 핵심 구현 코드

### 기본 Circuit Breaker 구조

```python
class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=30):
        # 현재 상태 (초기값: 정상)
        self.state = State.CLOSED
        
        # 실패 추적 변수들
        self.failure_count = 0              # 연속 실패 횟수
        self.last_failure_time = 0          # 마지막 실패 시간
        
        # 설정값들
        self.failure_threshold = failure_threshold  # 실패 허용 한계
        self.timeout = timeout              # OPEN 상태 유지 시간

    def call(self, func, *args, **kwargs):
        # 1. 현재 상태에 따른 처리
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self.state = State.HALF_OPEN
            else:
                raise Exception("🚫 Circuit Breaker OPEN")
        
        # 2. 실제 API 호출 시도
        try:
            result = func(*args, **kwargs)
            self._on_success()  # 성공 처리
            return result
        except Exception as e:
            self._on_failure()  # 실패 처리
            raise e
```

### 핵심 상태 관리 로직

```python
def _on_success(self):
    """호출 성공: 모든 카운터 리셋하고 정상 상태로"""
    print("✅ 호출 성공 - 정상 상태로 복귀")
    self.failure_count = 0
    self.state = State.CLOSED

def _on_failure(self):
    """호출 실패: 카운터 증가하고 임계점 확인"""
    self.failure_count += 1
    self.last_failure_time = time.time()
    
    if self.failure_count >= self.failure_threshold:
        print("🔴 Circuit Breaker OPEN - 호출 차단 시작")
        self.state = State.OPEN
```

## 핵심 깨달음

### 1. Rate Limiting과의 차이점

| 구분 | Rate Limiting | Circuit Breaker |
|------|---------------|-----------------|
| **목적** | 과부하 방지 (성능) | 장애 전파 방지 (안정성) |
| **차단 기준** | 시간당 요청 수 | 실패율/장애 감지 |
| **적용 시점** | 정상 상황 | 비정상 상황 |
| **복구 방식** | 시간 경과로 자동 | 상태 기반 테스트 |
| **카테고리** | backend/performance | backend/resilience |

### 2. 실제 사용 시나리오

**Circuit Breaker 적용 필수**
- 🎯 **결제 시스템**: 토스, 카카오페이 등 외부 결제 API
- 🎯 **지도 서비스**: 구글맵, 네이버맵 API 연동
- 🎯 **알림 발송**: SMS, 이메일 발송 서비스
- 🎯 **추천 시스템**: 외부 AI/ML 서비스 연동

**설정 가이드**
```python
CONFIGS = {
    "결제_시스템": {"failure_threshold": 3, "timeout": 60},    # 엄격
    "추천_시스템": {"failure_threshold": 10, "timeout": 30},   # 관대
    "로그_전송": {"failure_threshold": 20, "timeout": 300}     # 매우 관대
}
```

### 3. 실무에서의 트레이드오프

| 기준 | 직접 구현 | pybreaker 라이브러리 |
|------|-----------|---------------------|
| **학습 효과** | 높음 | 낮음 |
| **안정성** | 낮음 (버그 위험) | 높음 (검증됨) |
| **커스터마이징** | 자유로움 | 제한적 |
| **유지보수** | 어려움 | 쉬움 |

## 실제 테스트 결과

### 장애 감지 테스트
```
요청 1: ❌ 실패 (1/3)
요청 2: ❌ 실패 (2/3)  
요청 3: ❌ 실패 (3/3) → 🔴 OPEN 상태로 전환
```

### 차단 상태 테스트
```
요청 4: 🚫 즉시 차단 (복구까지 8초)
요청 5: 🚫 즉시 차단 (복구까지 6초)
→ 외부 API 호출 없이 빠른 실패 처리 ✅
```

### 자동 복구 테스트
```
10초 후: 🔄 HALF-OPEN 상태로 전환
테스트 요청: ✅ 성공 → CLOSED 상태로 복귀
→ 자동 복구 메커니즘 동작 확인 ✅
```

## 학습 과정에서 겪은 어려움

### 1. 상태 전환 타이밍 이해
처음에는 "언제 상태가 바뀌는지" 헷갈렸는데, **실패 임계치와 시간 기반**의 두 가지 트리거를 이해하고 나서 명확해짐.

### 2. HALF-OPEN 상태의 역할
단순히 "중간 상태"라고만 생각했는데, 실제로는 **복구 여부를 판단하는 핵심 메커니즘**임을 깨달음.

### 3. Rate Limiting과의 구분
둘 다 "요청을 제어한다"는 공통점 때문에 헷갈렸는데, **목적과 적용 시점이 완전히 다름**을 이해하는 게 중요했음.

### 4. 실무 적용의 복잡성
간단해 보이지만 실제로는 **모니터링, 알림, 로깅** 등 부가 기능들이 필수라는 걸 깨달음.

## 실제 서비스에 적용한다면?

### 단계적 접근법
1. **1단계**: 중요도 낮은 외부 API부터 적용 (학습 + 경험 축적)
2. **2단계**: 모니터링과 알림 시스템 구축
3. **3단계**: 핵심 서비스로 점진적 확대
4. **4단계**: 팀 전체 Circuit Breaker 패턴 이해도 향상

### 하이브리드 적용 예시
```python
# 1. Rate Limiting으로 과부하 방지

@rate_limit(limit=100, window=60)

# 2. Circuit Breaker로 장애 전파 방지  

@circuit_breaker(failure_threshold=5, timeout=30)
def call_payment_api(amount):
    return external_payment_service.charge(amount)
```

## 핵심 인사이트

> **"장애는 피할 수 없지만, 전파는 막을 수 있다."**  
> Circuit Breaker는 외부 의존성으로부터 시스템을 보호하는 **디지털 보디가드**

### 핵심 메시지
- **Fail Fast**: 빠른 실패로 사용자 경험 개선
- **Auto Recovery**: 자동 복구로 운영 부담 감소  
- **Resilience**: 장애에 강한 시스템 구축의 핵심 패턴
- **Microservices**: 분산 환경에서 필수적인 안정성 패턴
