import streamlit as st
import requests
import numpy as np
import sounddevice as sd
import wave
from openai import AzureOpenAI
from dotenv import load_dotenv
import os
import time

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


def speech_to_text(file_path):
    audio_file= open(file_path, "rb")
    transcription = client.audio.transcriptions.create(
      model="whisper-1",
      file=audio_file
    )
    print("transcript:")
    print(transcription.text)
    return transcription.text


def describe_image(image_url):
    response = client.chat.completions.create(
      model=model_name,
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "describe this image like in an IELTS exam. Keep it consize and within 50 words"},
            {
              "type": "image_url",
              "image_url": {
                "url": image_url,
              },
            },
          ],
        }
      ],
      max_tokens=300,
    )
    print("Chat GPT:")
    print(response.choices[0].message.content)
    return response.choices[0].message.content



def compare_descriptions(model_desc, user_desc):
    st.write(f" Description: {model_desc}")
    st.write(f"Your Description: {user_desc}")
    completion = client.chat.completions.create(
      model=model_name,
      messages=[
      {
          "role": "system", 
          "content": "You are a language teacher. you have a predefined description of an image, and also a user written dscription. you just have to judge the language, grammer and vocabolary of the user provided description. keep in mind that the user is a beginner so be supportive and helpful."},
      {
          "role": "user", 
          "content": f"Description: {model_desc},user Description: {user_desc}. based on these two respond what all the user can improve in their description of the image, keep it consize and to the point and 2-3 liner."}
      ]
    )

    print(completion.choices[0].message.content)
    st.markdown("### 📝 Feedback & Analysis")
    st.markdown(
        f"""
        <div style="
            background-color: #F8F9FA; 
            padding: 15px; 
            border-radius: 10px; 
            font-size: 16px; 
            color: #34495E; 
            font-weight: 500;
            box-shadow: 1px 1px 8px rgba(0,0,0,0.1);
        ">
            <b>🔍 Analysis:</b> {completion.choices[0].message.content.strip()}
        </div>
        """,
        unsafe_allow_html=True
    )


def styled_section(title, description):
    """Reusable function for rendering styled sections"""
    st.markdown(
        f"""
        <div style="
            background-color: #F8F9F9; 
            padding: 15px; 
            border-radius: 10px; 
            text-align: center; 
            font-size: 22px; 
            font-weight: bold; 
            color: #2E86C1; 
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        ">
            {title}
        </div>
        <p style="font-size:18px; color:#5D6D7E; text-align:center;">
            {description}
        </p>
        """,
        unsafe_allow_html=True
    )


def centered_button(label, key):
    """Reusable function for rendering centered buttons"""
    st.markdown("<div style='display: flex; justify-content: center;'>", unsafe_allow_html=True)
    return st.button(label, key=key, use_container_width=False)

def app():
    # Section Header
    styled_section("📷 Image Comprehension", "Learn to understand and describe images in your target language. This task focuses on improving your speaking skills and vocabulary.")

    # Initialize session state variables
    if 'image_shown' not in st.session_state:
        st.session_state.image_shown = False
    if 'recording_started' not in st.session_state:
        st.session_state.recording_started = False

    # Centered Start Button
    if centered_button('🚀 Start', "start-button"):
        st.session_state.image_shown = True
        st.session_state.image_generated = False

    if st.session_state.image_shown:
        # Fetch and display the image
        if not st.session_state.get("image_generated", False):
            url = "https://picsum.photos/1280/720"
            try:
                response = requests.get(url, verify=False)
                if response.status_code == 200:
                    st.session_state.image_url = response.url
                    st.session_state.image_generated = True
            except requests.exceptions.RequestException as e:
                st.error(f"Error fetching image: {e}")

        if "image_url" in st.session_state:
            st.image(st.session_state.image_url, caption="📸 Describe this image", use_container_width=True)

            # Styled Instructions
            styled_section(
                "🗣️ Describe the Image",
                "Take a moment to analyze the image carefully. Think about what you want to say before you begin.<br>"
                "⏳ You will have <span style='color: #D35400;'>30 seconds</span> to speak.<br>"
                "Focus on <b>clear description</b> and <b>fluid speech</b>."
            )

            # Centered Recording Button
            if centered_button("🎙️ Start Talking", "record-button"):
                st.session_state.recording_started = True
                duration = 3  # seconds
                sample_rate = 44100  # Sample rate

                progress_bar = st.progress(0)
                st.write("🎤 Recording in progress... Speak now!")

                myrecording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="int16")

                for i in range(duration):
                    time.sleep(1)  # Simulate real-time recording progress
                    progress_bar.progress((i + 1) / duration)

                sd.wait()  # Wait until recording is finished
                progress_bar.empty()  # Remove progress bar after recording completes

                st.session_state.recording_started = False
                st.success("✅ Recording Done!")

                # Save audio
                output_file = "output2.wav"
                with wave.open(output_file, "w") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(sample_rate)
                    wf.writeframes(myrecording.tobytes())

                st.info(f"🎧 Audio saved!")

                # Process speech
                user_description = "This picture shows a sunset. The sun is bright and orange. There is a fence in front. Below the fence, there is a road. Cars are driving on the road. Trees are seen on the side. The sky has colors like blue"
                model_description = describe_image(st.session_state.image_url)
                compare_descriptions(model_description, user_description)
