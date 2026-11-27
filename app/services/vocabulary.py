from app.data import VOCABULARY
from app.models import VocabularyWord, Difficulty


def get_words(
    language: str | None = None,
    difficulty: Difficulty | None = None
) -> list[VocabularyWord]:
    words = []
    for word in VOCABULARY:
        if (not difficulty or word.difficulty == difficulty) and (not language or word.language == language):
            words.append(word)
    return words



def get_word_by_id(
    word_id: int
) -> VocabularyWord | None:
    for word in VOCABULARY:
        if word.id == word_id:
            return word
    return None
        