
import re

from datetime import datetime
from typing import List

from app.modules.kqxs.errors import IncorrectResultException
from app.modules.kqxs.models import PrizeStructure
from app.modules.kqxs.provider.xsbd import XSBD
from app.modules.kqxs.provider.kqxsvn import KQXSVN

prize_structures: List[PrizeStructure] = [
    PrizeStructure(name="giai-tam", amount=1, length=2),
    PrizeStructure(name="giai-bay", amount=1, length=3),
    PrizeStructure(name="giai-sau", amount=3, length=4),
    PrizeStructure(name="giai-nam", amount=1, length=4),
    PrizeStructure(name="giai-tu", amount=7, length=5),
    PrizeStructure(name="giai-ba", amount=2, length=5),
    PrizeStructure(name="giai-nhi", amount=1, length=5),
    PrizeStructure(name="giai-nhat", amount=1, length=5),
    PrizeStructure(name="giai-dac-biet", amount=1, length=6),
]

def get_prize_structure(prize_code: str) -> PrizeStructure:
    """
    Get prize structure by prize code
    :param prize_code: prize code
    :return: prize structure
    """
    return next((x for x in prize_structures if x.name == prize_code), None)

class ScanClient:
  def _validate_result(self, result):
    if not result:
      raise IncorrectResultException("No result found")
    if not isinstance(result, dict):
      raise IncorrectResultException("Invalid result format")
    # get all keys in result
    keys = result.keys()
    if not keys:
      raise IncorrectResultException("Empty result")
    # check each key in result, get prize_code and it's value
    for city_code in keys:
      for prize_code in result[city_code]:
        if not isinstance(prize_code, str):
          raise IncorrectResultException("Invalid prize value format")
        prize_numbers = result[city_code][prize_code]
        if not isinstance(prize_numbers, list):
          raise IncorrectResultException("Invalid prize value format")
        # get prize structure based on prize_code
        prize_structure = get_prize_structure(prize_code)
        if not prize_structure:
          raise IncorrectResultException("Invalid prize code")
        # check prize_numbers size
        if len(prize_numbers) != prize_structure.amount:
          raise IncorrectResultException("Invalid prize number size")
        # check each prize number length
        for prize_number in prize_numbers:
          if not isinstance(prize_number, str) or not re.match(r'^\d+$', prize_number):
            raise IncorrectResultException("Invalid prize number format")
          if len(prize_number) != prize_structure.length:
            raise IncorrectResultException("Invalid prize number length")

    return result

  def scan(self, prizeDate: datetime):
    # first try to crawl from XSBD
    # if it fails, try to crawl from KQXSVN
    result = None
    error = None

    xsvnvn = KQXSVN()
    try:
      result = self._validate_result(xsvnvn.craw(prizeDate))
    except IncorrectResultException as e:
      error = e
      print(f"KQXSVN Error: {error}")

    if result is None:
      xsbd = XSBD()
      try:
        result = self._validate_result(xsbd.craw(prizeDate))
      except IncorrectResultException as e:
        error = e
        print(f"XSBD Error: {error}")

    return result
