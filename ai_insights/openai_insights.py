from recommendation_engine import generate_recommendation
import os


def generate_llm_insight(metrics):
    """
    Simulated LLM response layer.

    Future:
    - OpenAI GPT
    - Gemini
    - Claude
    """

    use_openai = os.getenv("USE_OPENAI", "False").lower() == "true"

    recommendation = generate_recommendation(metrics)

    if use_openai:
        summary = (
            "OpenAI integration placeholder. "
            "Replace with actual API call when API access is enabled."
        )
    else:
        summary = (
            "Operational demand exceeded normal capacity. "
            "Several KPIs indicate rising pressure on hospital resources."
        )

    return {
        "executive_summary": summary,
        "recommendation": recommendation
    }


if __name__ == "__main__":

    sample_metrics = {
        "wait_time_change": 18,
        "patient_arrivals_change": 15,
        "doctor_availability_change": -10,
        "lab_delay_change": 5
    }

    result = generate_llm_insight(sample_metrics)

    print("\nEXECUTIVE SUMMARY:")
    print(result["executive_summary"])

    print("\nRECOMMENDATION:")
    print(result["recommendation"])