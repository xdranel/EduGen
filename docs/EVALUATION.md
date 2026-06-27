# Evaluation Framework

Prompt 5 adds a local evaluation framework for generated educational content.

## Metrics

| Metric | Purpose | Limitation |
| --- | --- | --- |
| ROUGE-1 | Measures unigram overlap with a reference answer. | Rewards wording overlap, not factual correctness. |
| ROUGE-L | Measures longest common subsequence overlap. | Can miss paraphrases. |
| BLEU | Measures precision-style token overlap. | Harsh for valid alternative explanations. |
| BERTScore fallback | Uses lexical similarity when optional BERTScore is not installed. | Real BERTScore requires the optional dependency. |
| Latency | Measures response time. | Hardware dependent. |
| Memory/CPU usage | Tracks resource cost. | Optional richer tracking requires `psutil`. |
| Generation speed | Tokens per second approximation. | Uses whitespace tokens unless tokenizer data is provided. |

## Human Evaluation

Human reviewers score each output from 1 to 5:

- Correctness
- Coherence
- Readability
- Educational Value
- Completeness
- Grammar
- Relevance

The framework computes the average score automatically.

## Error Analysis

The analyzer detects:

- repetition
- hallucination indicators
- incomplete answers
- too short
- too long
- missing required sections

## Outputs

Reports are saved under:

```text
outputs/evaluation/
```

Supported report formats:

- Markdown
- HTML
- CSV
- PDF when `reportlab` is installed

Optional richer evaluation dependencies:

```bash
pip install -r requirements-evaluation.txt
```
