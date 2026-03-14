# my first streamlit project
# CodeAlpha Internship Platform
# Simple translation tool + FAQ search

import streamlit as st
import json
import io
import random
from deep_translator import GoogleTranslator
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from gtts import gTTS
import numpy as np

# basic page setup
st.set_page_config(page_title="CodeAlpha", page_icon="📚", layout="wide")

# languages i support
# using language codes that deep-translator understands
LANGUAGES = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Chinese': 'zh-CN',
    'Hindi': 'hi',
    'Russian': 'ru',
    'Arabic': 'ar',
    'Thai': 'th'
}

# ========== TASK 1: TRANSLATION ==========

def translate_text(text, from_lang, to_lang):
    # use deep translator (better than googletrans for python 3.13+)
    try:
        translator = GoogleTranslator(source_language=from_lang, target_language=to_lang)
        result = translator.translate(text)
        return result, True
    except Exception as e:
        print(f"Translation error: {e}")
        return None, False


def make_audio(text, lang_code):
    # convert text to speech
    try:
        speech = gTTS(text=text, lang=lang_code)
        audio_file = io.BytesIO()
        speech.write_to_fp(audio_file)
        audio_file.seek(0)
        return audio_file, True
    except:
        return None, False


def show_translator():
    st.header("🌍 Translator")
    st.write("Translate text to other languages")
    
    col1, col2 = st.columns(2)
    
    with col1:
        source_lang = st.selectbox("Translate from:", list(LANGUAGES.keys()))
    with col2:
        target_lang = st.selectbox("Translate to:", list(LANGUAGES.keys()))
    
    # text input
    text_to_translate = st.text_area("Enter text:", height=100)
    
    if st.button("Translate", use_container_width=True):
        if not text_to_translate.strip():
            st.warning("Please enter some text")
        elif source_lang == target_lang:
            st.info("Pick different languages")
        elif len(text_to_translate) > 5000:
            st.warning("Text too long (max 5000 characters)")
        else:
            with st.spinner("Translating..."):
                translated, success = translate_text(
                    text_to_translate,
                    LANGUAGES[source_lang],
                    LANGUAGES[target_lang]
                )
            
            if success:
                st.success("Done!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Your text:**")
                    st.write(text_to_translate)
                with col2:
                    st.write("**Translation:**")
                    st.write(translated)
                
                # try to add audio
                with st.spinner("Making audio..."):
                    audio, audio_ok = make_audio(translated, LANGUAGES[target_lang])
                
                if audio_ok:
                    st.audio(audio, format="audio/mp3")
                else:
                    st.info("Couldn't make audio, but translation worked")
            else:
                st.error("Translation failed. Check internet")


# ========== TASK 2: FAQ SEARCH ==========

def load_faq():
    # read the faq file
    try:
        with open('faqs.json', 'r') as f:
            return json.load(f)
    except:
        return {"intents": []}


def build_patterns(intents):
    # flatten all patterns from faqs
    all_patterns = []
    pattern_to_tag = {}
    tag_responses = {}
    
    for intent in intents:
        tag = intent.get('tag')
        responses = intent.get('responses', [])
        tag_responses[tag] = responses
        
        for pattern in intent.get('patterns', []):
            idx = len(all_patterns)
            all_patterns.append(pattern.lower())
            pattern_to_tag[idx] = tag
    
    return all_patterns, pattern_to_tag, tag_responses


def find_answer(question, vectorizer, pattern_matrix, pattern_map, response_map):
    # compare question to all faq patterns
    question_vec = vectorizer.transform([question.lower()])
    scores = cosine_similarity(question_vec, pattern_matrix).flatten()
    
    best_idx = np.argmax(scores)
    best_score = scores[best_idx]
    
    # if match is good enough, return answer
    if best_score > 0.25:
        tag = pattern_map[best_idx]
        answers = response_map[tag]
        return random.choice(answers)
    else:
        # no good match
        fallback = [
            "Hmm, I'm not sure about that. Try asking something else.",
            "That's not in my knowledge base. Email support@codealpha.ai",
            "Can you rephrase that?",
            "Not sure, maybe check the internship portal?"
        ]
        return random.choice(fallback)


def show_faq():
    st.header("❓ FAQ Search")
    st.write("Ask questions about CodeAlpha internship")
    
    # load faq data
    faq_data = load_faq()
    intents = faq_data.get('intents', [])
    
    if not intents:
        st.error("No FAQ data found")
        return
    
    # build patterns
    patterns, pattern_map, response_map = build_patterns(intents)
    
    if not patterns:
        st.error("No patterns in FAQ")
        return
    
    # setup vectorizer
    vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
    pattern_matrix = vectorizer.fit_transform(patterns)
    
    # show available questions
    with st.expander("View available questions"):
        for intent in intents:
            st.write(f"**{intent.get('tag')}:**")
            for p in intent.get('patterns', [])[:3]:  # show first 3
                st.write(f"- {p}")
            if len(intent.get('patterns', [])) > 3:
                st.write(f"... and {len(intent.get('patterns', [])) - 3} more")
    
    # search
    st.write("---")
    question = st.text_input("Type your question:")
    
    if st.button("Search FAQ", use_container_width=True):
        if not question.strip():
            st.warning("Please ask a question")
        else:
            answer = find_answer(question, vectorizer, pattern_matrix, pattern_map, response_map)
            st.info(f"**Answer:** {answer}")


# ========== MAIN APP ==========

def main():
    # sidebar navigation
    st.sidebar.title("CodeAlpha")
    st.sidebar.write("Internship Platform")
    st.sidebar.write("---")
    
    page = st.sidebar.radio(
        "Pick a tool:",
        ["Translator", "FAQ Search"]
    )
    
    st.sidebar.write("---")
    st.sidebar.write("""
        **About**
        
        12-week AI internship program. Learn machine learning and work on real projects.
        
        **Questions?**
        
        Email: support@codealpha.ai
        
        Slack: #intern-support
    """)
    
    # show the right page
    if page == "Translator":
        show_translator()
    else:
        show_faq()


if __name__ == "__main__":
    main()


