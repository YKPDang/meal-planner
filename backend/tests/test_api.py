from datetime import date, timedelta

from fastapi.testclient import TestClient

import main


def setup_module() -> None:
    main.DB_PATH = main.Path("/tmp/meal_planner_test.db")
    if main.DB_PATH.exists():
        main.DB_PATH.unlink()
    main.init_db()


def test_recipe_crud_and_tags() -> None:
    client = TestClient(main.app)

    create_response = client.post(
        "/recipes",
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

    list_response = client.get("/recipes")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1


def test_meal_plan_random_modes() -> None:
    client = TestClient(main.app)
    today = date.today()

    second_recipe = client.post(
        "/recipes",
        json={
            "name": "Rice Bowl",
            "description": "Dinner",
            "ingredients": [{"unit": "1 cup", "item": "rice"}],
            "tags": ["quick-lunch"],
        },
    )
    assert second_recipe.status_code == 201

    day = today.isoformat()
    random_response = client.post(f"/meal-plan/{day}/random", json={"mode": "random"})
    assert random_response.status_code == 200
    assert random_response.json()["recipe"]["id"]

    filtered_response = client.post(
        f"/meal-plan/{(today + timedelta(days=1)).isoformat()}/random",
        json={"mode": "filtered", "tags": ["pasta"]},
    )
    assert filtered_response.status_code == 200
    assert "pasta" in filtered_response.json()["recipe"]["tags"]

    smart_response = client.post(
        f"/meal-plan/{(today + timedelta(days=2)).isoformat()}/random",
        json={"mode": "smart", "lookback_days": 1},
    )
    assert smart_response.status_code == 200
