import pandas as pd
import openai
import os
import sys
from dotenv import load_dotenv

# Load your OpenAI API key
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Load dataset
df = pd.read_csv("animated_movie_dataset_ethical_emotional_tag_formatted.csv")
df['ethical_values_clean'] = df['ethical_values_clean'].str.lower()
df['emotional_theme_clean'] = df['emotional_theme_clean'].str.lower()

# Define allowed tags
ethical_set = {
    "kindness", "courage", "family", "friendship", "freedom", "perseverance",
    "self-acceptance", "empathy", "resilience", "responsibility", "justice", "loyalty"
}
emotional_set = {
    "heartwarming", "high-energy", "dream-driven", "bittersweet",
    "pure fun", "family bonding", "heroic quest"
}

# 🎬 Start interaction
print("🎬 Welcome to the Animated Movie Recommender!")
print("✨ This AI assistant will recommend animated gems based on the values you believe in and the emotions you want to feel.")
print("\n🔍 Step 1: Choose 1–3 **ethical values** that matter to you:")
print("Examples: kindness, courage, family, friendship, freedom, perseverance,self-acceptance, empathy, resilience, responsibility, justice, loyalty")
user_input_ethical = input("\n💬 Enter ethical values (comma-separated): ").lower()
if user_input_ethical==' ':
    user_input_ethical = input("😞 No input provided. Please enter at least one ethical value.").lower()
 

if user_input_ethical not in ethical_set:
    user_input_ethical = input( "Re-enter value from following:" \
    "Examples: kindness, courage, family, friendship, freedom, perseverance,self-acceptance, empathy, resilience, responsibility, justice, loyalty")

print("\n🎭 Step 2: What emotional experience are you looking for in a movie?")
print("Examples: heartwarming, high-energy, dream-driven, bittersweet, pure fun, family bonding, heroic quest")
user_input_emotional = input("\n💬 Enter emotional tones (comma-separated): ").lower()
if user_input_emotional==' ':
    user_input_emotional = input("😞 No input provided. Please enter at least one emotional tone.").lower()

if user_input_emotional not in emotional_set:
    user_input_emotional = input("Re-enter value from following:" \
    "Examples: heartwarming, high-energy, dream-driven, bittersweet, pure fun, family bonding, heroic quest")

print("\n🔍 Finding matches based on your values...\n")

# Parse and clean inputs
terms_eth = [term.strip() for term in user_input_ethical.split(",")]
terms_em = [term.strip() for term in user_input_emotional.split(",")]



# # Validate inputs
ethical_values = [t for t in terms_eth if t in ethical_set]
# print("You have entered ethical values:", ethical_values)
emotional_tones = [t for t in terms_em if t in emotional_set]
# print("You have entered emotional tones:", emotional_tones)
if(ethical_values==[]):
    print("😞 No valid ethical values found. Please try again with valid values.")
    sys.exit(1)
if(emotional_tones==[]):
    print("😞 No valid emotional tones found. Please try again with valid tones.")
    sys.exit(1)

# Apply flexible filtering
ethical_mask = df['ethical_values_clean'].apply(lambda ev: any(val in ev for val in ethical_values)) if ethical_values else True
emotional_mask = df['emotional_theme_clean'].apply(lambda et: any(tone in et for tone in emotional_tones)) if emotional_tones else True

filtered_df = df[ethical_mask & emotional_mask]

# Handle no matches
if filtered_df.empty:
    print("😞 No movies found matching your criteria on my dataset but wait, Let's find some alternatives!")
    fallback_prompt = f"""
You are a movie recommendation assistant.

The user is seeking animated movies that reflect the following:

- Ethical Values: {', '.join(ethical_values)}
- Emotional Tones: {', '.join(emotional_tones)}

Since there are no direct dataset matches, recommend:
- 2 Popular Picks 🎯 (widely loved, high IMDb or box office)
- 2 Hidden Gems 💎 (lesser-known, but deeply matching user's values)

- A one-line thematic heading like: "Here’s a {', '.join(emotional_tones)} animated movie that beautifully explores the theme of {', '.join(ethical_values)}:"
For each movie:

1. 🎬 Title (Year)
2. Studio, Language, IMDb Rating, and Duration
3. A 2–3 line "Why It Fits" explaining its connection to the ethical values and emotional tones
4. A bullet list: "You’ll Love It If You Enjoy…"
5. End each with its Popularity Tag (Highly Popular, Popular among few, or Niche Audience)

Use clear plain text formatting (no markdown or asterisks).

Avoid generic suggestions. Make sure to align with user's emotional and ethical input.
"""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": fallback_prompt}]
    )
    print("\n🎬 Final Recommendations:\n")
    print(response.choices[0].message.content.strip())

else:
    # Prepare dataset summary
    movie_details_text = "\n\n".join([
        f"{row['title']} ({row['release_year']})\n"
        f"Studio: {row['production_companies'] if pd.notna(row['production_companies']) else 'N/A'}\n"
        f"Language: {row.get('language', 'English')}\n"
        f"{'IMDb Rating:' + str(row['rating']) if row['rating'] and row['rating']>0 else 'N/A' }\n"
        f"Duration: {row.get('runtime', 'N/A')} mins\n"
        f"Overview: {row.get('overview', '')}"
        for _, row in filtered_df.head(5).iterrows()
    ])

    gpt_prompt = f"""
You are a friendly animated movie recommendation assistant.

Below is a list of animated movies from the user's dataset that align with their preferences:

Ethical Values: {', '.join(ethical_values)}
Emotional Tones: {', '.join(emotional_tones)}

Below is a list of selected movies from the user's own dataset. Each movie includes:
- Title
- Release Year
- Studio
- Language
- IMDb Rating
- Duration
- Overview


🎬 List of movies:

{movie_details_text}

Instructions:
- Label each movie as either:
   - Popular Pick 🎯 → (widely loved, high IMDb or highly popular)
   - Hidden Gem 💎 → (lesser-known, but deeply matching user's values)
- Select 2 movies which is Popular Pick 🎯 and 2 movies which is Hidden Gem 💎 from the above list.
 
- A one-line thematic heading like: "Here’s a {', '.join(emotional_tones)} animated movie that beautifully explores the theme of {', '.join(ethical_values)}:"
- For each movie, generate:

1. 🎬 Title (Year) 
2. Studio if nan dont return subheading ,IMDb Rating, and Duration
3. A 2–3 line "Why It Fits" explaining its connection to the ethical and emotional theme
4. A bullet list: "You’ll Love It If You Enjoy…"
5. End each with its Popularity Tag (Highly Popular, Popular among few, or Niche Audience)

Use clear plain text formatting (no markdown or asterisks).
"""

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": gpt_prompt}]
    )

    print("\n🎬 Final Recommendations:\n")
    print(response.choices[0].message.content.strip())

