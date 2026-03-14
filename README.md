# CodeAlpha Internship Platform

Simple web app for translating text and searching CodeAlpha FAQs.

## Setup (Do This First)

### Step 1: Open Terminal
Navigate to the `Code_Alpha` folder in your terminal.

```bash
cd Code_Alpha
```

### Step 2: Create Virtual Environment
Make a clean Python environment so dependencies don't mix with other projects.

**Windows:**
```bash
python -m venv venv
```

**Mac/Linux:**
```bash
python3 -m venv venv
```

### Step 3: Activate Virtual Environment
Before installing anything, activate the environment.

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line now.

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- streamlit (web interface)
- deep-translator (translation - works with Python 3.13+)
- gTTS (text-to-speech)
- scikit-learn (pattern matching)
- nltk (language processing)

Wait for everything to finish.

## Run the App

With your virtual environment activated, run:

```bash
streamlit run app.py
```

Your browser should open automatically to `http://localhost:8501`

If it doesn't, go to that URL manually.

## Using the App

### 📝 Translator Tab
1. Pick "From" language and "To" language
2. Paste or type text
3. Click "Translate"
4. Listen to audio (if it works)

Supports: English, Spanish, French, German, Italian, Portuguese, Japanese, Korean, Chinese, Hindi, Russian, Arabic, Thai

### ❓ FAQ Tab
1. Type a question about CodeAlpha
2. Click "Search FAQ"
3. Get an answer

Check the "View available questions" dropdown to see what you can ask about.

## Troubleshooting

**"No module named deep_translator"**
- Make sure your venv is activated (you should see `(venv)` in terminal)
- Run `pip install -r requirements.txt` again

**Translation/Audio doesn't work**
- Check your internet connection
- Google Translate API might be rate-limited

**"Port 8501 already in use"**
- Streamlit is already running. Close the browser tab and terminal running Streamlit
- Wait a few seconds, then run `streamlit run app.py` again

## Stop the App

Press `Ctrl + C` in the terminal.

## File Info

- `app.py` - The whole app
- `faqs.json` - Questions and answers database
- `requirements.txt` - What Python packages to install
- `venv/` - Virtual environment folder (created when you run python -m venv venv)

## Questions?

Email: support@codealpha.ai

Slack: #intern-support


