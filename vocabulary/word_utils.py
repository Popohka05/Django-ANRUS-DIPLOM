import re

import inflect


_inflect = inflect.engine()

_SINGULAR_S_ENDINGS = (
    'ss',
    'us',
    'is',
    'ous',
)


def normalize_english_text(value: str) -> str:
    return re.sub(r'\s+', ' ', value.strip().lower())


def canonicalize_english_word(value: str) -> str:
    normalized = normalize_english_text(value)
    if not normalized:
        return normalized

    singular = _singularize_if_plural(normalized)
    if singular != normalized:
        return singular

    parts = normalized.split()
    if len(parts) > 1:
        last = _singularize_if_plural(parts[-1])
        if last != parts[-1]:
            return ' '.join([*parts[:-1], last])

    return normalized


def _singularize_if_plural(value: str) -> str:
    if value.endswith(_SINGULAR_S_ENDINGS):
        return value

    singular = _inflect.singular_noun(value)
    if not singular:
        return value

    return singular
