import streamlit as st
import requests

st.title("🎬 Movie OTT Finder")

movie_name = st.text_input("Enter movie name")

BASE_URL = "http://127.0.0.1:5000"  # change later after deploy

if st.button("Search"):
    if movie_name:
        try:
            response = requests.get(
                f"{BASE_URL}/search",
                params={"movie": movie_name}
            )

            data = response.json()

            if "available_on" in data:
                st.success(f"Movie: {data['movie']}")

                if isinstance(data["available_on"], list):
                    st.write("Available on:")
                    for ott in data["available_on"]:
                        st.write(f"- {ott}")
                else:
                    st.warning(data["available_on"])

            elif "message" in data:
                st.warning(data["message"])

            else:
                st.error("Something went wrong")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a movie name")