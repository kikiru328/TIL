# 설치: pip install pybreaker
from pybreaker import CircuitBreaker

# 간단한 설정
db = CircuitBreaker(fail_max=5, reset_timeout=30)


@db  # 데코레이터로 적용
def call_payment_api(amount):
    # 실제 API 호출
    response = requests.post("/api/payment", {"amount": amount})
    return response.json()


# 사용
try:
    result = call_payment_api(1000)
    print(f"결제 성공: {result}")
except CircuitBreakerError:
    print("결제 서비스 일시 중단")
