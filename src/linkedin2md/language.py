"""Language detection implementations.

Single Responsibility: Detect language of text.
"""

import re

from linkedin2md.protocols import LanguageDetector, MultilingualText


class SpanishEnglishDetector(LanguageDetector):
    """Detect Spanish vs English text.

    Single Responsibility: Only handles language detection.
    Extensible: Implement LanguageDetector protocol for other languages.
    """

    # Spanish language detection patterns
    SPANISH_PATTERNS = [
        r"\b(el|la|los|las|un|una|unos|unas)\b",  # Articles
        r"\b(de|del|en|con|por|para|sobre|entre)\b",  # Prepositions
        r"\b(que|como|donde|cuando|quien)\b",  # Conjunctions
        r"\b(es|son|fue|fueron|está|están)\b",  # Verbs
        r"\b(muy|más|también|además|durante)\b",  # Adverbs
        r"[áéíóúñ¿¡]",  # Spanish characters
    ]

    def __init__(self) -> None:
        self._regex = re.compile("|".join(self.SPANISH_PATTERNS), re.IGNORECASE)

    @property
    def supported_languages(self) -> list[str]:
        """Return list of detectable language codes."""
        return ["en", "es"]

    def detect(self, text: str) -> str:
        """Detect if text is Spanish or English."""
        if not text:
            return "en"

        matches = len(self._regex.findall(text))
        words = len(text.split())

        if words > 0 and matches / words > 0.1:
            return "es"
        return "en"


class PortugueseSpanishEnglishDetector(LanguageDetector):
    """Detect Brazilian Portuguese, Spanish or English text.

    Strategy:
    1. Decide whether the text is Romance (pt/es) using the same density
       heuristic as ``SpanishEnglishDetector`` extended with Portuguese
       markers. Any text the legacy detector classified as Spanish is still
       classified as Romance here.
    2. Disambiguate Portuguese vs Spanish by counting language-exclusive
       words, characters and suffixes. Ties resolve to Spanish to preserve
       legacy behavior.
    """

    # Words that only (or overwhelmingly) appear in Portuguese.
    # English homographs such as "do", "no", "a", "as" are intentionally
    # excluded to avoid misclassifying English text.
    PORTUGUESE_WORDS = frozenset(
        {
            "um", "uma", "uns", "umas", "com", "em", "da", "das", "dos",
            "nas", "nos", "ao", "aos", "às", "pelo", "pela", "pelos", "pelas",
            "não", "são", "também", "você", "vocês", "é", "foi", "foram",
            "estão", "muito", "muita", "mais", "onde", "quando", "sou",
            "seu", "sua", "seus", "suas", "meu", "minha", "isso", "isto",
            "esse", "essa", "já", "até", "ou", "então", "atual", "atuação",
            "trabalho", "experiência", "desenvolvedor", "desenvolvimento",
            "equipe", "projetos", "através", "após", "além",
        }
    )  # fmt: skip

    # Words that only (or overwhelmingly) appear in Spanish.
    SPANISH_WORDS = frozenset(
        {
            "el", "la", "los", "las", "un", "una", "unos", "unas", "del",
            "en", "con", "y", "es", "son", "fue", "fueron", "están", "muy",
            "más", "también", "además", "donde", "cuando", "quien", "soy",
            "su", "sus", "mi", "pero", "desarrollador", "desarrollo",
            "experiencia", "trabajo", "equipo", "proyectos", "través",
        }
    )  # fmt: skip

    # Words shared by both languages that still indicate Romance text
    # (same set the legacy SpanishEnglishDetector counts).
    SHARED_WORDS = frozenset(
        {
            "de", "por", "para", "sobre", "entre", "que", "como", "está",
            "durante",
        }
    )  # fmt: skip

    PORTUGUESE_CHARS = frozenset("ãõçâêôà")
    SPANISH_CHARS = frozenset("ñ¿¡")
    SHARED_CHARS = frozenset("áéíóú")

    _TOKEN = re.compile(r"[^\W\d_]+", re.UNICODE)

    @property
    def supported_languages(self) -> list[str]:
        """Return list of detectable language codes."""
        return ["en", "es", "pt"]

    def detect(self, text: str) -> str:
        """Detect if text is Portuguese, Spanish or English."""
        if not text:
            return "en"

        words = len(text.split())
        if words == 0:
            return "en"

        lowered = text.lower()
        tokens = self._TOKEN.findall(lowered)

        pt_score = 0
        es_score = 0
        shared_score = 0
        for token in tokens:
            if token in self.PORTUGUESE_WORDS:
                pt_score += 1
            if token in self.SPANISH_WORDS:
                es_score += 1
            if token in self.SHARED_WORDS:
                shared_score += 1
            if token.endswith(("ção", "ções", "ões")):
                pt_score += 1
            elif token.endswith(("ción", "ciones")):
                es_score += 1

        for character in lowered:
            if character in self.PORTUGUESE_CHARS:
                pt_score += 1
            elif character in self.SPANISH_CHARS:
                es_score += 1
            elif character in self.SHARED_CHARS:
                shared_score += 1

        romance_score = pt_score + es_score + shared_score
        if romance_score / words <= 0.1:
            return "en"
        return "pt" if pt_score > es_score else "es"


class MultilingualTextFactory:
    """Factory for creating MultilingualText objects.

    Single Responsibility: Create multilingual text with language detection.
    Dependency Inversion: Depends on LanguageDetector protocol.
    """

    def __init__(self, detector: LanguageDetector):
        self._detector = detector

    def create(self, text: str, lang: str | None = None) -> MultilingualText:
        """Create MultilingualText with text in detected/specified language."""
        if not text:
            return MultilingualText()

        detected = lang or self._detector.detect(text)
        return MultilingualText(**{detected: text})


# Backward compatibility alias
BilingualTextFactory = MultilingualTextFactory


# Default instances
_default_detector = PortugueseSpanishEnglishDetector()
_default_factory = BilingualTextFactory(_default_detector)


def get_default_detector() -> LanguageDetector:
    """Get the default language detector."""
    return _default_detector


def get_default_factory() -> BilingualTextFactory:
    """Get the default bilingual text factory."""
    return _default_factory
