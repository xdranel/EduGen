import html
import re


class TextPreprocessor:
    def clean(self, text: str) -> str:
        text = html.unescape(text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = text.encode("utf-8", errors="ignore").decode("utf-8")
        text = " ".join(text.split())
        return text.strip()

    def clean_many(self, texts: list[str], min_length: int = 1) -> list[str]:
        seen: set[str] = set()
        cleaned_texts: list[str] = []

        for text in texts:
            cleaned = self.clean(text)
            if len(cleaned) < min_length or cleaned in seen:
                continue
            seen.add(cleaned)
            cleaned_texts.append(cleaned)

        return cleaned_texts

    def instruction_format(self, instruction: str, response: str, input_text: str = "") -> dict[str, str]:
        return {
            "instruction": self.clean(instruction),
            "input": self.clean(input_text),
            "output": self.clean(response),
        }
