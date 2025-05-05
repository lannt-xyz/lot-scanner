from sqlalchemy import Column, Integer, String, DateTime, Boolean

from app.db.entities import Base
from app.db.entities.audit_mixin import AuditMixin

class CodeMaster(Base, AuditMixin):
    __tablename__ = "code_master"

    id = Column(Integer, primary_key=True, autoincrement=True)
    group_code = Column(String(10))
    group_name = Column(String(255))
    code_value = Column(String(10))
    code_name1 = Column(String(255))
    code_name2 = Column(String(255))
    display_order = Column(Integer)
