import time
import redis

client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def check_rate_limit(ip_address: str) -> bool:
  current_minute = int(time.time() // 60)
  key = f"rate_limit:{ip_address}:minute_{current_minute}"

  current_count: typing.TypeVar = client.incr(key)

  if current_count == 1:
    client.expire(key, 60)

  if current_count > 5:
    return False

  return True



test_ip = "192.168.1.1"
current_minute = int(time.time() // 60)
client.delete(f"rate_limit:{test_ip}:minute_{current_minute}")

for i in range(1, 11):
    result = check_rate_limit(test_ip)
    print(f"Запрос {i}: {'Разрешен (True)' if result else 'Заблокирован (False)'}")