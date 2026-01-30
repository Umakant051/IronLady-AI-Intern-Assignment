# Task1: AI-Powered Virtual Assistant for Iron Lady Learners
# app.py
import streamlit as st

st.set_page_config(page_title="Iron Lady AI Chatbot", page_icon="🤖")

st.title("🤖 Iron Lady AI Chatbot")
st.write("Ask me about Iron Lady programs, enrollment, or support!")

# Placeholder for conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

# Input from user
user_input = st.text_input("You:", "")

if user_input:
    # Store user message
    st.session_state.messages.append(f"User: {user_input}")
    
    # Placeholder AI response
    response = f"AI: I understood your question about '{user_input}'! (Replace this with real AI)"
    
    st.session_state.messages.append(response)

# Display chat
for msg in st.session_state.messages:
    st.write(msg)
