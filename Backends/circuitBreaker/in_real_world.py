import time
import random
from enum import Enum


class PaymentError(Exception):
    def __init__(self, error_type, message):
        self.error_type = error_type
        super().__init__(message)


class ErrorType(Enum):
    TIMEOUT = "timeout"
    SERVER_ERROR = "server_error"
    VALIDATION_ERROR = "validation_error"
    NETWORK_ERROR = "network_error"


class State(Enum):
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    HALF_OPEN = "HALF_OPEN"


class PaymentCircuitBreaker:
    def __init__(self):
        self.state = State.CLOSED
        self.failure_count = 0
        self.last_failure_time = 0
        self.test_call_count = 0
        self.concurrent_test_calls = 0
        self.start_time = time.time()  # 시작 시간을 인스턴스 변수로

        # 설정값
        self.failure_threshold = 3
        self.timeout = 15  # 15초로 단축 (테스트 편의)
        self.max_test_calls = 2  # HALF_OPEN에서 최대 2번만 테스트

    def process_payment(self, amount, card_number):
        """결제 처리"""

        # OPEN 상태: 결제 API 장애 중
        if self.state == State.OPEN:
            if time.time() - self.last_failure_time > self.timeout:
                self._change_state(State.HALF_OPEN)
                self.test_call_count = 0
                self.concurrent_test_calls = 0  # 리셋 추가
                print("🟡 결제 시스템 복구 테스트 시작")
            else:
                print("🔴 결제 시스템 장애 - 현금결제나 다른 카드를 이용해주세요")
                raise PaymentError(ErrorType.SERVER_ERROR, "결제 서비스 일시 중단")

        # HALF_OPEN 상태: 제한된 테스트만 허용
        if self.state == State.HALF_OPEN:
            if self.test_call_count >= self.max_test_calls:
                print("🟡 복구 테스트 진행 중 - 잠시 후 다시 시도해주세요")
                raise PaymentError(ErrorType.SERVER_ERROR, "복구 테스트 중")

            if self.concurrent_test_calls > 0:
                print("🟡 다른 결제 테스트 진행 중")
                raise PaymentError(ErrorType.SERVER_ERROR, "복구 테스트 중")

            self.test_call_count += 1
            self.concurrent_test_calls += 1

        try:
            print(f"💳 결제 API 호출: {amount}원 (상태: {self.state.value})")

            # 실제 결제 API 호출 시뮬레이션
            result = self._call_payment_api(amount, card_number)

            # 성공 처리
            self._on_success()
            return result

        except PaymentError as e:
            # 실패 처리 (에러 타입별로 다르게)
            self._on_failure(e)
            raise e
        finally:
            if self.state == State.HALF_OPEN:
                self.concurrent_test_calls -= 1

    def _call_payment_api(self, amount, card_number):
        """외부 결제 API 시뮬레이션 - 시간이 지날수록 안정화"""

        elapsed = time.time() - self.start_time

        # 잘못된 카드번호는 항상 실패
        if len(card_number) < 16:
            raise PaymentError(ErrorType.VALIDATION_ERROR, "잘못된 카드번호")

        # 시간대별 실패율 (점진적 회복)
        if elapsed < 10:
            error_rate = 0.8  # 처음 10초: 80% 실패
        elif elapsed < 20:
            error_rate = 0.4  # 10-20초: 40% 실패
        else:
            error_rate = 0.1  # 20초 후: 10% 실패

        print(
            f"    [API 상태: 장애율 {error_rate*100:.0f}%, 경과시간: {elapsed:.1f}초]"
        )

        if random.random() < error_rate:
            error_type = random.choice(
                [ErrorType.TIMEOUT, ErrorType.SERVER_ERROR, ErrorType.NETWORK_ERROR]
            )

            if error_type == ErrorType.TIMEOUT:
                time.sleep(0.1)
                raise PaymentError(error_type, "결제 API 응답 없음")
            elif error_type == ErrorType.SERVER_ERROR:
                raise PaymentError(error_type, "결제 서버 내부 오류")
            else:
                raise PaymentError(error_type, "네트워크 연결 실패")

        # 성공
        return f"결제 완료: {amount}원"

    def _on_success(self):
        """결제 성공 시"""
        print("✅ 결제 성공!")
        self.failure_count = 0
        self._change_state(State.CLOSED)
        self.test_call_count = 0

    def _on_failure(self, error):
        """결제 실패 시 - 에러 타입별 다른 처리"""
        print(f"❌ 결제 실패: {error}")

        # 검증 에러는 우리 시스템 문제이므로 Circuit Breaker와 무관
        if error.error_type == ErrorType.VALIDATION_ERROR:
            print("   → 사용자 입력 오류 (실패 카운트 제외)")
            return

        # HALF_OPEN에서 실패하면 즉시 OPEN
        if self.state == State.HALF_OPEN:
            print("🔴 복구 테스트 실패 - 결제 시스템 다시 차단")
            self._change_state(State.OPEN)
            self.last_failure_time = time.time()
            self.test_call_count = 0
            return

        # CLOSED에서 실패 카운트 증가
        self.failure_count += 1
        self.last_failure_time = time.time()

        print(f"   → 실패 카운트: {self.failure_count}/{self.failure_threshold}")

        # 네트워크 에러나 서버 에러가 연속으로 발생하면 즉시 OPEN
        if error.error_type in [
            ErrorType.NETWORK_ERROR,
            ErrorType.SERVER_ERROR,
            ErrorType.TIMEOUT,
        ]:
            if self.failure_count >= self.failure_threshold:
                self._change_state(State.OPEN)
                print(f"🔴 결제 시스템 차단 - {self.timeout}초 후 복구 테스트")

    def _change_state(self, new_state):
        """상태 변경 및 로깅"""
        if self.state != new_state:
            print(f"🔄 상태 변경: {self.state.value} → {new_state.value}")
            self.state = new_state


# 실제 사용 시뮬레이션
def simulate_shopping_mall():
    cb = PaymentCircuitBreaker()

    # 고객들의 결제 시도 (더 많은 시나리오)
    payments = [
        (50000, "1234567890123456"),
        (25000, "1234567890123456"),
        (75000, "1234567890123456"),
        (30000, "123456"),  # 잘못된 카드번호
        (40000, "1234567890123456"),
        (60000, "1234567890123456"),
        (35000, "1234567890123456"),
        (80000, "1234567890123456"),
        (45000, "1234567890123456"),
        (55000, "1234567890123456"),
        (20000, "1234567890123456"),
        (90000, "1234567890123456"),
        (65000, "1234567890123456"),
        (15000, "1234567890123456"),
        (70000, "1234567890123456"),
    ]

    print("=== 온라인 쇼핑몰 결제 시나리오 ===")
    print("0-10초: 80% 장애, 10-20초: 40% 장애, 20초+: 10% 장애\n")

    for i, (amount, card) in enumerate(payments, 1):
        print(f"\n=== 고객 {i} 결제 시도 ===")
        try:
            result = cb.process_payment(amount, card)
            print(f"고객에게 표시: {result}")
        except PaymentError as e:
            print(f"고객에게 표시: 결제 실패 - {e}")

        time.sleep(2)  # 결제 간격

    print(f"\n최종 상태: {cb.state.value}")


# 실행
if __name__ == "__main__":
    simulate_shopping_mall()
