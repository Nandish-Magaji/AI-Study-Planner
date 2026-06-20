import os
import streamlit as st

from utils.llm import generate_response
from utils.prompts import build_prompt
from utils.pdf_generator import create_pdf

st.markdown(
    """
    <div class="main-header">
        <h1>📚 AI Study Planner Pro</h1>
        <p>
            Generate Study Plans, Lesson Plans,
            Quizzes and Flashcards using AI.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

def load_css():

    with open("assets/styles.css") as f:

        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True
        )

load_css()

if "history" not in st.session_state:
    st.session_state.history = []

if "current_output" not in st.session_state:
    st.session_state.current_output = ""

show_history = len(st.session_state.history) > 0

if show_history:
    left_col, output_col, history_col = st.columns([1, 2.5, 1])
else:
    left_col, output_col = st.columns([1, 2.5])

with left_col:
    with st.container(border=True):

        st.markdown("### ⚙️ Configuration")

        tool_type = st.selectbox(
            "Choose Tool",
            [
                "Study Plan",
                "Lesson Plan",
                "Quiz Generator",
                "Flashcard Generator"
            ]
        )

        model_name = st.selectbox(
            "Choose Model",
            [
                "llama-3.3-70b-versatile",
                "llama-3.1-8b-instant"
            ]
        )

        difficulty = st.selectbox(
            "Difficulty Level",
            [
                "Beginner",
                "Intermediate",
                "Advanced"
            ]
        )

        audience = st.selectbox(
            "Target Audience",
            [
                "School Students",
                "College Students",
                "Professionals"
            ]
        )

        subject = st.text_input("Subject")

        topic = st.text_input("Topic")

        duration = st.text_input("Duration")

        learning_objectives = st.text_area(
            "Learning Objectives",
            height=80
        )

        customization = st.text_area(
            "Customization",
            height=80
        )

        st.divider()

        generate = st.button(
            "🚀 Generate",
            use_container_width=True
        )

        validation_placeholder = st.empty()

if generate:

    fields = [
        subject,
        topic,
        duration,
        learning_objectives,
        customization
    ]

    if not all(field.strip() for field in fields):

        validation_placeholder.markdown(
            """
            <div style="
                color:#ff6b6b;
                margin-top:8px;
                font-size:14px;
                font-weight:500;
            ">
                ⚠ Please fill out all required fields.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        validation_placeholder.empty()

        prompt = build_prompt(
            tool_type,
            subject,
            topic,
            duration,
            difficulty,
            audience,
            learning_objectives,
            customization
        )

        try:

            with st.spinner(
                "Generating content..."
            ):

                result = generate_response(
                    prompt,
                    model_name
                )

            st.session_state.current_output = result

            st.session_state.history.append(
                {
                    "tool": tool_type,
                    "topic": topic,
                    "output": result
                }
            )

        except Exception as e:

            validation_placeholder.error(
                f"Error: {str(e)}"
            )

    with output_col:

        with st.container(border=True):

            st.markdown("### 📄 Generated Output")

            if st.session_state.current_output:

                st.markdown(
                    st.session_state.current_output
                )

                st.divider()

                download_col1, download_col2 = st.columns(2)

                with download_col1:

                    st.download_button(
                        "⬇️ Markdown",
                        data=st.session_state.current_output,
                        file_name="generated_output.md",
                        mime="text/markdown"
                    )

                pdf_path = (
                    "generated_files/generated_output.pdf"
                )

                os.makedirs(
                    "generated_files",
                    exist_ok=True
                )

                create_pdf(
                    st.session_state.current_output,
                    pdf_path
                )

                with open(pdf_path, "rb") as pdf_file:

                    with download_col2:

                        st.download_button(
                            "📄 PDF",
                            data=pdf_file,
                            file_name="generated_output.pdf",
                            mime="application/pdf"
                        )

            else:

                st.info(
                    "Generated content will appear here."
                )

if show_history:

    with history_col:

        with st.container(border=True):

            st.markdown("### 📜 History")

            if st.button(
                "🗑 Clear History",
                use_container_width=True
            ):

                st.session_state.history = []
                st.rerun()

            for item in reversed(
                st.session_state.history
            ):

                with st.expander(
                    f"📝 {item['tool']} | {item['topic']}",
                    expanded=False
                ):

                    st.markdown(
                        item["output"]
                    )