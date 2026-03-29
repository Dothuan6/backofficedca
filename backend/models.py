import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship
import datetime

from database import Base

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, index=True)
    symbol = Column(String, index=True)
    initial_usd = Column(Float)
    dca_config = Column(JSON) # {"step_percent": 1.5, "multiplier": 1.5, "max_orders": 5}
    take_profit_percent = Column(Float)
    stop_loss_percent = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    rounds = relationship("Round", back_populates="strategy")

class Round(Base):
    __tablename__ = "rounds"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    strategy_id = Column(String, ForeignKey("strategies.id"))
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    status = Column(String, default="RUNNING") # RUNNING or COMPLETED
    total_invested = Column(Float, default=0.0)
    total_return = Column(Float, default=0.0)
    pnl = Column(Float, default=0.0)
    pnl_percent = Column(Float, default=0.0)
    current_dca_level = Column(Integer, default=0)

    strategy = relationship("Strategy", back_populates="rounds")
    orders = relationship("Order", back_populates="round")

class Order(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    round_id = Column(String, ForeignKey("rounds.id"))
    order_type = Column(String) # BUY or SELL
    price = Column(Float)
    quantity = Column(Float)
    usdt_value = Column(Float)
    executed_at = Column(DateTime, default=datetime.datetime.utcnow)

    round = relationship("Round", back_populates="orders")
