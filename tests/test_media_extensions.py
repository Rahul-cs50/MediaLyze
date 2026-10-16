from backend.app.core.config import AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, get_allowed_media_extensions


def test_get_allowed_media_extensions_by_library_type() -> None:
    assert get_allowed_media_extensions("movies") == VIDEO_EXTENSIONS
    assert get_allowed_media_extensions("series") == VIDEO_EXTENSIONS
    assert get_allowed_media_extensions("music") == AUDIO_EXTENSIONS
    assert get_allowed_media_extensions("audiobooks") == AUDIO_EXTENSIONS
    assert get_allowed_media_extensions("mixed") == VIDEO_EXTENSIONS + AUDIO_EXTENSIONS
    assert get_allowed_media_extensions("other") == VIDEO_EXTENSIONS + AUDIO_EXTENSIONS


def test_webm_is_a_video_extension_for_video_and_mixed_libraries() -> None:
    assert ".webm" in VIDEO_EXTENSIONS
    assert ".webm" in get_allowed_media_extensions("movies")
    assert ".webm" in get_allowed_media_extensions("series")
    assert ".webm" in get_allowed_media_extensions("mixed")
    assert ".webm" in get_allowed_media_extensions("other")
    assert ".webm" not in get_allowed_media_extensions("music")
    assert ".webm" not in get_allowed_media_extensions("audiobooks")


def test_audio_extensions_include_newly_supported_formats() -> None:
    assert {".ogg", ".oga", ".aiff", ".aif", ".alac", ".mka", ".ape", ".m4b", ".aa", ".aax"}.issubset(
        AUDIO_EXTENSIONS
    )
