import os
from pathlib import Path


DB_PATH = Path(os.getenv("DATABASE_PATH", "/data/meal_planner.db"))
SMART_RANDOM_LOOKBACK_DAYS = int(os.getenv("SMART_RANDOM_LOOKBACK_DAYS", "7"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
