from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.db.entities import Base

class CodeMaster(Base):
    __tablename__ = "code_master"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_code = Column(String)
    group_name = Column(String)
    code_value = Column(String)
    code_name1 = Column(String)
    code_name2 = Column(String)
    display_order = Column(Integer)
    is_deleted = Column(Boolean, default=False)
    created_by = Column(String)
    updated_by = Column(String)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
