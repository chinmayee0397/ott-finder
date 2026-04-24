from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


@app.route("/")
def home():
    return {"message": "Movie OTT Finder API is running"}


@app.route("/search")
def search_movie():
    movie_name = request.args.get("movie")

    if not movie_name:
        return jsonify({"error": "Please provide movie name"}), 400

    # Step 1: Search movie
    search_url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": movie_name
    }

    search_res = requests.get(search_url, params=params).json()

    if not search_res.get("results"):
        return {"message": "Movie not found"}

    movie_id = search_res["results"][0]["id"]

    # Step 2: Get OTT providers
    provider_url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
    provider_res = requests.get(provider_url, params={"api_key": API_KEY}).json()

    providers = provider_res.get("results", {}).get("IN", {})

    ott_list = []

    for key in ["flatrate", "rent", "buy"]:
        if key in providers:
            for p in providers[key]:
                ott_list.append(p["provider_name"])

    if not ott_list:
        return {"movie": movie_name, "available_on": "Not available on OTT"}

    return {
        "movie": movie_name,
        "available_on": list(set(ott_list))
    }


if __name__ == "__main__":
    app.run(debug=True)