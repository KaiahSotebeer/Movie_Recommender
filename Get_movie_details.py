import requests

TMDB_TOKEN = "YOUR_TMDB_READ_ACCESS_TOKEN"


def get_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    headers = {
        "Authorization": f"Bearer {TMDB_TOKEN}",
        "accept": "application/json"
    }

    params = {
        "language": "en-US"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params,
        timeout=10
    )

    response.raise_for_status()
    return response.json()


movie = get_movie_details(11)

print("Title:", movie["title"])
print("Release date:", movie["release_date"])
print("Description:", movie["overview"])
print("Runtime:", movie["runtime"], "minutes")
print("Genres:", ", ".join(g["name"] for g in movie["genres"]))
print("IMDb ID:", movie["imdb_id"])