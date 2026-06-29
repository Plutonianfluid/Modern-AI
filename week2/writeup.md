# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: Give me the plan for excersize 1 of week 2 and a framework of how should I approach said problem. Do not implement or change files

Generated Code Snippets:

line 33: "content": "You extract action items from notes. Return only concrete tasks. Return only a JSON array of strings. Do not include markdown, explanations, or extra text. If there are no action items, return []",

the framework was from ollama's json website in assignment.md

### Exercise 2: Add Unit Tests
Prompt: Write unit tests for `extract_action_items_llm()` covering multiple inputs (e.g., bullet lists, keyword-prefixed lines, empty input) in `week2/tests/test_extract.py`.

Generated Code Snippets: from ..app.services.extract import extract_action_items

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

### Exercise 3: Refactor Existing Code for Clarity
Prompt: Give me a detailed plan for the 3rd todo of the assignment and a framework for me to follow but do not do any implementing without my permission

Generated/Modified Code Snippets: 

db.py:
NoteRecord = dict[str, Any]
ActionItemRecord = dict[str, Any]

def serialize_note(row: sqlite3.Row) -> NoteRecord:
    return {
        "id": row["id"],
        "content": row["content"],
        "created_at": row["created_at"],
    }


def serialize_action_item(row: sqlite3.Row) -> ActionItemRecord:
    return {
        "id": row["id"],
        "note_id": row["note_id"],
        "text": row["text"],
        "done": bool(row["done"]),
        "created_at": row["created_at"],
    }

main.py
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="Action Item Extractor", lifespan=lifespan)

Action items.py

@router.post("/extract", response_model=ExtractActionItemsResponse)
def extract(payload: ExtractActionItemsRequest) -> ExtractActionItemsResponse:
    text = payload.text.strip()

Schemas.py

from __future__ import annotations

from pydantic import BaseModel


class NoteCreate(BaseModel):
    content: str


class NoteResponse(BaseModel):
    id: int
    content: str
    created_at: str


class ExtractActionItemsRequest(BaseModel):
    text: str
    save_note: bool = False


class ExtractedActionItemResponse(BaseModel):
    id: int
    text: str


class ExtractActionItemsResponse(BaseModel):
    note_id: int | None
    items: list[ExtractedActionItemResponse]


class ActionItemResponse(BaseModel):
    id: int
    note_id: int | None
    text: str
    done: bool
    created_at: str


class MarkDoneRequest(BaseModel):
    done: bool = True


class MarkDoneResponse(BaseModel):
    id: int
    done: bool


### Exercise 4: Use Agentic Mode to Automate a Small Task
Prompt: give a detailed plan for TODO number 4

Generated Code Snippets: 
@router.post("/extract", response_model=ExtractActionItemsResponse)
def extract(payload: ExtractActionItemsRequest) -> ExtractActionItemsResponse:
    return _extract_and_save(payload, extract_service.extract_action_items)


@router.post("/extract-llm", response_model=ExtractActionItemsResponse)
def extract_llm(payload: ExtractActionItemsRequest) -> ExtractActionItemsResponse:
    extractor = getattr(
        extract_service,
        "extract_action_items_llm",
        extract_service.extract_action_items,
    )
    return _extract_and_save(payload, extractor)


@router.get("", response_model=list[NoteResponse])
def list_all_notes() -> list[NoteResponse]:
    return [NoteResponse(**note) for note in db.list_notes()]

$('#extract_llm').addEventListener('click', () => {
        extractItems('/action-items/extract-llm', 'Extracting with LLM...');
      });

      $('#list_notes').addEventListener('click', async () => {
        notesEl.textContent = 'Loading notes...';
        try {
          const res = await fetch('/notes');
          if (!res.ok) throw new Error('Request failed');
          const notes = await res.json();
          if (!notes.length) {
            notesEl.innerHTML = '<p class="muted">No saved notes yet.</p>';
            return;
          }
          notesEl.innerHTML = '<h2>Saved Notes</h2>' + notes.map(note => (
            `<div class="note">
              <div class="muted">Note ${note.id} · ${escapeHtml(note.created_at)}</div>
              <div>${escapeHtml(note.content)}</div>
            </div>`
          )).join('');
        } catch (err) {
          console.error(err);
          notesEl.textContent = 'Error loading notes';
        }
      });


### Exercise 5: Generate a README from the Codebase
Prompt: Generate a README from the Codebase

Generated Code Snippets:
README.md file


## SUBMISSION INSTRUCTIONS
Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields. 