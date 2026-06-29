from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv
from pydantic import BaseModel

class Response(BaseModel):
    items: list[str]


def extract_action_items(text: str) -> List[str]:
    lines = []

    for line in text.splitlines():
        if line.strip():
            cleaned_line = " ".join(line.split())
            lines.append(cleaned_line)

    if not lines:
        return []
    
    notes = "\n".join(lines)

    response = chat(
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract action items from notes. "
                    "Extract only concrete tasks. "
                    "Ignore summaries and observations. "
                    "Return JSON matching the provided schema."
                )
            },
            {
                'role': 'user',
                "content": f"Notes:\n{notes}"
            }
        ],
        model='llama3.1',
        format=Response.model_json_schema(),
    )

    unique = Response.model_validate_json(response.message.content)
    return unique.items