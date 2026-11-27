from fastapi import FastAPI, HTTPException

from app.models import VocabularyWord, Difficulty
from app.services.vocabulary import (
    get_words,
    get_word_by_id
)

from uuid import UUID

from app.models import (
    QuizCreate,
    QuizResponse,
    AnswerSubmit,
    AnswerResult
)

from app.services.quiz import (
    create_quiz,
    get_quiz,
    submit_answer
)

from app.exceptions import (
    QuizNotFoundError,
    InsufficientVocabularyError,
    QuestionNotFoundError,
    AlreadyAnsweredError
)

app = FastAPI(
    title="Lexi",
    description="Vocabulary learning API",
    version="0.1.0"
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/words", response_model=list[VocabularyWord])
def list_words(language: str | None=None,difficulty: Difficulty | None=None):
    return get_words(language,difficulty)


@app.get("/words/{word_id}", response_model=VocabularyWord)
def list_word_by_id(word_id: int):
    word = get_word_by_id(word_id)
    if not word:
        raise HTTPException(status_code=404, detail="Word not found")
    return word


@app.post(
    "/quizzes",
    response_model=QuizResponse,
    status_code=201
)
def create_quiz_endpoint(request: QuizCreate):
    try:
        return create_quiz(request)

    except InsufficientVocabularyError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@app.get(
    "/quizzes/{session_id}",
    response_model=QuizResponse
)
def get_quiz_endpoint(session_id: UUID):
    try:
        return get_quiz(session_id)

    except QuizNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

@app.post(
    "/quizzes/{session_id}/answers",
    response_model=AnswerResult
)
def submit_answer_endpoint(
    session_id: UUID,
    request: AnswerSubmit
):
    # TODO: Call submit_answer()
    try:
        return submit_answer(session_id, request)
    except QuizNotFoundError as e:
        raise HTTPException(
            status_code=404,
            detail = str(e)
        )
    except QuestionNotFoundError as e:
            raise HTTPException(
                status_code=404,
                detail = str(e)
            )
    except AlreadyAnsweredError as e:
            raise HTTPException(
                status_code=409,
                detail = str(e)
            )