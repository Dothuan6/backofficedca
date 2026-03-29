from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class DCAConfig(BaseModel):
    step_percent: float
    multiplier: float
    max_orders: int

class StrategyBase(BaseModel):
    name: str
    symbol: str
    initial_usd: float
    dca_config: DCAConfig
    take_profit_percent: float
    stop_loss_percent: float

class StrategyCreate(StrategyBase):
    pass

class Strategy(StrategyBase):
    id: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    order_type: str
    price: float
    quantity: float
    usdt_value: float

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: str
    round_id: str
    executed_at: datetime
    model_config = ConfigDict(from_attributes=True)

class RoundBase(BaseModel):
    status: str
    total_invested: float
    total_return: float
    pnl: float
    pnl_percent: float
    current_dca_level: int

class Round(RoundBase):
    id: str
    strategy_id: str
    start_time: datetime
    end_time: Optional[datetime] = None
    orders: List[Order] = []
    model_config = ConfigDict(from_attributes=True)
