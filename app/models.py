from enum import Enum
from pydantic import BaseModel, Field


class Difficulty(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class VocabularyWord(BaseModel):
    id: int = Field(gt=0)
    word: str = Field(min_length=1, max_length=100)
    translation: str = Field(min_length=1, max_length=100)
    language: str = Field(min_length=2, max_length=2)
    difficulty: Difficulty

from uuid import UUID
from pydantic import Field


class QuizCreate(BaseModel):
    language: str = Field(min_length=2, max_length=2)
    difficulty: Difficulty | None=None
    num_questions: int=Field(default=3, ge=1, le=10)


class QuizQuestion(BaseModel):
    id: int
    word: str
    language: str
    difficulty: Difficulty


class QuizSession(BaseModel):
    id: UUID
    questions: list[VocabularyWord]
    answers: dict[int,bool] = Field(default={})
    xp: int = Field(default=0)


class QuizResponse(BaseModel):
    id: UUID
    questions:list[QuizQuestion]
    answered_count: int
    correct_count: int
    xp: int
    completed: bool


class AnswerSubmit(BaseModel):
    word_id: int = Field(ge=0)
    answer: str = Field(min_length=1, max_length=100)


class AnswerResult(BaseModel):
    word_id: int
    correct: bool
    correct_answer:	str
    xp_earned: int
    total_xp: int
    completed: bool