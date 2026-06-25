# ADR-008: Strict Structured Outputs for AI Extraction

## Context
Resume extraction demands strict schema compliance to populate our relational database accurately. Relying on standard JSON-mode prompts often results in malformed JSON or hallucinations, leading to parsing errors or missing fields.

## Decision
We will utilize the **OpenAI Structured Outputs API** (`response_format`) using Pydantic schemas. The `OpenAIExtractionProvider` directly passes the `CandidateProfile` Pydantic class to the `parse()` method of the beta OpenAI client.

## Consequences
- **Pros**: Guarantees JSON schema adherence. Eliminates the need for manual JSON decoding, regex patching, or extensive retry loops just to get valid JSON.
- **Cons**: Binds our implementation tightly to the OpenAI Python SDK's beta features. If we migrate to Anthropic or local models, we will need to implement a fallback mechanism or adopt a library like `instructor` or `marvin` to enforce structure universally.
