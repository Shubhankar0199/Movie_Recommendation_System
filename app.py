import streamlit as st
import time

from utils.recommender import recommend, get_movie_suggestions

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Movie Recommendation Assistant",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------
# LOAD CSS
# ---------------------------------------------------

with open("styles/style.css") as css:
    st.markdown(f"<style>{css.read()}</style>", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("🎬 Movie Assistant")

    st.write("Welcome!")

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Hello 👋\n\nTell me your favourite movie."
            }
        ]

        st.rerun()

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🎬 AI Movie Recommendation Assistant")
st.caption("Discover movies similar to your favourites.")

# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello 👋\n\nTell me your favourite movie."
        }
    ]

# ---------------------------------------------------
# DISPLAY CHAT
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------------------------------------------
# USER INPUT
# ---------------------------------------------------

prompt = st.chat_input("Enter movie name...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        try:

            recommendations = recommend(prompt)

            if recommendations is None or recommendations.empty:

                suggestions = get_movie_suggestions(prompt)

                response = "❌ Movie not found.\n\n"

                if suggestions:

                    response += "Did you mean:\n\n"

                    for movie in suggestions:
                        response += f"• {movie}\n"

                else:

                    response += "Please try another movie."

            else:

                response = f"🎬 **Movies similar to '{prompt}'**\n\n"

                for _, movie in recommendations.iterrows():

                    response += f"""
### 🍿 {movie['title']}

⭐ **Rating:** {movie['vote_average']}

🎭 **Genre:** {movie['genres']}

📝 **Tagline:** {movie['tagline']}

📖 **Overview:**

{movie['overview']}

---

"""

        except Exception as e:

            response = f"❌ Error: {e}"

        full_text = ""

        for word in response.split():

            full_text += word + " "

            placeholder.markdown(full_text + "▌")

            time.sleep(0.02)

        placeholder.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )