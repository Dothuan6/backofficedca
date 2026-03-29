from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import List

import models
import schemas
import database

# engine has been imported in database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Crypto Bot Backoffice API")

# Setup CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/v1/strategies", response_model=List[schemas.Strategy])
def read_strategies(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    strategies = db.query(models.Strategy).offset(skip).limit(limit).all()
    return strategies

@app.post("/api/v1/strategies", response_model=schemas.Strategy)
def create_strategy(strategy: schemas.StrategyCreate, db: Session = Depends(database.get_db)):
    dca_config_dict = strategy.dca_config.model_dump()
    db_strategy = models.Strategy(
        name=strategy.name,
        symbol=strategy.symbol,
        initial_usd=strategy.initial_usd,
        dca_config=dca_config_dict,
        take_profit_percent=strategy.take_profit_percent,
        stop_loss_percent=strategy.stop_loss_percent
    )
    db.add(db_strategy)
    db.commit()
    db.refresh(db_strategy)
    return db_strategy

@app.get("/api/v1/rounds", response_model=List[schemas.Round])
def read_rounds(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    rounds = db.query(models.Round).offset(skip).limit(limit).all()
    return rounds

@app.get("/api/v1/analytics/dashboard")
def get_dashboard_analytics(db: Session = Depends(database.get_db)):
    rounds = db.query(models.Round).all()
    total_pnl = sum([r.pnl for r in rounds])
    completed_rounds = [r for r in rounds if r.status == "COMPLETED"]
    active_rounds = [r for r in rounds if r.status == "RUNNING"]
    win_rate = (len([r for r in completed_rounds if r.pnl > 0]) / len(completed_rounds) * 100) if len(completed_rounds) > 0 else 0
    
    return {
        "total_pnl": total_pnl,
        "active_rounds": len(active_rounds),
        "completed_rounds": len(completed_rounds),
        "win_rate": round(win_rate, 2),
        "avg_profit_per_round": round(total_pnl / len(completed_rounds) if len(completed_rounds) > 0 else 0, 2)
    }

# Endpoint for Recommendation Simulation Engine Output
@app.post("/api/v1/engines/recommend")
def recommend_strategy(strategy_id: str, db: Session = Depends(database.get_db)):
    # Mocking recommendation engine output based on the architecture plan
    return {
        "strategy_id": strategy_id,
        "recommendations": [
            {
                "config_suggestion": {
                    "dca_step_percent": { "from": 2.0, "to": 1.5 },
                    "multiplier": { "from": 1.5, "to": 1.8 },
                    "take_profit_percent": { "from": 1.0, "to": 1.2 }
                },
                "reasoning": [
                    "Current strategy misses optimal averaging zone (avg depth utilized is only 1.2 / 5 orders).",
                    "Profit exits too early given current asset volatility.",
                    "Drawdown recovery is strong (low risk); optimizing profit taking is mathematically safe."
                ],
                "expected_result_simulation": {
                    "pnl_increase_percent": 12.4,
                    "max_drawdown_increase_percent": 4.8,
                    "winrate_percent": { "from": 68.5, "to": 74.2 }
                }
            }
        ]
    }

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Bot API Running"}
