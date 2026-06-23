import os

USE_OPENAI = os.getenv("USE_OPENAI", "False").lower() == "true"


def get_llm_response(prompt):
    """
    Central LLM interface.

    Today:
        returns mock response

    Future:
        calls OpenAI automatically
    """

    if USE_OPENAI:
        from openai_insights import generate_openai_response
        return generate_openai_response(prompt)

    return """
Executive Summary:
Operational demand exceeded normal capacity.

Operational Risks:
- Increased wait times
- Higher patient backlog

Recommendations:
- Increase physician coverage
- Expand triage staffing
"""