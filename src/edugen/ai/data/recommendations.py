from dataclasses import dataclass


@dataclass(frozen=True)
class DatasetRecommendation:
    dataset_id: str
    purpose: str
    license: str
    estimated_size: str
    advantages: str
    limitations: str
    download_source: str
    expected_contribution: str


def recommended_datasets() -> list[DatasetRecommendation]:
    return [
        DatasetRecommendation(
            dataset_id="allenai/sciq",
            purpose="Science question answering and explanations.",
            license="cc-by-nc-3.0",
            estimated_size="about 13k multiple choice science questions",
            advantages="Good for quiz, answer-key, and science concept generation.",
            limitations="Science-focused and non-commercial license.",
            download_source="https://huggingface.co/datasets/allenai/sciq",
            expected_contribution="Improves factual educational QA and quiz style.",
        ),
        DatasetRecommendation(
            dataset_id="databricks/databricks-dolly-15k",
            purpose="Instruction-following examples across explanation and generation tasks.",
            license="cc-by-sa-3.0",
            estimated_size="15k instruction-response records",
            advantages="Small, reproducible, easy to preprocess.",
            limitations="General instruction data, not only education.",
            download_source="https://huggingface.co/datasets/databricks/databricks-dolly-15k",
            expected_contribution="Improves instruction formatting and response structure.",
        ),
        DatasetRecommendation(
            dataset_id="OpenAssistant/oasst1",
            purpose="Human-written assistant conversations.",
            license="apache-2.0",
            estimated_size="161k multilingual messages",
            advantages="Good conversational instruction data with permissive license.",
            limitations="Needs filtering because not all samples are educational.",
            download_source="https://huggingface.co/datasets/OpenAssistant/oasst1",
            expected_contribution="Improves assistant tone and multi-turn explanation quality.",
        ),
        DatasetRecommendation(
            dataset_id="openstax_textbooks",
            purpose="Open educational textbook source material.",
            license="cc-by-4.0",
            estimated_size="varies by selected books",
            advantages="High-quality academic educational content.",
            limitations="Requires custom extraction and attribution handling.",
            download_source="https://openstax.org/",
            expected_contribution="Provides reliable source knowledge and references.",
        ),
    ]
