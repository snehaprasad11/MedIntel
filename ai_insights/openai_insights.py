from ai_insights.recommendation_engine import generate_recommendation


def generate_llm_insight(metrics: dict):

    summary = f"""
Total appointments analyzed: {metrics['total_appointments']}

Average wait time: {metrics['avg_wait_time']} minutes

Average bed occupancy: {metrics['avg_bed_occupancy']}%

Average ICU occupancy: {metrics['avg_icu_occupancy']}%
"""

    recommendation = generate_recommendation(metrics)

    return {
        "executive_summary": summary,
        "recommendation": recommendation
    }