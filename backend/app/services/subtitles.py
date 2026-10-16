from collections.abc import Iterable
from pathlib import Path

from backend.app.services.languages import normalize_language_hint, recognized_region_subtag


def _region_token(token: str) -> str | None:
    if len(token) != 2 or not token.isalpha():
        return None
    region = recognized_region_subtag(token)
    if region is None:
        return None

    # Some region subtags are also language codes (for example BR and PT).
    # Their standard uppercase spelling disambiguates them from language names.
    if normalize_language_hint(token) is not None and token != token.upper():
        return None
    return region


def _language_region_pair(left: str, right: str) -> str | None:
    # Composite tags are already handled by normalize_language_hint and must
    # not be split into separate subtags.
    if any(separator in left or separator in right for separator in ("-", "_")):
        return None

    candidates: list[tuple[str, str]] = []
    left_region = _region_token(left)
    right_language = normalize_language_hint(right)
    if left_region and right_language:
        candidates.append((right_language, left_region))

    left_language = normalize_language_hint(left)
    right_region = _region_token(right)
    if left_language and right_region:
        candidates.append((left_language, right_region))

    # If both interpretations are possible (such as BR.PT), keep the legacy
    # first-language behavior rather than guessing which token is the region.
    if len(candidates) != 1:
        return None
    language, region = candidates[0]
    return normalize_language_hint(f"{language}-{region}")


def _detect_external_subtitles_from_names(
    video_path: Path,
    candidate_names: Iterable[str],
    allowed_extensions: tuple[str, ...],
) -> list[dict[str, str | None]]:
    suffixes = {extension.lower() for extension in allowed_extensions}
    stem = video_path.stem
    detected: list[dict[str, str | None]] = []

    for entry_name in sorted(candidate_names, key=str.lower):
        if entry_name == video_path.name:
            continue
        entry_path = Path(entry_name)
        extension = entry_path.suffix.lower()
        if extension not in suffixes:
            continue
        if not (entry_path.stem == stem or entry_name.startswith(f"{stem}.")):
            continue

        middle = entry_name[len(stem) : -len(extension)]
        tokens = [token for token in middle.split(".") if token]
        language = None
        for index, token in enumerate(tokens):
            if index + 1 < len(tokens):
                language = _language_region_pair(token, tokens[index + 1])
                if language:
                    break
            language = normalize_language_hint(token)
            if language:
                break

        detected.append(
            {
                "path": entry_name,
                "language": language,
                "format": extension.lstrip("."),
            }
        )

    return detected


def detect_external_subtitles_from_names(
    video_path: Path,
    sibling_names: Iterable[str],
    allowed_extensions: tuple[str, ...],
) -> list[dict[str, str | None]]:
    return _detect_external_subtitles_from_names(video_path, sibling_names, allowed_extensions)


def detect_external_subtitles(
    video_path: Path,
    allowed_extensions: tuple[str, ...],
) -> list[dict[str, str | None]]:
    # Inspect only matching sidecars. An unreadable, unrelated media file in the
    # same directory must not turn every neighboring file into an analysis failure.
    candidates = _detect_external_subtitles_from_names(
        video_path, (entry.name for entry in video_path.parent.iterdir()), allowed_extensions,
    )
    return [item for item in candidates if (video_path.parent / str(item["path"])).is_file()]
