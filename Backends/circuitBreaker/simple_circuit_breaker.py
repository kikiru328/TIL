import time
from enum import Enum


class State(Enum):
    CLOSED = 1  # 정상: 모든 요청 허용
    OPEN = 2  # 차단: 모든 요청 거부
    HALF_OPEN = 3  # 테스트: 제한적 허용


class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold=5, timeout=30):
        self.state = State.CLOSED
        self.failure_count = 0  # 연속 실패 횟수
        self.last_failure_time = 0  # 마지막 실패 시간
        self.failure_threshold = failure_threshold  # 실패 허용 한계
        self.timeout = timeout  # OPEN 상태 유지 시간(초)
        self.half_open_calls = 0  # HALF_OPEN에서 진행 중인 호출 수
        self.max_half_open_calls = 1  # 최대 허용 테스트 호출
        self.half_open_success_count = 0  # HALF_OPEN에서 성공한 호출 수

    def call(self, func, *args, **kwargs):
        # OPEN 상태: 차단 중인지 확인
        if self.state == State.OPEN:
            # 충분한 시간이 지났으면 테스트 모드로 전환
            if time.time() - self.last_failure_time > self.timeout:
                self._change_state(State.HALF_OPEN)
                self.half_open_calls = 0  # 카운터 리셋
                self.half_open_success_count = 0
            else:
                # 아직 차단 시간이므로 즉시 실패
                raise CircuitBreakerOpenException("Circuit Breaker Open")

        # HALF_OPEN 상태: 동시 호출 제한
        if self.state == State.HALF_OPEN:
            if self.half_open_calls >= self.max_half_open_calls:
                raise CircuitBreakerOpenException("Half-Open Test in Progress")
            self.half_open_calls += 1

        # 실제 API 호출 시도
        try:
            result = func(*args, **kwargs)
            self._success()  # 성공 처리
            return result
        except Exception as e:
            self._failure()  # 실패 처리
            raise e
        finally:
            # HALF_OPEN에서 호출 완료 시 카운터 감소
            if self.state == State.HALF_OPEN:
                self.half_open_calls -= 1

    def _success(self):
        """호출 성공: 카운터 리셋하고 정상 상태로"""
        print("✅ API 호출 성공!")
        self.failure_count = 0
        if self.state == State.HALF_OPEN:
            self.half_open_success_count += 1
        self._change_state(State.CLOSED)

    def _failure(self):
        """호출 실패: 카운터 증가하고 한계치 확인"""
        self.failure_count += 1
        self.last_failure_time = time.time()

        # HALF_OPEN에서 실패하면 즉시 OPEN으로
        if self.state == State.HALF_OPEN:
            print("❌ HALF_OPEN 테스트 실패")
            self._change_state(State.OPEN)
            return

        # CLOSED에서만 카운터 체크
        if self.failure_count >= self.failure_threshold:
            self._change_state(State.OPEN)

    def _change_state(self, new_state):
        """상태 변경 및 로깅"""
        if self.state != new_state:
            print(f"🔄 상태 변경: {self.state.name} → {new_state.name}")
            self.state = new_state


# 개선된 API - 시간이 지날수록 점점 안정화
def recovering_api():
    """복구되는 API 시뮬레이션"""
    import random

    # 전역 변수로 시작 시간 저장
    if not hasattr(recovering_api, "start_time"):
        recovering_api.start_time = time.time()

    elapsed = time.time() - recovering_api.start_time

    # 시간대별 실패율
    if elapsed < 5:
        failure_rate = 0.9  # 처음 5초: 90% 실패 (심각한 장애)
    elif elapsed < 15:
        failure_rate = 0.7  # 5-15초: 70% 실패 (여전히 불안정)
    elif elapsed < 25:
        failure_rate = 0.2  # 15-25초: 20% 실패 (복구 중)
    else:
        failure_rate = 0.05  # 25초 이후: 5% 실패 (거의 정상)

    print(f"    [API 상태: 실패율 {failure_rate*100:.0f}%]")

    if random.random() < failure_rate:
        raise Exception("API Error")
    return "API Success"


# 테스트 실행
print("=== API 복구 시나리오 테스트 ===")
print("0-5초: 90% 실패, 5-15초: 70% 실패, 15-25초: 20% 실패, 25초+: 5% 실패\n")

cb = CircuitBreaker(failure_threshold=3, timeout=8)

for i in range(35):
    try:
        result = cb.call(recovering_api)
        print(f"요청 {i:2d}: {result} (상태: {cb.state.name})")
    except CircuitBreakerOpenException as e:
        print(f"요청 {i:2d}: Circuit Breaker 차단 - {e} (상태: {cb.state.name})")
    except Exception as e:
        print(f"요청 {i:2d}: API 실패 - {e} (상태: {cb.state.name})")
    time.sleep(1)

print(f"\n최종 상태: {cb.state.name}")
