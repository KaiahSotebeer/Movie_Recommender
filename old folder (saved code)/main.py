
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
def search_tmdb(preferences):
    import os
    import requests

    API_TOKEN = tmdb_api

    url = "https://api.themoviedb.org/3/discover/movie"

    headers = {
        "accept": "application/json",
    }
    parameters = {
                "api_key": API_TOKEN,
                "with_genres": preferences["genre_choice"],
                "release_date.gte": preferences["year_choice_start"] ,
                "release_date.lte": preferences["year_choice_end"],
                "vote_average.gte": preferences["rating_choice"] ,
            }
    response = requests.get(url, params=parameters, headers=headers)
    return response.json()
    
movies = search_tmdb(preferences)
print(movies)

#Third block below, using the pulled information from user preferences and the API search to filter out unrelated movies.
#filter by voter rating
def filter_movies(movies, preferences, genres):
    yes_movies = []
    for movie in movies:
        if float(movie["vote_average"]) >= float(preferences["rating_choice"]):
            yes_movies.append(movie)

    if yes_movies == []:
        print("No movie could be found with your selected average rating")
    else:
        return yes_movies
#Now moving to release date - slicing to avoid exact dates/months. I don't think many people would use that feature anyway...
    for movie in movies:
        if int(movie["release_date"][0:4]) >= preferences["year_choice_start"] and int(movie["release_date"][0:4]) <= preferences["year_choice_end"]:
            yes_movies.append(movie)

    if yes_movies == []:
        print("No movie could be found with your selected release year")
    else:
        return yes_movies
#genre choice below
    for movie in movies:
        match = False
        for genres in preferences["genre_choice"]:
                if genres in movie["genre_ids"]:
                    match = True
        if match:
                yes_movies.append(movie)
    if yes_movies == []:
            print("No movie could be found with your selected genre")
    return yes_movies

#Sorting displayed movies by TMBD voter average... 
def get_rating(movie): 
     return movie["vote_average"]

def sort_movies(yes_movies):
    sorting = sorted(yes_movies, key = get_rating)
    return sorting

#Now displaying results
def display_movies(sort_movies):
    for movie in sort_movies: 
        print (movie["title"]),movie["vote_average"],movie(["release_date"])






