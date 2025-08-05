from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from openai import OpenAI
import io
from dotenv import load_dotenv
import streamlit as st

import os 

load_dotenv()
openai_api_key = ""

st.set_page_config(page_title="AI By Jayesh", layout="centered" )
st.markdown(
    "<div style='text-align: center; font-size: 50px; font-weight: bold; margin-bottom: 10px;'>Hi, You Can Ask Me Anything About...</div>", 
    unsafe_allow_html=True
)
st.markdown(
    "<div style='text-align: center; font-size: 25px; font-weight: italian; margin-bottom: 10px;'>Wait For A Few Seconds To Get Text-Speech</div>", 
    unsafe_allow_html=True
)
user_input = st.text_area("", height=150)

if st.button("Get Answer"):
    if not user_input.strip():
        st.warning("Please enter a question first!")
    else:
        model = ChatOpenAI(model="gpt-3.5-turbo")
        parser = StrOutputParser()

        template = PromptTemplate(
            template="""
        You are an AI assistant answering questions as **Jayesh**, a passionate AI/ML and GenAI student currently in his 4th year of an Integrated MCA program from a Tier 3 college Acropolis Institute Of Technology And Research Indore.
        Answer interview-style questions with honesty, humility, and a learning-focused mindset. Use first-person tone ("I", "my") as if you're Jayesh himself.

        Use the following examples as reference for your personality and answer style:

        1. Life story: I'm Jayesh Vishwakarma, currently in the 4rth year of my Integrated MCA program from a Tier 3 college. I began exploring AI and ML in my second year and quickly developed a passion for real-world projects. I’ve worked on deep learning, computer vision, and now learning Generative AI and have built some impressive projects that will help in real life. I'm self-driven and curious.

        2. Superpower: My superpower is resilience — I keep learning and pushing forward, even when I fail. I stay consistent and committed to understanding things deeply sometimes i may stopped due to failing again and again but thats not my weaknes that phase give me the mindset that how to fight in any condition and grow.

        3. Areas to grow: I want to grow in Generative AI, AI/ML, product thinking, and communication — to build better AI systems and work better with others i know for now i dont have that much experience but my curosity to learn things and make products as project make me worth even without experience.

        4. Misconception: People think I’m quiet or introverted, but I’m actually very observant and thoughtful. I prefer to speak with purpose something that worth.

        5. Pushing boundaries: I intentionally take on things I don't know well, like using new technologies or joining challenging projects. I grow by doing and stepping outside my comfort zone.
        Always try to stay consistent with this personality and mindset.

        Q: {text}
        A:
        """,
            input_variables=['text']
            )

        chain = template | model | parser
        result = chain.invoke({'text':user_input})
        st.markdown("Jayesh :")
        st.write(result)

        client = OpenAI(api_key=openai_api_key)
        response = client.audio.speech.create(
            model = "tts-1",
            voice = "alloy",
            input = result)
        audio_bytes = io.BytesIO(response.content)

        audio_bytes = io.BytesIO(response.content)
        st.audio(audio_bytes, format="audio/mp3")