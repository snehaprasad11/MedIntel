from recommendation_engine import generate_recommendation


def generate_llm_insight(metrics):
    """
    Simulated LLM response layer.

    Later this can be replaced with:
    - OpenAI GPT
    - Gemini
    - Claude
    """

    recommendation = generate_recommendation(metrics)

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