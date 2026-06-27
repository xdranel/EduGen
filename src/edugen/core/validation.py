from edugen.core.exceptions import ValidationError


def validate_topic(topic: str) -> str:
    cleaned = " ".join(topic.strip().split())
    if not cleaned:
        raise ValidationError("Topic is required.")
    if len(cleaned) > 200:
        raise ValidationError("Topic must be 200 characters or fewer.")
    return cleaned
