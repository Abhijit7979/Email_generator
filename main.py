# main.py

import streamlit as st
from llm.email_bot import generate_email_from_input

st.set_page_config(page_title="Email Writer", layout="centered")

st.title("📧  Email Generator")
st.markdown("Enter a one-line description of your email, and we'll generate a professional email for you!")
example_prompts = [
    "I’m Abhijit Rao, write a polite email to my professor Dr. Sharma asking for an extension on the AI project deadline due to a medical emergency.",
    "I am Abhijit Rao, send a follow-up email to the HR of TCS about my interview last week and ask if there’s any update on the next steps.",
    "This is Abhijit Rao, write a formal thank-you email to my internship mentor Ms. Priya for her guidance during the summer project.",
    "I’m Abhijit Rao, write a professional email to a company requesting sponsorship for a college tech fest I’m organizing next month.",
    "I am Abhijit Rao, write a convincing email to my manager explaining why I need to take two extra days off after my planned leave."
]

with st.expander("📌 Click to see example prompts"):
    for prompt in example_prompts:
        if st.button(prompt[:80] + "...", key=prompt):
            st.session_state["user_input"] = prompt

user_input = st.text_area(
    "✍️ Describe your email in one line:",
    value=st.session_state.get("user_input", ""),
    height=100
)

# ---------- GENERATE EMAIL ----------
if st.button("Generate Email"):
    if not user_input.strip():
        st.warning("Please enter a valid input.")
    else:
        with st.spinner("Generating your email..."):
            try:
                email = generate_email_from_input(user_input)
                st.success("✅ Email generated:")
                st.text_area("📨 Your Email", email, height=300)
            except Exception as e:
                st.error(f"Something went wrong: {e}")