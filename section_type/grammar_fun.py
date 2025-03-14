import streamlit as st
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the API key
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("API_VERSION")
api_endpoint = os.getenv("AZURE_BASE_URL")
together_api = os.getenv("TOGETHER_API_KEY")

## Azure OpenAI
'''
model_name = "gpt-4o-mini"

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=api_endpoint)
'''
## Together AI

from together import Together

model_name = "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free"
client = Together(
    api_key=together_api
)



def generate_grammar_exercise():
    # Using OpenAI to generate a grammar exercise
    completion = client.chat.completions.create(
      model=model_name,
      messages=[
      {"role": "system", "content": "You are a language teacher. your job is to tech people english grammar, via fun and interesting short exercises by sharing with them some fill in the blanks or multiple choice questions. Please give one question only"},
      {"role": "user", "content": "Create a fun grammar exercise (fill in the blanks or multiple choice) based on English language. Please give one question only"}
      ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content.strip()

def check_answer(question, user_answer):
    # Using OpenAI to check the user's answer and provide feedback
    completion = client.chat.completions.create(
      model=model_name,
      messages=[
      {"role": "system", "content": "You are a language teacher. your job is to tech people english grammar. you will be give a question and an answer, both by the user. you have to evaluate it and share feedback. please be supportive and helpful."},
      {"role": "user", "content": f"Question: {question}\nAnswer: {user_answer}\nEvaluate the correctness of the answer and provide feedback: Keep it consize and 2-3 liner"}
      ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content.strip()



def styled_box(content, background="#EAF2F8", text_color="#154360"):
    """Reusable function to create styled sections."""
    return f"""
    <div style="
        background-color: {background}; 
        padding: 15px; 
        border-radius: 10px; 
        text-align: center; 
        font-size: 18px; 
        color: {text_color}; 
        font-weight: bold;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    ">
        {content}
    </div>
    """

def app():
    # Styled Header
    st.markdown(styled_box("📝 Grammar and Fun", "#F8F9F9", "#2E86C1"), unsafe_allow_html=True)

    st.write("")  # Adds some spacing
    st.markdown(
        """<p style="font-size:18px; color:#5D6D7E; text-align:center;">
            Sharpen your grammar skills with interactive exercises and fun challenges!
        </p>""",
        unsafe_allow_html=True
    )

    # State management
    if 'exercise' not in st.session_state:
        st.session_state.exercise = None
    if 'user_response' not in st.session_state:
        st.session_state.user_response = ''

    # Centered Start Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button('🚀 Start Exercise', use_container_width=True):
            st.session_state.exercise = generate_grammar_exercise()

    if st.session_state.exercise:
        st.markdown(styled_box("✏️ Exercise:"), unsafe_allow_html=True)
        st.write(st.session_state.exercise)

        # User input
        st.markdown("<p style='font-size:16px; font-weight:bold; color:#1A5276;'>Your Answer:</p>", unsafe_allow_html=True)
        user_response = st.text_input("", key="response")

        # Centered Check Answer Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button('✅ Check Answer', use_container_width=True):
                if user_response:
                    st.session_state.user_response = user_response
                    feedback = check_answer(st.session_state.exercise, user_response)
                    st.markdown(styled_box("📢 Feedback on Your Answer:", "#D5F5E3", "#186A3B"), unsafe_allow_html=True)
                    st.write(feedback)
                else:
                    st.error("⚠️ Please enter an answer before checking.")

