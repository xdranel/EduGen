from dataclasses import dataclass
import re


@dataclass(frozen=True)
class ContentSection:
    title: str
    body: str


SECTION_HEADING = re.compile(r"^\s*(?:\d+\.\s*)?([A-Z][A-Za-z -]+)\s*$")


def split_sections(content: str) -> list[ContentSection]:
    sections: list[ContentSection] = []
    current_title = "Generated Material"
    current_lines: list[str] = []

    for line in content.splitlines():
        match = SECTION_HEADING.match(line)
        if match and len(line.strip()) < 80:
            if current_lines:
                sections.append(ContentSection(current_title, "\n".join(current_lines).strip()))
                current_lines = []
            current_title = match.group(1).strip()
        else:
            current_lines.append(line)

    if current_lines:
        sections.append(ContentSection(current_title, "\n".join(current_lines).strip()))

    return [section for section in sections if section.body]
