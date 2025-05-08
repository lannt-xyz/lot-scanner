from cv2 import exp
from sqlalchemy import Column, BigInteger, String, Enum, DateTime
from app.db.entities import Base
from app.db.entities.audit_mixin import AuditMixin

class AdReward(Base, AuditMixin):
    __tablename__ = "ad_reward"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(String(255), nullable=True)
    guest_id = Column(String(255), nullable=True)
    reward_token = Column(String(255), unique=True, nullable=False)
    ad_network = Column(String(50), default="admob")
    status = Column(String(1), default="0")
    claimed_at = Column(DateTime, nullable=True)
    expired_at = Column(DateTime, nullable=True)
