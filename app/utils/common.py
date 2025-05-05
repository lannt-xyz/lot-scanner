from datetime import datetime, timezone


def convert_datetime_to_utc(date_time: datetime):
  if date_time is None:
    return None

  if date_time.tzinfo is None:
    return date_time.replace(tzinfo=timezone.utc)
  
  return date_time.astimezone(timezone.utc)

def utcnow() -> datetime:
  return datetime.now(timezone.utc)
