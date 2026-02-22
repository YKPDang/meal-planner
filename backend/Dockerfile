FROM python:3.12-slim

WORKDIR /repo
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend

ENV DATABASE_PATH=/data/meal_planner.db
ENV PYTHONPATH=/repo
EXPOSE 8000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
