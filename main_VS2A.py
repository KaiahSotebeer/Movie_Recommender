#working on streamlit interface 
import streamlit as st
#importing the movie recommender code I wrote for Vs 1 B - just so I don't make easy mistakes in re-coding.
import main_VS1B as mr

#streamlit app
st.title("Welcome to Movie Recommender")
st.set_page_config(layout = "wide")
st.write("Finally know what to watch!")

#user selects genre
genre = st.selectbox(
    "Please select your genres of interest",
    ("Action", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Science Fiction", "Thriller")
)
#user select rating on a slider
rating = st.slider(
    "Rating from 1-10",
    min_value=1,
    max_value=10,
)
#user selects choice start year
year_choice_start = st.number_input(
    "Start year",
    min_value=1900,
    max_value=2026,
    value=2000
)
#user selects choice end year
year_choice_end = st.number_input(
    "End year",
    min_value=1900,
    max_value=2026,
    value=2026
)
#making the search button
if st.button("Find Movies"):
    #pulling preference dict from main_VS1B.py
    preferences = {
        "genre_choice": genre,
        "year_choice_start": int(year_choice_start),
        "year_choice_end": int(year_choice_end),
        "rating_choice": float(rating),
    }
    #searching TMDB for preferences
    data = mr.search_tmdb(preferences)
    movies = data["results"]
    poster_path = movies[0]["poster_path"]
    poster_url = "https://image.tmdb.org/t/p/"
    filtered = mr.filter_movies(movies, preferences)

    if filtered:
        #I decided to only show the top 5 choices? Otherwise with all the images the output gets very long... 
        recs = mr.sort_movies(filtered)
        top_five = recs[:5]

        for movie in top_five:
            st.write(movie["title"], movie["vote_average"])
            #getting the TMDB posters. I used this website to help format https://developer.themoviedb.org/docs/image-basics)
            if poster_path:
                poster_url = "https://image.tmdb.org/t/p/w500/" + movie["poster_path"]
                print(f"Standard Poster (w500): {poster_url}")
                st.image(poster_url)
        else:
            print("No poster available")
    else:
        st.warning("No movies found. Try changing your preferences.")



    
