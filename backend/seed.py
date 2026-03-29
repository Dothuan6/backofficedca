import random
from datetime import datetime, timedelta
import uuid

import database, models

def seed_data():
    database.Base.metadata.drop_all(bind=database.engine)
    database.Base.metadata.create_all(bind=database.engine)
    
    db = database.SessionLocal()
    
    # Create Strategy
    strategy = models.Strategy(
        id=str(uuid.uuid4()),
        name="BNB Safety Ladder",
        symbol="BNBUSDT",
        initial_usd=1000.0,
        dca_config={"step_percent": 1.5, "multiplier": 1.5, "max_orders": 5},
        take_profit_percent=1.2,
        stop_loss_percent=0.0
    )
    db.add(strategy)
    db.commit()

    # Create dummy rounds
    for i in range(10):
        is_completed = random.choice([True, True, True, False])
        pnl = random.uniform(-10.0, 30.0) if is_completed else 0.0
        r = models.Round(
            id=str(uuid.uuid4()),
            strategy_id=strategy.id,
            start_time=datetime.utcnow() - timedelta(hours=random.randint(1, 100)),
            status="COMPLETED" if is_completed else "RUNNING",
            total_invested=random.uniform(50, 500),
            pnl=pnl,
            pnl_percent=random.uniform(-1.0, 5.0) if is_completed else 0.0
        )
        if is_completed:
            r.end_time = r.start_time + timedelta(hours=random.randint(1, 24))
            
        db.add(r)
        
    db.commit()
    print("Database seeded with sample Strategy and Rounds.")

if __name__ == "__main__":
    seed_data()
