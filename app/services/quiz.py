from uuid import UUID, uuid4
import random

from app.data import SESSIONS
from app.models import (
    QuizCreate,
    QuizQuestion,
    QuizSession,
    QuizResponse,
    AnswerSubmit,
    AnswerResult,
    Difficulty
)

from app.services.vocabulary import get_words

from app.exceptions import (
    QuizNotFoundError,
    InsufficientVocabularyError,
    QuestionNotFoundError,
    AlreadyAnsweredError
)


XP_BY_DIFFICULTY = {
    Difficulty.EASY: 10,
    Difficulty.MEDIUM: 20,
    Difficulty.HARD: 30
}


def to_quiz_response(
    session: QuizSession
) -> QuizResponse:
    questions = []
    for question in session.questions:
        public_question = QuizQuestion(
            id = question.id,
            word = question.word,
            language = question.language,
            difficulty = question.difficulty
        )
        questions.append(public_question)
    answer_count = len(session.answers)
    correct = sum(session.answers.values())
    completed = answer_count == len(session.questions)
    return QuizResponse(
    id=session.id,
    questions=questions,
    answered_count=answer_count,
    correct_count=correct,
    xp=session.xp,
    completed=completed
)

    


def create_quiz(request: QuizCreate) -> QuizResponse:
    words = get_words(
        language=request.language,
        difficulty=request.difficulty
    )

    if len(words) < request.num_questions:
        raise InsufficientVocabularyError(
            "Not enough matching vocabulary"
        )

    selected_questions = random.sample(words, request.num_questions)

    session = QuizSession(
        id=uuid4(),
        questions=selected_questions
    )

    SESSIONS[session.id] = session

    return to_quiz_response(session)




def get_quiz(session_id: UUID) -> QuizResponse:
    session = SESSIONS.get(session_id)

    if session is None:
        raise QuizNotFoundError("Quiz not found")

    return to_quiz_response(session)


def submit_answer(
    session_id: UUID,
    request: AnswerSubmit
) -> AnswerResult:

    # Retrieve session
    session = SESSIONS.get(session_id)

    if session is None:
        raise QuizNotFoundError("Quiz not found")

    # Find question & difficulty
    question = None
    difficulty = None

    for word in session.questions:
        if word.id == request.word_id:
            question = word
            difficulty = word.difficulty
            break

    if question is None:
        raise QuestionNotFoundError(
            "Question not found in quiz"
        )

    # Prevent duplicate submissions
    if request.word_id in session.answers:
        raise AlreadyAnsweredError(
            "Question already answered"
        )

    # Evaluate correctness
    submitted_answer = request.answer.strip().casefold()
    expected_answer = question.translation.strip().casefold()

    correct = submitted_answer == expected_answer

    # Calculate XP
    xp_earned = XP_BY_DIFFICULTY[difficulty] if correct else 0

    # Update session state
    session.answers[request.word_id] = correct
    session.xp += xp_earned

    # Determine completion
    completed = len(session.answers) == len(session.questions)

    # Return feedback
    return AnswerResult(
        word_id=request.word_id,
        correct=correct,
        correct_answer=question.translation,
        xp_earned=xp_earned,
        total_xp=session.xp,
        completed=completed
    )