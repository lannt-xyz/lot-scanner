from datetime import datetime, timezone

from app.utils.constants import TICKET_RESULT_DATA


def convert_datetime_to_utc(date_time: datetime):
  if date_time is None:
    return None

  if date_time.tzinfo is None:
    return date_time.replace(tzinfo=timezone.utc)
  
  return date_time.astimezone(timezone.utc)

def utcnow() -> datetime:
  return datetime.now(timezone.utc)

def get_ticket_result(result: int):
    # Use a list comprehension to find the matching ticket result
    matching_results = [x for x in TICKET_RESULT_DATA if x["prize"] == result]
    return matching_results[0] if matching_results else None
