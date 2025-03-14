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


def generate_random_sentence():
    # Using OpenAI to generate a random sentence (you can specify the language or context here)
    completion = client.chat.completions.create(
      model=model_name,
      messages=[
      {"role": "system", "content": "You are a language teacher. your job is to generate a long sentence in Hindi"},
      {"role": "user", "content": " Please generate a long sentence in hindi, keep it 3-4 liner at max"}
      ]
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content.strip()

def verify_translation(original, translation):
    # Using OpenAI to verify the translation and provide feedback
    completion = client.chat.completions.create(
      model=model_name,
      messages=[
      {"role": "system", "content": "You are a language teacher. your job is to check the translation done by the user from hindi to english. You will be given an original sentence and a translation of it done by the user. You have to point out what is wrong in it, or what can be improved. if everything is fine appreciate the user"},
      {"role": "user", "content": f"Original sentence in hindi: {original},user translation: {translation}. based on the original sentance and the user generated translation guide, tell what is wrong and right in 2-3 liner reponse."}
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
    st.markdown(styled_box("📖 Reading and Translation", "#F8F9F9", "#2E86C1"), unsafe_allow_html=True)

    st.write("")  # Adds spacing
    st.markdown(
        """<p style="font-size:18px; color:#5D6D7E; text-align:center;">
            Test your translation skills by translating the given sentence into English.
        </p>""",
        unsafe_allow_html=True
    )

    # State management
    if 'generated_sentence' not in st.session_state:
        st.session_state.generated_sentence = None
    if 'translation_input' not in st.session_state:
        st.session_state.translation_input = ''

    # Centered Start Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button('🚀 Generate Sentence', use_container_width=True):
            st.session_state.generated_sentence = generate_random_sentence()

    if st.session_state.generated_sentence:
        st.markdown(styled_box("📝 Sentence to Translate:"), unsafe_allow_html=True)
        st.write(st.session_state.generated_sentence)

        # User input for translation
        st.markdown("<p style='font-size:16px; font-weight:bold; color:#1A5276;'>Your Translation:</p>", unsafe_allow_html=True)
        user_translation = st.text_area("", key="translation", height=100)

        # Centered Verify Button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button('✅ Verify Translation', use_container_width=True):
                if user_translation:
                    st.session_state.translation_input = user_translation
                    correction = verify_translation(st.session_state.generated_sentence, user_translation)
                    st.markdown(styled_box("📢 Translation Feedback:", "#D5F5E3", "#186A3B"), unsafe_allow_html=True)
                    st.write(correction)
                else:
                    st.error("⚠️ Please enter a translation before verifying.")


