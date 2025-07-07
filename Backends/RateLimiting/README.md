# Rate Limiting

[![CS Knowledge](https://img.shields.io/badge/CS-Backend-blue.svg)]()
[![Algorithm](https://img.shields.io/badge/Algorithm-Rate%20Limiting-green.svg)]()
[![Implementation](https://img.shields.io/badge/Implementation-Python%20%2B%20Redis-red.svg)]()

> **Rate Limiting의 핵심 알고리즘 3가지를 완전히 이해하고 직접 구현**

## 학습 동기

대규모 웹 서비스에서 필수적인 Rate Limiting 기술을 제대로 이해하기 위해서 각 알고리즘의 차이점, 실제 문제점을 확인해보았습니다.  


## 핵심 학습 내용

### Rate Limiting이란?

**"특정 시간 동안 허용되는 요청의 수를 제한하는 기술"**

#### 일상생활 비유로 이해하기
- **은행 창구**: "한 명당 하루에 5번까지만 업무 가능"
- **엘리베이터**: "최대 10명까지만 탑승 가능"  
- **카페**: "바리스타 1명, 1분에 커피 5잔까지만 제작 가능"

#### 왜 필요한가?
1. **서버 보호**: 과부하로 인한 다운 방지
2. **공정성**: 모든 사용자에게 균등한 기회 제공
3. **비용 관리**: 클라우드 리소스 사용량 제어
4. **남용 방지**: 스팸, DDoS 공격 차단

## 3가지 핵심 알고리즘 비교

### 1. Fixed Window (고정 윈도우)

#### 개념
시간을 **고정된 구간**으로 나누어 각 구간마다 요청 개수 제한

```
09:00:00~09:01:00 | 09:01:00~09:02:00 | 09:02:00~09:03:00
   최대 5개 요청   |    최대 5개 요청   |    최대 5개 요청
```

#### 핵심 로직
```python
# 윈도우 시작점 계산이 핵심!
current_time = int(time.time())  # 1698765432
window_seconds = 60
window_start = (current_time // window_seconds) * window_seconds
# 결과: 1698765420 (윈도우 시작 시간)

redis_key = f"fixed_window:{user_id}:{window_start}"
count = redis.incr(redis_key)  # 카운터 증가
```

#### 장단점
✅ **장점**: 구현 간단, 메모리 적게 씀, 빠름  
❌ **단점**: **윈도우 경계 문제** - 20초에 10개 요청 들어올 수 있음

#### 경계 문제 예시
```
09:00:50 → 5개 요청 (윈도우1에서 허용)
09:01:10 → 5개 요청 (윈도우2에서 허용)
실제 결과: 20초 안에 10개! → 서버 과부하 위험
```

### 2. Sliding Window (슬라이딩 윈도우)

#### 개념  
**현재 시점을 기준**으로 과거 일정 시간 동안의 요청 수 제한

```
현재 09:00:30 → 윈도우: 08:59:30 ~ 09:00:30
현재 09:00:50 → 윈도우: 08:59:50 ~ 09:00:50 (계속 움직임)
```

#### 핵심 로직
```python
# 모든 요청 시간을 기록해야 함!
current_time = time.time()
window_start = current_time - 60  # 1분 전

# Redis Sorted Set 사용
redis.zremrangebyscore(key, 0, window_start)  # 오래된 요청 제거
current_count = redis.zcard(key)  # 현재 요청 수
redis.zadd(key, {current_time: current_time})  # 새 요청 추가
```

#### 장단점
✅ **장점**: 정확한 제한, 경계 문제 완전 해결  
❌ **단점**: 구현 복잡, 메모리 많이 씀 (모든 요청 시간 저장)

#### 경계 문제 해결
```
09:00:50에 5개, 09:01:10에 5개 요청시:
→ 09:01:10 윈도우는 09:00:10~09:01:10
→ 이미 5개가 있으므로 새로운 5개는 거절! ✅
```

### 3. Token Bucket (토큰 버킷)

#### 개념
**토큰이 담긴 버킷**을 이용해 요청을 제어

```
🪣 버킷 크기: 5개 토큰
⏰ 충전 속도: 초당 1개
🎫 요청 시: 토큰 1개 소비
```

#### 핵심 로직
```python
# 토큰 충전 계산
elapsed = current_time - last_refill_time
new_tokens = min(capacity, current_tokens + elapsed * refill_rate)

# 토큰 있으면 허용, 없으면 거절
if new_tokens >= tokens_needed:
    remaining = new_tokens - tokens_needed
    return True  # 허용
else:
    return False  # 거절
```

#### 특별한 장점: 버스트 허용
```
평상시: 🪣 [●●●●●] (토큰 5개 축적)
갑자기 요청 몰림: 🪣 [_____] (모든 토큰 사용 가능!)
→ 일시적 버스트는 허용하되, 장기적으로는 제한
```

#### 장단점
✅ **장점**: 버스트 허용으로 사용자 경험 좋음, 유연함  
❌ **단점**: 순간적 과부하 가능성

## 핵심 깨달음

### 1. 알고리즘별 사용 시나리오

**Fixed Window**
- 🎯 **언제**: 단순한 제한, 높은 성능 필요
- 📝 **예시**: 로그인 시도 제한, 단순 API
- ⚠️ **주의**: 경계에서 burst 발생 가능

**Sliding Window**
- 🎯 **언제**: 정확한 제한 필요, 보안 중요
- 📝 **예시**: 결제 API, 중요한 업무 API
- ⚠️ **주의**: 메모리 사용량 고려

**Token Bucket**
- 🎯 **언제**: 유연한 패턴, 버스트 허용 필요
- 📝 **예시**: LLM API, 파일 업로드, 스트리밍
- ⚠️ **주의**: 순간 과부하 가능성

### 2. 실제 구현에서 중요한 점

#### Redis + Lua 스크립트 필수
```python
# 여러 Redis 명령어를 하나로 묶어 원자적 연산 보장
lua_script = """
redis.call('ZREMRANGEBYSCORE', key, 0, window_start)
local count = redis.call('ZCARD', key)
if count >= limit then return 0 end
redis.call('ZADD', key, current_time, current_time)
return 1
"""
```
**Why?** 동시에 여러 요청이 와도 정확한 계산 보장

#### 알고리즘별 메모리 사용량
```
Fixed Window: key → 숫자 (4바이트)
Sliding Window: key → 모든 요청 시간들 (시간 * 8바이트)  
Token Bucket: key → {tokens, last_refill} (16바이트)
```

### 3. 실무에서의 트레이드오프

| 기준 | Fixed Window | Sliding Window | Token Bucket |
|------|-------------|----------------|--------------|
| **구현 난이도** | 쉬움 | 어려움 | 보통 |
| **정확성** | 낮음 | 높음 | 보통 |
| **메모리** | 적음 | 많음 | 적음 |
| **사용자 경험** | 나쁨 | 예측가능 | 좋음 |

## 실제 테스트 결과

### 연속 요청 테스트 (5개 제한에 6개 요청)
```
모든 알고리즘: [✅✅✅✅✅❌] 동일한 결과
```

### 시간 경과 후 테스트 (3초 후 요청)
```
Fixed Window:    ❌ (같은 윈도우 내라서 거절)
Sliding Window:  ✅ (일부 요청이 윈도우에서 제거됨)
Token Bucket:    ✅ (토큰 3개 충전됨)
```

### 경계 문제 테스트
```
시나리오: 윈도우 끝에 5개, 윈도우 시작에 5개

Fixed Window:    💥 "20초에 10개 허용" (문제!)
Sliding Window:  ✅ "정확히 1분에 5개만"
Token Bucket:    ✅ "버스트는 허용하되 평균 제한"
```

## 학습 과정에서 겪은 어려움

### 1. 윈도우 시작점 계산 이해
처음에는 단순히 `time.time() - 60`으로 생각했는데, Fixed Window에서는 **정확한 구간 경계**를 계산해야 한다는 걸 깨달음.

### 2. Redis 동시성 문제
여러 요청이 동시에 오면 카운터가 정확하지 않게 계산되는 문제. **Lua 스크립트**로 해결해야 함을 이해.

### 3. 각 알고리즘의 트레이드오프
처음엔 "정확한 게 무조건 좋다"고 생각했는데, 실제로는 **상황에 맞는 선택**이 더 중요함을 깨달음.

## 실제 서비스에 적용한다면?

### 단계적 접근법
1. **1단계**: Fixed Window로 빠르게 시작 (학습 + 기본 보호)
2. **2단계**: 문제 발생시 Sliding Window로 업그레이드  
3. **3단계**: 사용자 경험 개선을 위해 Token Bucket 도입
4. **4단계**: 서비스별 하이브리드 조합

### 하이브리드 예시
```
로그인 실패: Fixed Window (단순, 강력)
결제 API: Sliding Window (정확성 중요)  
파일 업로드: Token Bucket (버스트 허용)
```

## 핵심 인사이트

> **"모든 자원은 유한하다."**  
> Rate Limiting은 제한된 자원을 **공정하고 안전하게** 분배하는 핵심 기술
