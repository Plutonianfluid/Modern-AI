import re

_PREFIX = re.compile(r"^(?:todo|action(?: item)?|next step)\s*:\s*", re.IGNORECASE)
_CHECKBOX = re.compile(r"^\s*[-*]\s*\[\s\]\s*(.+)$")
_BULLET = re.compile(r"^\s*[-*]\s+")
_IMPERATIVE = re.compile(
    r"^(?:please\s+)?(?:call|email|send|schedule|review|update|write|create|fix|"
    r"follow up|submit|finish|prepare|deploy|ship)\b",
    re.IGNORECASE,
)


def extract_action_items(text: str) -> list[str]:
    """Extract explicit and likely action items while preserving their wording."""
    results: list[str] = []
    seen: set[str] = set()

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        checkbox = _CHECKBOX.match(line)
        candidate = checkbox.group(1).strip() if checkbox else _BULLET.sub("", line).strip()
        explicit_prefix = bool(_PREFIX.match(candidate))
        actionable = (
            checkbox is not None
            or explicit_prefix
            or candidate.endswith("!")
            or bool(_IMPERATIVE.match(candidate))
        )
        if not actionable:
            continue

        candidate = _PREFIX.sub("", candidate).strip()
        key = candidate.casefold()
        if candidate and key not in seen:
            results.append(candidate)
            seen.add(key)

    return results
