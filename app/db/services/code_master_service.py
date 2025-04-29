from typing import List
from sqlmodel import and_, select

from app.db import SessionDep
from app.db.entities.code_master import CodeMaster

from app.models.select_option import SelectOption

class CodeMasterService:
    def __init__(self, db: SessionDep):
        self.db = db
        pass

    def get_by_group_code(self, group_code: str) -> List[SelectOption]:
        """
        Fetches all key/value pairs associated with a specific group code.

        Args:
            group_code (str): The group code to filter channels.

        Returns:
            list: A list of key/value pairs associated with the provided group code.
        """
        result = (
            self.db.exec(
                select(
                    CodeMaster.code_value.label("key"),
                    CodeMaster.code_name1.label("value"),
                    CodeMaster.display_order
                ).where(and_(
                    CodeMaster.group_code == group_code,
                    CodeMaster.is_deleted.is_(False),
                )).order_by(CodeMaster.display_order)
            )
            .all()
        )
        return [
            SelectOption(**item._asdict())
            for item in result
        ]