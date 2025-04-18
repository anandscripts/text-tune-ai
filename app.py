import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API")
genai.configure(api_key=api_key)

# Load the Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

# Response generation function
def response(prompt):
    final_text = model.generate_content(prompt)
    return final_text.text

# Prompt templates
prompt_templates = {
    "Summarize": "Summarize the following text in a concise and clear way:\n\n{}",
    "Paraphrase / Rephrase": "Rephrase the following text without changing its original meaning:\n\n{}",
    "Grammar & Spell Check": "Correct any grammar or spelling mistakes in the following text:\n\n{}",
    "Text Expansion": { 
        "Add a line": "Add one more meaningful sentence to expand the idea in the following text:\n\n{}",
        "Paragraph": "Expand the following text into a full, coherent paragraph:\n\n{}"
    },
    "Tone Adjustment": {
        "Professional": "Rewrite the following text in a professional tone suitable for workplace or formal communication:\n\n{}",
        "Friendly": "Rewrite the following text in a friendly and approachable tone:\n\n{}",
        "Empathetic": "Rewrite the following text in an empathetic tone that shows care and understanding:\n\n{}"
    }
}

# Page config
st.set_page_config(page_title="Text Tune", layout="centered", page_icon='📝')
st.title("📝 AI Text Modifier")

# ---- Layout: 3 columns for options and 1 for text ----
col1, col2, col3 = st.columns([4, 4, 2])
# col4 = st.container()  # for input & output

# Column 1 - Main option
with col1:
    task = st.selectbox(
        "Modification Type",
        ["Summarize", "Paraphrase / Rephrase", "Grammar & Spell Check", 
         "Text Expansion", "Tone Adjustment"]
    )

# Column 2 - Tone sub-options (only if tone selected)
sub_option = None
with col2:
    if task == "Tone Adjustment":
        sub_option = st.selectbox(
            "Tone Type",
            ["Professional", "Friendly", "Empathetic"]
        )
    elif task == "Text Expansion":
        sub_option = st.selectbox(
            "Expansion Type",
            ["Add a line", "Paragraph"]
        )
    else:
        st.markdown("")

# Column 3 - Modify button
with col3:
    st.write('')
    st.write('')
    modify_button = st.button("🔁 Submit")

# Input text area
user_text = st.text_area("✍️ Enter your text here:", height=200)

# Output text block
if modify_button:
    if not user_text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Thinking..."):
            if task == "Tone Adjustment" or task == "Text Expansion":
                prompt_text = prompt_templates[task][sub_option].format(user_text)
            else:
                prompt_text = prompt_templates[task].format(user_text)

            output = response(prompt_text)

        # Display result in a styled container with copy button
        st.write('---')
        st.markdown("#### Modified Text")
        st.code(output, language="markdown", wrap_lines=True)
