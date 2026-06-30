import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.environ.get("GEMINI_API_KEY", "your-api-key-here"))

model = genai.GenerativeModel("gemini-flash-latest")

st.title("🎭 Debate Me!")

if "history" not in st.session_state:
    st.session_state.history = []

topic = st.text_input("Enter a topic to debate:")
user_input = st.text_input("Your argument:")

if st.button("Submit") and topic and user_input:
    prompt = f"""You are a debater. Topic: "{topic}". 
    Always argue AGAINST the user's position. Be sharp and logical, under 100 words.
    User said: {user_input}"""
    response = model.generate_content(prompt)
    st.session_state.history.append(("You", user_input))
    st.session_state.history.append(("AI", response.text))

for speaker, msg in st.session_state.history:
    st.write(f"**{speaker}:** {msg}")

if st.button("End Debate & Get Score") and st.session_state.history:
    convo = str(st.session_state.history)
    score_prompt = f"Score this debate performance out of 100 with 3 tips: {convo}"
    score = model.generate_content(score_prompt)
    st.write("### Result")
    st.write(score.text)