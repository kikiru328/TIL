# test_burst_traffic.py
import time
import threading
from typing import Any
import sys
sys.path.append("../")
from rate_limiters.no_limit import NoLimitRateLimiter



def simulate_heavy_request() -> int:
    """CPU 집약적인 무거운 연산을 시뮬레이션"""
    result: int = 0
    for i in range(1_000_000):  # 백만 번 계산
        result += i * i
    return result


def burst_attack(limiter: NoLimitRateLimiter, ip: str, num_requests: int) -> None:
    """Burst Traffic 공격 시뮬레이션
    
    Args:
        limiter (NoLimitRateLimiter): 레이트 리미터 인스턴스
        ip (str): 요청 IP 주소
        num_requests (int): 요청 횟수
    """
    print(f"{ip}에서 {num_requests}개 요청 시작!")
    start_time: float = time.time()
    
    for i in range(num_requests):
        result: dict[str, Any] = limiter.is_allowed(ip)

        if result.get('allowed', False):
            simulate_heavy_request()
            print(f"  요청 {i + 1} 처리 완료")
        else:
            print(f"  요청 {i + 1} 거절됨")

    end_time: float = time.time()
    elapsed: float = end_time - start_time
    print(f"{ip} 완료! 총 시간: {elapsed:.2f}초")


def main() -> None:
    """NoLimitRateLimiter를 이용한 Burst 트래픽 테스트 실행"""
    limiter = NoLimitRateLimiter()

    print("=== No Limit에서 Burst Traffic 테스트 ===")
    print("경고: 서버에 부하가 몰릴 예정!\n")

    threads: list[threading.Thread] = []

    for i in range(3):  # 3개 IP에서 동시 공격
        ip = f"192.168.1.{100 + i}"
        thread = threading.Thread(target=burst_attack, args=(limiter, ip, 5))
        threads.append(thread)

    start_total: float = time.time()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_total: float = time.time()
    total_elapsed: float = end_total - start_total
    print(f"\n전체 완료! 총 시간: {total_elapsed:.2f}초")
    print("문제점: 모든 요청이 동시에 처리되어 서버 과부하!")


if __name__ == "__main__":
    main()
