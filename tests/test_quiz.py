import pytest

from fastapi.testclient import TestClient
from app.main import app
from app.data import SESSIONS


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_sessions():
    SESSIONS.clear()
    yield
    SESSIONS.clear()


def create_test_quiz(difficulty="easy", count=2):
    response = client.post(
        "/quizzes",
        json={
            "language": "es",
            "difficulty": difficulty,
            "num_questions": count
        }
    )

    assert response.status_code == 201

    return response.json()


def test_create_quiz():
    quiz = create_test_quiz()

    assert len(quiz["questions"]) == 2
    assert quiz["xp"] == 0
    assert quiz["answered_count"] == 0
    assert quiz["completed"] is False

    for question in quiz["questions"]:
        assert "translation" not in question


def test_correct_answer():
    quiz = create_test_quiz()

    response = client.post(
        f"/quizzes/{quiz['id']}/answers",
        json={
            "word_id": 1,
            "answer": "  APPLE  "
        }
    )

    assert response.status_code == 200
    assert response.json()["correct"] is True
    assert response.json()["xp_earned"] == 10


def test_duplicate_answer():
    quiz = create_test_quiz()

    url = f"/quizzes/{quiz['id']}/answers"

    answer = {
        "word_id": 1,
        "answer": "apple"
    }

    first = client.post(url, json=answer)
    assert first.status_code == 200

    second = client.post(url, json=answer)
    assert second.status_code == 409

    progress = client.get(f"/quizzes/{quiz['id']}")

    assert progress.json()["xp"] == 10


def test_invalid_question_count():
    response = client.post(
        "/quizzes",
        json={
            "language": "es",
            "num_questions": 0
        }
    )

    assert response.status_code == 422


def test_insufficient_vocabulary():
    response = client.post(
        "/quizzes",
        json={
            "language": "es",
            "num_questions": 10
        }
    )

    assert response.status_code == 400


def test_question_outside_quiz():
    quiz = create_test_quiz()

    response = client.post(
        f"/quizzes/{quiz['id']}/answers",
        json={
            "word_id": 5,
            "answer": "hello"
        }
    )

    assert response.status_code == 404


def test_hard_question_scoring():
    quiz = create_test_quiz(
        difficulty="hard",
        count=1
    )

    response = client.post(
        f"/quizzes/{quiz['id']}/answers",
        json={
            "word_id": 4,
            "answer": "unfortunately"
        }
    )

    assert response.status_code == 200
    assert response.json()["xp_earned"] == 30
    assert response.json()["completed"] is True


def test_independent_sessions():
    first = create_test_quiz()
    second = create_test_quiz()

    assert first["id"] != second["id"]

    response = client.post(
        f"/quizzes/{first['id']}/answers",
        json={
            "word_id": 1,
            "answer": "apple"
        }
    )

    assert response.status_code == 200

    progress = client.get(f"/quizzes/{second['id']}")

    assert progress.json()["xp"] == 0
    assert progress.json()["answered_count"] == 0