import os
import streamlit as st

st.set_page_config(page_title="Iron Lady AI Chatbot", page_icon="🤖")

st.title("🤖 Iron Lady AI Chatbot")
st.write("Ask me about Iron Lady programs, enrollment, or support!")

# Check if API key exists
API_KEY = os.getenv("OPENAI_API_KEY")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.text_input("You:")

if user_input:
    st.session_state.messages.append(("User", user_input))

    # Default fallback reply
    user_text = user_input.lower()

    if "what is iron lady" in user_text:
        ai_reply = (
            "Iron Lady is a women-focused learning and career empowerment platform "
            "that provides structured programs, mentorship, and skill development."
        )

    elif "program" in user_text:
        ai_reply = (
            "Iron Lady offers career-oriented programs designed to enhance skills, "
            "confidence, and leadership abilities for women."
        )

    elif "enroll" in user_text or "join" in user_text:
        ai_reply = (
            "Users can enroll in Iron Lady programs by exploring available courses "
            "and following the enrollment process on the official website."
        )

    elif "why" in user_text and "iron lady" in user_text:
        ai_reply = (
            "The name 'Iron Lady' represents strength, confidence, and resilience, "
            "reflecting the platform’s mission to empower women professionally."
        )

    else:
        ai_reply = (
            "I can help you understand Iron Lady programs, enrollment, and support. "
            "Please ask a specific question."
        )


    # Try OpenAI ONLY if API key exists
    if API_KEY:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=API_KEY)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant for Iron Lady."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.4
            )
            ai_reply = response.choices[0].message.content

        except Exception:
            pass  # silently fall back

    st.session_state.messages.append(("AI", ai_reply))

# Display chat
for role, msg in st.session_state.messages:
    st.write(f"**{role}:** {msg}")
