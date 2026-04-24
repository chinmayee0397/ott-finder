import streamlit as st
import requests

# Your deployed backend URL (Render)
BASE_URL = "https://ott-finder.onrender.com"

st.set_page_config(page_title="Movie OTT Finder", page_icon="🎬")

st.title("🎬 Movie OTT Finder")
st.write("Search any movie to find where it's available on OTT platforms")

# Input box
movie_name = st.text_input("Enter movie name")

# Button click
if st.button("Search"):

    if not movie_name.strip():
        st.warning("Please enter a movie name")
    else:
        try:
            with st.spinner("Searching movie..."):
                response = requests.get(
                    f"{BASE_URL}/search",
                    params={"movie": movie_name}
                )

            if response.status_code != 200:
                st.error("Backend error. Please try again.")
            else:
                data = response.json()

                # Movie found with OTT
                if "available_on" in data and isinstance(data["available_on"], list):
                    st.subheader(f"🎬 {data['movie']}")
                    st.success("Available on:")

                    for ott in data["available_on"]:
                        st.write(f"🍿 {ott}")

                # Movie not found / not available
                else:
                    msg = data.get("message", "Not available on OTT platforms")
                    st.warning(msg)

        except Exception as e:
            st.error(f"Something went wrong: {e}")