import streamlit as st # 6740034022 PA4
import pandas as pd
import json
import google.generativeai as genai

st.set_page_config(
    page_title="Lyrics Analyzer & Song Recommender",
    page_icon=":material/queue_music:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# App Title
st.title("⏔⏔⏔ ꒰ ᧔ෆ᧓ ꒱ ⏔⏔⏔         ")
st.title("Lyrics Analyzer & Song Recommender :material/queue_music: ⋆₊˚⊹♡")
st.subheader("""Put in any song lyrics to get insights including:   
1. Lyrics interpretation  
2. Interesting vocabulary & idiom extraction with meanings and example usages  
3. Song recommendations based on lyrical similarity  
""")
st.divider()

# User Input
with st.sidebar:
    st.header("API Key Input")
    API_input = st.text_input(
        "We need your API key to call prompts",
        label_visibility="visible",
        disabled=False,
        placeholder="Enter your API key here",
    )
    st.write(" ⋆｡°✩₊ °✦ ‧  ‧ ₊ ˚✧₊ °✦⋆｡°✩₊ ‧  ‧ ₊ ˚✧₊ ")

left, right = st.columns(2)
with left:
    lyrics_input = st.text_area("Paste your song lyrics below:", height=250)

with right:
    st.space('small')
    with st.container(border=True):
        vocab_num = st.slider('How many vocabulary/idioms do you want to display?', 1, 20, 5)
        song_rec_num = st.slider('How many song recommendations do you want to display?', 1, 20, 5)

if st.button("Submit for Analysis", type="primary"):
    if not lyrics_input.strip():
        st.error("Please paste some lyrics first.")
        st.stop()
    if not API_input.strip():
        st.error("Please enter your API key to proceed.")
        st.stop()

    # LLM Prompt
    genai.configure(api_key=API_input)
    model = genai.GenerativeModel("gemini-2.5-flash-lite")
    prompt = f"""You are a music analyst and language expert.
    Analyze the following song lyrics:
    \"\"\"{lyrics_input}\"\"\"

    Tasks:
    1. Interpretation: A short interpretation of the lyrics (3 to 6 sentences).  
    2. Extraction: Extract {vocab_num} interesting words/idioms from the lyrics.  
    3. Recommendations: Recommend {song_rec_num} songs with similar lyrical themes.  

    Output Requirement:
    You must return ONLY a single valid JSON object. Do not include any conversational text outside the JSON.
    The JSON must follow this exact schema:

    {{
        "interpretation": "String containing the lyrics interpretation text.",
        "vocabulary": [
            {{
                "Word": "The interesting word or idiom",
                "Meaning": "The definition",
                "Example": "A natural example sentence but not from the lyrics"
            }}
        ],
        "recommendations": [
            {{
                "Song": "Song Name",
                "Artist": "Artist Name",
                "Why It Matches": "Why it matches in 1 to 2 sentences"
            }}
        ]
    }}
"""
    # Output
    response = model.generate_content(prompt)
    st.toast("Your lyrics have been analyzed! ✨", icon=":material/queue_music:")

    try:
        json_string = response.text.strip()
        if json_string.startswith('```json'):
            json_string = json_string[7:]
        if json_string.endswith('```'):
            json_string = json_string[:-3]
        data = json.loads(json_string)
    except json.JSONDecodeError:
        st.error("Failed to parse response as JSON. Please try again.")
        st.stop()

    st.subheader("Lyrics Interpretation ⋆𐙚₊˚⊹♡")
    st.write(data.get("interpretation", "No interpretation found."))
    st.divider()

    st.subheader("Vocabulary & Idiom Extraction ⋆𐙚₊˚⊹♡")
    vocab_list = data.get("vocabulary", [])
    if vocab_list:
        vocab_df = pd.DataFrame(vocab_list)
        st.dataframe(vocab_df, hide_index=True)
    else:
        st.info("No vocabulary or idioms were found in the lyrics.")
    st.divider()

    st.subheader("Song Recommendations ⋆𐙚₊˚⊹♡")
    song_rec_list = data.get("recommendations", [])
    if song_rec_list:
        song_rec_df = pd.DataFrame(song_rec_list)
        st.dataframe(song_rec_df, height="stretch", hide_index=True)
    else:
        st.info("No song recommendations were found based on the lyrics.")
    st.divider()

    st.badge("Hope you'll enjoy diving deeper into the lyrics and discovering new favorites!", icon=":material/star_shine:", color="violet", width="stretch")