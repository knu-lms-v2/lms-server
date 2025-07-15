from datetime import datetime, timedelta,timezone

def is_due_within_7_days(due_dt):
    now = datetime.now(timezone.utc)
    end = now + timedelta(days=7)
    return now <= due_dt <= end

# 오늘
now = datetime.now(timezone.utc)
print(is_due_within_7_days(now))  # True

# 3일 뒤
in_3_days = now + timedelta(days=3)
print(is_due_within_7_days(in_3_days))  # True

# 7일 뒤
in_7_days = now + timedelta(days=7)
print(is_due_within_7_days(in_7_days))  # True

# 8일 뒤
in_8_days = now + timedelta(days=8)
print(is_due_within_7_days(in_8_days))  # False

# 1일 전(이미 마감)
yesterday = now - timedelta(days=1)
print(is_due_within_7_days(yesterday))  # False