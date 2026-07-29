from backend.app.services.extract import extract_action_items


def test_extract_action_items():
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert "write tests" in items
    assert "review PR" in items
    assert "Ship it!" in items


def test_extracts_checkboxes_imperatives_and_deduplicates():
    text = """
    - [ ] Email the client by Friday
    * schedule the launch
    Next step: Prepare release notes
    TODO: Fix login
    todo: fix login
    - [x] Already completed
    This is only background information.
    """

    assert extract_action_items(text) == [
        "Email the client by Friday",
        "schedule the launch",
        "Prepare release notes",
        "Fix login",
    ]


def test_extract_empty_text():
    assert extract_action_items("") == []
