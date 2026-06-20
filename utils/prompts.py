def build_prompt(
tool_type,
subject,
topic,
duration,
difficulty,
audience,
learning_objectives,
customization
):

    common_context = f"""

    Subject: {subject}
    Topic: {topic}
    Duration: {duration}
    Difficulty: {difficulty}
    Target Audience: {audience}

    Learning Objectives:
    {learning_objectives}

    Customization:
    {customization}
    """

    prompts = {

        "Study Plan": f"""

    You are an expert educator.

    {common_context}

    Create:

    Overview
    Learning Goals
    Study Timeline
    Activities
    Practice Exercises
    Assessment Questions
    Summary

    Return Markdown only.
    """,

        "Lesson Plan": f"""

    You are an expert teacher.

    {common_context}

    Create:

    Lesson Objectives
    Introduction
    Teaching Activities
    Student Activities
    Assessment
    Summary

    Return Markdown only.
    """,

        "Quiz Generator": f"""

    You are an assessment specialist.

    {common_context}

    Generate:

    10 MCQs
    5 Short Answer Questions
    Answer Key

    Return Markdown only.
    """,

        "Flashcard Generator": f"""

    You are an educational flashcard creator.

    {common_context}

    Generate 15 flashcards.

    Format:

    Question:
    Answer:

    Return Markdown only.
    """
    }

    return prompts[tool_type]