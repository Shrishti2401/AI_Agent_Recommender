# 🎬 AI Animated Movie Recommender

An intelligent movie recommendation agent that suggests animated films based on **ethical values** and **emotional tones** using a mix of curated dataset filtering and GPT-powered fallbacks.

---

## 📁 Repository Contents

- `ai_recommender.py` – Core Python script for filtering dataset, invoking GPT, and generating styled recommendations.
- `animated_movie_dataset_ethical_emotional_tag_formatted.csv` – Cleaned and tagged dataset of 9,000+ animated movies with ethical and emotional value labels.
- `Animated_Movie_Recommender_Documentation.docx` – Final project report with prompt design, flow diagrams, testing logs, and full explanation.
- `output.txt` – Raw logs showing sample inputs, outputs, and test cases.

---

## 🔍 What This Agent Does

- Accepts user inputs like:  
  _Ethical Values:_ `courage`, `freedom`, `kindness`, etc.  
  _Emotional Tones:_ `bittersweet`, `heartwarming`, `dream-driven`, etc.
- Filters a rich movie dataset based on those values.
- If matching movies are found, it sends them to GPT for natural-language styled recommendations.
- If no matches are found, GPT fallback prompt suggests great alternatives — with "Popular Pick 🎯" or "Hidden Gem 💎" tags.

---

## 🚧 Ongoing Work

- **Project Title**: [Value-Based-Recommender-System-for-User-Entertainment](https://github.com/Shrishti2401/Value-Based-Recommender-System-for-User-Entertainment)
- Goal: Build a fully-deployed web chatbot (using Streamlit) for ethical and emotional storytelling-based discovery.
- Upcoming:  
  - Add user input UI  
  - Deploy to web  
  - Integrate real-time GPT output  
  - Handle rate-limiting, re-runs, and feedback loop

---

## 🧠 Built With

- Python (pandas, openai)
- OpenAI GPT-3.5 Turbo
- Local CSV dataset
- Word documentation + prompt design
