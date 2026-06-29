from ..app.services.extract import extract_action_items


def test_extract_bullet_list_items():
    text = """
    Meeting notes:
    - Set up database
    * Implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)

    assert items == [
        "Set up database",
        "Implement API extract endpoint",
        "Write tests",
    ]


def test_extract_checkbox_items():
    text = """
    - [ ] Set up database
    - [todo] Write tests
    """.strip()

    items = extract_action_items(text)

    assert items == [
        "Set up database",
        "Write tests",
    ]


def test_extract_keyword_prefixed_items():
    text = """
    TODO: Update onboarding docs
    action: Email the team
    next: Schedule review meeting
    Random note that should not be included.
    """.strip()

    items = extract_action_items(text)

    assert items == [
        "TODO: Update onboarding docs",
        "action: Email the team",
        "next: Schedule review meeting",
    ]


def test_extract_empty_input_returns_empty_list():
    assert extract_action_items("") == []


def test_extract_whitespace_input_returns_empty_list():
    assert extract_action_items("   \n\n   ") == []


def test_extract_imperative_sentence_fallback():
    text = "Update the README. Discussed project timeline. Write tests for extractor."

    items = extract_action_items(text)

    assert items == [
        "Update the README.",
        "Write tests for extractor.",
    ]


def test_extract_deduplicates_items_case_insensitively():
    text = """
    - Write tests
    - write tests
    - Write tests
    """.strip()

    items = extract_action_items(text)

    assert items == ["Write tests"]