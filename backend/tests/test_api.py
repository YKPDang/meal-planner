from datetime import date, timedelta

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from fastapi.testclient import TestClient

from backend import main


def reset_db() -> None:
    main.config.DB_PATH = main.config.Path("/tmp/meal_planner_test.db")
    if main.config.DB_PATH.exists():
        main.config.DB_PATH.unlink()
    from backend.app.db import init_db

    init_db()


def setup_module() -> None:
    reset_db()


def setup_function() -> None:
    reset_db()


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

    pasta_recipe = client.post(
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
    assert pasta_recipe.status_code == 201

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


def test_smart_random_avoids_recent_recipe() -> None:
    client = TestClient(main.app)
    today = date.today()

    first = client.post(
        "/api/recipes",
        json={
            "name": "Stew",
            "description": "Hearty dinner",
            "ingredients": [{"unit": "2 cups", "item": "beans"}],
            "tags": ["dinner"],
        },
    )
    assert first.status_code == 201
    first_id = first.json()["id"]

    second = client.post(
        "/api/recipes",
        json={
            "name": "Salad",
            "description": "Light lunch",
            "ingredients": [{"unit": "1", "item": "lettuce"}],
            "tags": ["lunch"],
        },
    )
    assert second.status_code == 201

    # Assign the first recipe to yesterday so smart random should avoid it.
    yesterday = (today - timedelta(days=1)).isoformat()
    assign_response = client.put(f"/api/meal-plan/{yesterday}", json={"recipe_id": first_id})
    assert assign_response.status_code == 200

    smart_response = client.post(
        f"/api/meal-plan/{today.isoformat()}/random",
        json={"mode": "smart", "lookback_days": 7},
    )
    assert smart_response.status_code == 200
    assert smart_response.json()["recipe"]["id"] != first_id


def test_filtered_random_requires_tags_and_filters() -> None:
    client = TestClient(main.app)
    today = date.today()

    pasta = client.post(
        "/api/recipes",
        json={
            "name": "Tagliatelle",
            "description": "Quick pasta",
            "ingredients": [{"unit": "200g", "item": "pasta"}],
            "tags": ["pasta"],
        },
    )
    assert pasta.status_code == 201

    soup = client.post(
        "/api/recipes",
        json={
            "name": "Soup",
            "description": "Warm bowl",
            "ingredients": [{"unit": "1 cup", "item": "broth"}],
            "tags": ["soup"],
        },
    )
    assert soup.status_code == 201

    missing_tags = client.post(
        f"/api/meal-plan/{today.isoformat()}/random",
        json={"mode": "filtered", "tags": []},
    )
    assert missing_tags.status_code == 400

    filtered = client.post(
        f"/api/meal-plan/{(today + timedelta(days=1)).isoformat()}/random",
        json={"mode": "filtered", "tags": ["pasta"]},
    )
    assert filtered.status_code == 200
    assert "pasta" in filtered.json()["recipe"]["tags"]


def test_health_check() -> None:
    client = TestClient(main.app)
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_assign_and_clear_meal_plan_day() -> None:
    client = TestClient(main.app)
    today = date.today().isoformat()

    created = client.post(
        "/api/recipes",
        json={
            "name": "Toast",
            "description": "Simple breakfast",
            "ingredients": [{"unit": "2", "item": "bread"}],
            "tags": ["breakfast"],
        },
    )
    assert created.status_code == 201

    assigned = client.put(f"/api/meal-plan/{today}", json={"recipe_id": created.json()["id"]})
    assert assigned.status_code == 200
    assert assigned.json()["recipe"]["name"] == "Toast"

    cleared = client.put(f"/api/meal-plan/{today}", json={"recipe_id": None})
    assert cleared.status_code == 200
    assert cleared.json()["recipe"] is None


def test_assign_nonexistent_recipe_returns_404() -> None:
    client = TestClient(main.app)
    today = date.today().isoformat()
    response = client.put(f"/api/meal-plan/{today}", json={"recipe_id": 9999})
    assert response.status_code == 404


def test_update_nonexistent_recipe_returns_404() -> None:
    client = TestClient(main.app)
    response = client.put(
        "/api/recipes/9999",
        json={
            "name": "Ghost",
            "description": "Missing",
            "ingredients": [],
            "tags": [],
        },
    )
    assert response.status_code == 404


def test_delete_recipe_cascades_ingredients() -> None:
    client = TestClient(main.app)
    created = client.post(
        "/api/recipes",
        json={
            "name": "Pizza",
            "description": "Cheesy",
            "ingredients": [{"unit": "1", "item": "cheese"}],
            "tags": ["dinner"],
        },
    )
    assert created.status_code == 201
    recipe_id = created.json()["id"]

    delete_response = client.delete(f"/api/recipes/{recipe_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/api/recipes/{recipe_id}")
    assert get_response.status_code == 404


def test_smart_random_no_eligible_recipes_returns_404() -> None:
    client = TestClient(main.app)
    today = date.today()

    created = client.post(
        "/api/recipes",
        json={
            "name": "Only Choice",
            "description": "Single recipe",
            "ingredients": [{"unit": "1", "item": "ingredient"}],
            "tags": ["solo"],
        },
    )
    assert created.status_code == 201
    recipe_id = created.json()["id"]

    yesterday = (today - timedelta(days=1)).isoformat()
    assign_response = client.put(f"/api/meal-plan/{yesterday}", json={"recipe_id": recipe_id})
    assert assign_response.status_code == 200

    smart_response = client.post(
        f"/api/meal-plan/{today.isoformat()}/random",
        json={"mode": "smart", "lookback_days": 7},
    )
    assert smart_response.status_code == 404


def test_filtered_random_no_matches_returns_404() -> None:
    client = TestClient(main.app)
    today = date.today()

    created = client.post(
        "/api/recipes",
        json={
            "name": "Plain",
            "description": "No match",
            "ingredients": [{"unit": "1", "item": "water"}],
            "tags": ["plain"],
        },
    )
    assert created.status_code == 201

    filtered = client.post(
        f"/api/meal-plan/{today.isoformat()}/random",
        json={"mode": "filtered", "tags": ["nonexistent-tag"]},
    )
    assert filtered.status_code == 404


def test_create_tag_idempotent() -> None:
    client = TestClient(main.app)
    first = client.post("/api/tags", json={"name": "quick"})
    assert first.status_code == 201
    second = client.post("/api/tags", json={"name": "quick"})
    assert second.status_code == 201
    assert first.json()["id"] == second.json()["id"]
