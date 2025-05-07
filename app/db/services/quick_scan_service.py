from datetime import datetime

from app.db import SessionDep
from app.db.services.code_master_service import CodeMasterService
from app.models.ticket_model import TicketModel, TicketResponseModel
from app.modules.kqxs.models import PrizeStructure
from app.modules.kqxs.scan_client import ScanClient, get_prize_structure
from app.utils.common import get_ticket_result_by_code
from app.utils.constants import CONSOLATION_PRIZE_CODE, GROUP_CODES_CHANNELS, NON_MATCH_CODE, SPECIAL_CONSOLATION_PRIZE_CODE, SPECIAL_PRIZE_CODE

class QuickScanService:
    def __init__(self, db: SessionDep):
        self.db = db
        pass

    def _check(self, prize_number: str, channel_result) -> bool:
        # Check if the prize_number matches any prize
        matched_prize_code = NON_MATCH_CODE
        for prize_code, prize_numbers in channel_result.items():
            # First check the additional prize numbers
            if prize_code == SPECIAL_PRIZE_CODE:
                ticket_last_five = prize_number[-5:]
                result_last_five = prize_numbers[0][-5:]

                # if the last five number of ticket.prize_number matched with last file number of prize_numbers[0]
                if ticket_last_five == result_last_five:
                    matched_prize_code = SPECIAL_CONSOLATION_PRIZE_CODE
                
                # fist digit must be the same but the last five number only allow for different 1 digit in any position
                ticket_first_digit = prize_number[0]
                result_first_digit = prize_numbers[0][0]
                diff_count = sum(1 for a, b in zip(ticket_last_five, result_last_five) if a != b)
                if diff_count == 1 and ticket_first_digit == result_first_digit:
                    matched_prize_code = CONSOLATION_PRIZE_CODE

            # extract the last n digits of the prize_number based on the prize_config
            prize_structure: PrizeStructure = get_prize_structure(prize_code)
            if prize_structure is None:
                continue
            correcting_prize_numbers = prize_number[-prize_structure.length:]
            # Check if the prize_number is in the list of prize numbers
            if correcting_prize_numbers in prize_numbers:
                matched_prize_code = prize_code
                break
        return matched_prize_code

    def scan(self, ticket: TicketModel) -> TicketResponseModel:
        """
        Scans a ticket and returns the result.

        Args:
            ticket (TicketModel): The ticket object to be scanned.

        Returns:
            TicketResponseModel: The scanned ticket response model.
        """
        if not ticket:
            raise ValueError("Ticket cannot be None")

        if ticket.prize_date is None or ticket.prize_number is None or ticket.channel is None:
            raise ValueError("Prize date, channel, number must be provided")
        
        current_datetime = datetime.now()
        limit_date_time = datetime(current_datetime.year, current_datetime.month, current_datetime.day, 16, 30)

        result = get_ticket_result_by_code(NON_MATCH_CODE)
        # if prize_date is early than current date
        # if prize_date is same as current date and current time is greater than 16:30
        if ticket.prize_date < limit_date_time.date() or current_datetime >= limit_date_time:
            code_mater = CodeMasterService(self.db)
            channel = code_mater.find_by_code(GROUP_CODES_CHANNELS, ticket.channel).code_name2

            scan_client = ScanClient()
            scan_result = scan_client.scan(ticket.prize_date)
            if channel not in scan_result:
                raise ValueError("Channel not found in scan result")

            channel_result = scan_result[channel]
            matched_prize_code = self._check(ticket.prize_number, channel_result)

            if matched_prize_code is not None:
                result = get_ticket_result_by_code(matched_prize_code)

        return TicketResponseModel(
            id=None,
            channel=ticket.channel,
            prize_date=ticket.prize_date,
            prize_number=ticket.prize_number,
            prize_amount=result['amount'] if result else None,
            result=result['message'] if result else None,
        )
