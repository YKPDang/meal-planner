from datetime import date, timedelta

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient

from backend import main


def setup_module() -> None:
    main.config.DB_PATH = main.config.Path("/tmp/meal_planner_test.db")
    if main.config.DB_PATH.exists():
        main.config.DB_PATH.unlink()
    from backend.app.db import init_db

    init_db()


def test_recipe_crud_and_tags() -> None:
    client = TestClient(main.app)

    create_response = client.post(
        "/api/recipes",
        json={
            "name": "Pasta Salad",
            "description": "Quick lunch",
            "ingredients": [
                {"unit": "200g", "item": "pasta"},
                {"unit": "1", "item": "tomato"},
            ],
            "tags": ["pasta", "quick-lunch"],
        },
    )
    assert create_response.status_code == 201
    payload = create_response.json()
    assert payload["name"] == "Pasta Salad"
    assert set(payload["tags"]) == {"pasta", "quick-lunch"}

    list_response = client.get("/api/recipes")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_meal_plan_random_modes() -> None:
    client = TestClient(main.app)
    today = date.today()

    second_recipe = client.post(
        "/api/recipes",
        json={
            "name": "Rice Bowl",
            "description": "Dinner",
            "ingredients": [{"unit": "1 cup", "item": "rice"}],
            "tags": ["quick-lunch"],
        },
    )
    assert second_recipe.status_code == 201

    day = today.isoformat()
    random_response = client.post(f"/api/meal-plan/{day}/random", json={"mode": "random"})
    assert random_response.status_code == 200
    assert random_response.json()["recipe"]["id"]

    filtered_response = client.post(
        f"/api/meal-plan/{(today + timedelta(days=1)).isoformat()}/random",
        json={"mode": "filtered", "tags": ["pasta"]},
    )
    assert filtered_response.status_code == 200
    assert "pasta" in filtered_response.json()["recipe"]["tags"]

    smart_response = client.post(
        f"/api/meal-plan/{(today + timedelta(days=2)).isoformat()}/random",
        json={"mode": "smart", "lookback_days": 1},
    )
    assert smart_response.status_code == 200
