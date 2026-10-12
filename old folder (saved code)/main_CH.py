
#Notes on next to-dos (vs 1 B):
#I need to add the "relaxer" button somewhere - so far my test searches are often not coming up with results... a relaxer button could help still provide a close recommendation
#I also need to figure out how to print more pages if needed. 
#I have genres as a dict, but I could index them elsewhere?


#assigning dict for genre names -> to TMBD number labels from the TMBD movie info page. (P.S. thanks so much for sending that to me, Dr. Harding! It helped a lot.)
genres = {
    "Action": 28,
    "Adventure": 12,
    "Animation": 16,
    "Comedy": 35,
    "Crime": 80,
    "Documentary": 99,
    "Drama": 18,
    "Fantasy": 14,
    "Horror": 27,
    "Mystery": 9648,
    "Romance": 10749,
    "Science Fiction": 878,
    "Thriller": 53
}

#Below I am defining get_user_preferences to ask for genre, rating, and year
#Building preferences (base) - block
user_name = input("Enter your name: ")
def get_user_preferences(name):
    print (f"Hello {name}, welcome to Movie Recommender")

    #Getting genre selection from the user, eventually I'd like this to be a dropdown menu on streamlit.
    genre_choice = input("Enter your genre(s) of interest")

    #Getting year selection from the user - again, I'd like this to be in streamlit.
    year_choice_start = int(input("Enter the start year"))
    year_choice_end = int(input("Enter the end year"))

    #Asking user for rating
    rating_choice = float(input("Enter the average rating of the film"))

    #preferences are stored and eventually given to the API(?)
    preferences = {
        "genre_choice": genre_choice ,
        "year_choice_start": year_choice_start ,
        "year_choice_end": year_choice_end ,
        "rating_choice": rating_choice ,
    }
    return preferences

preferences = get_user_preferences(user_name)

#Searching the api based on user preferences - below I used part of the code example generated from feedback from my light spec? Hopefully it works. 
from keys import tmdb_api

def get_genre_ids(genre_text):
    # Convert typed genre name(s), e.g. "Comedy, Drama", to TMDB genre ids; unknown names are skipped
    names = [g.strip().title() for g in genre_text.split(",")]
    return [genres[name] for name in names if name in genres]

def search_tmdb(preferences):
    import os
    import requests


    url = "https://api.themoviedb.org/3/discover/movie"

    # tmdb_api is a v4 read access token, so it is sent as a Bearer header (not as api_key)
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {tmdb_api}",
    }
    parameters = {
                "with_genres": ",".join(str(g) for g in get_genre_ids(preferences["genre_choice"])),
                "release_date.gte": f"{preferences['year_choice_start']}-01-01",
                "release_date.lte": f"{preferences['year_choice_end']}-12-31",
                "vote_average.gte": preferences["rating_choice"] ,
            }
    response = requests.get(url, params=parameters, headers=headers)
    response.raise_for_status()
    return response.json()
    
movies = search_tmdb(preferences)["results"]

#Third block below, using the pulled information from user preferences and the API search to filter out unrelated movies.
def filter_movies(movies, preferences):
    yes_movies = list(movies)

    #filter by voter rating
    yes_movies = [m for m in yes_movies if float(m["vote_average"]) >= preferences["rating_choice"]]
    if not yes_movies:
        print("No movie could be found with your selected average rating")
        return yes_movies

    #Now moving to release date - slicing to avoid exact dates/months. Some movies have an empty release_date.
    yes_movies = [m for m in yes_movies
                  if m.get("release_date")
                  and preferences["year_choice_start"] <= int(m["release_date"][0:4]) <= preferences["year_choice_end"]]
    if not yes_movies:
        print("No movie could be found with your selected release year")
        return yes_movies

    #genre choice below - keep movies matching at least one chosen genre
    genre_ids = get_genre_ids(preferences["genre_choice"])
    if genre_ids:
        yes_movies = [m for m in yes_movies if any(g in m["genre_ids"] for g in genre_ids)]
    if not yes_movies:
        print("No movie could be found with your selected genre")
    return yes_movies

#Sorting displayed movies by TMBD voter average, highest first
def get_rating(movie):
    return movie["vote_average"]

def sort_movies(yes_movies):
    return sorted(yes_movies, key=get_rating, reverse=True)

#Now displaying results
def display_movies(sorted_movies):
    for movie in sorted_movies:
        print(f'{movie["title"]} - rating {movie["vote_average"]} - released {movie.get("release_date", "unknown")}')

display_movies(sort_movies(filter_movies(movies, preferences)))
