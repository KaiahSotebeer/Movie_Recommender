#working on streamlit interface 
import streamlit as st
#importing the movie recommender code I wrote for Vs 1 B - just so I don't make easy mistakes in re-coding.
import main as mr

#streamlit app
#adding "now showing" image
st.image(
    "images/now_showing_2.jpg",
    width=600)

st.title("Welcome to Movie Recommender")
st.set_page_config(layout = "wide", page_icon= "🎬")
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
        count = 0
        cols = st.columns(5)

        for movie in recs:
            #getting the TMDB posters. I used this website to help format https://developer.themoviedb.org/docs/image-basics)
            if movie.get("vote_count", 0) <= 50:
                    continue
            if count == 5:
                break

            with cols[count]:
                st.write(movie["title"], movie["vote_average"])
                st.write(f"⭐ {movie['vote_average']}/10")
                poster_path = movie.get("poster_path")

                if poster_path:
                    poster_url = "https://image.tmdb.org/t/p/w154" + movie["poster_path"]
                    print(f"Thumbsize Poster (w154): {poster_url}\nRatings: {movie.get('vote_count', 0):,}")
                    st.image(poster_url)
                    st.caption(f"Number of Ratings: {movie.get('vote_count', 0):,}")
                else:
                    st.write("No poster available")

                movie_id = movie["id"]
                details = mr.get_movie_details(movie_id)
                st.write("Title:", details["title"])
                st.write("Release date:", details["release_date"])
                st.write("Description:", details["overview"])
                st.write("How long is the movie?:", details["runtime"], "minutes")
                
            count += 1

        if count == 0:
            st.warning("No movies found with minimum of 50 ratings")
    else:
        st.warning("No movies found. Try changing your preferences.")



    
