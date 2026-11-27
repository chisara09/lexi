from app.models import QuizSession, VocabularyWord, Difficulty
from uuid import UUID
VOCABULARY = [
    VocabularyWord(
        id=1,
        word="manzana",
        translation="apple",
        language="es",
        difficulty=Difficulty.EASY
    ),
    VocabularyWord(
        id=2,
        word="perro",
        translation="dog",
        language="es",
        difficulty=Difficulty.EASY
    ),
    VocabularyWord(
        id=3,
        word="ventana",
        translation="window",
        language="es",
        difficulty=Difficulty.MEDIUM
    ),
    VocabularyWord(
        id=4,
        word="desafortunadamente",
        translation="unfortunately",
        language="es",
        difficulty=Difficulty.HARD
    ),
    VocabularyWord(
        id=5,
        word="bonjour",
        translation="hello",
        language="fr",
        difficulty=Difficulty.EASY
    ),
    VocabularyWord(
        id=6,
        word="fromage",
        translation="cheese",
        language="fr",
        difficulty=Difficulty.MEDIUM
    )
]

SESSIONS: dict[UUID, QuizSession] = {}