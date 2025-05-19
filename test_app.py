import pytest
from main import app, get_db_connection


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_get_news(client):
    response = client.get("/news")
    print("Response Json:", response.get_json())
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data


def test_get_news_params(client):
    response = client.get("/news?country=gb&category=technology")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data


def test_missing_api_key(monkeypatch, client):
    monkeypatch.setenv("NEWS_API_KEY", "")
    response = client.get("/news")
    data = response.get_json()
    assert response.status_code != 200
    assert "error" in data


def test_invalid_url(monkeypatch, client):
    monkeypatch.setattr("main.news_url", "https://invalid-url.org/")
    response = client.get("/news")
    data = response.get_json()
    assert response.status_code == 500
    assert "error" in data


def test_db_connection():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        assert any("articles" in table for table in tables), "articles table not found"
    except Exception as e:
        pytest.fail(f"DB connection failed: {e}")
    finally:
        if conn:
            conn.close()
