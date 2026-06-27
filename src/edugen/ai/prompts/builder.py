from edugen.ai.prompts.templates import EDUCATIONAL_MATERIAL_TEMPLATE, SECTION_TEMPLATES
from edugen.core.validation import validate_topic


class PromptBuilder:
    def educational_material(
        self,
        topic: str,
        difficulty: str = "Beginner",
        language: str = "English",
        quiz_count: int = 5,
    ) -> str:
        return EDUCATIONAL_MATERIAL_TEMPLATE.format(
            topic=validate_topic(topic),
            difficulty=difficulty,
            language=language,
            quiz_count=quiz_count,
        ).strip()

    def section(self, section_name: str, **values: object) -> str:
        template = SECTION_TEMPLATES[section_name]
        if "topic" in values:
            values["topic"] = validate_topic(str(values["topic"]))
        return template.format(**values).strip()
