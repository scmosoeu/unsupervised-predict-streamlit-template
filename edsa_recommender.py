"""

    Streamlit webserver-based Recommender Engine.

    Author: Explore Data Science Academy.

    Note:
    ---------------------------------------------------------------------
    Please follow the instructions provided within the README.md file
    located within the root of this repository for guidance on how to use
    this script correctly.

    NB: !! Do not remove/modify the code delimited by dashes !!

    This application is intended to be partly marked in an automated manner.
    Altering delimited code may result in a mark of 0.
    ---------------------------------------------------------------------

    Description: This file is used to launch a minimal streamlit web
	application. You are expected to extend certain aspects of this script
    and its dependencies as part of your predict project.

	For further help with the Streamlit framework, see:

	https://docs.streamlit.io/en/latest/

"""
# Streamlit dependencies
import streamlit as st

# Data handling dependencies
import pandas as pd
import numpy as np

# Custom Libraries
from utils.data_loader import load_movie_titles
from recommenders.collaborative_based import collab_model
from recommenders.content_based import content_model

# Added Custom Libraries
from added_functions.webscrapper import poster, overview
from added_functions.ratings_plots import counting_plot, distribution_plot
from added_functions.year_plots import release_year
from added_functions.runtime import movie_duration
from added_functions.director_plots import director_movies_ratings
import added_markdown.text as txt

# Data Loading
title_list = load_movie_titles('resources/data/movies.csv')

# Custom Data loading
ratings = pd.read_csv('resources/data/ratings.csv')
movies = pd.read_csv('resources/data/movies.csv')
links = pd.read_csv('../data/links.csv', nrows=10)
metadata = pd.read_csv('../data/imdb_data.csv')

# App declaration
def main():

    # DO NOT REMOVE the 'Recommender System' option below, however,
    # you are welcome to add more options to enrich your app.
    page_options = ["Recommender System","Solution Overview", "EDA", "Movie App"]

    # -------------------------------------------------------------------
    # ----------- !! THIS CODE MUST NOT BE ALTERED !! -------------------
    # -------------------------------------------------------------------
    page_selection = st.sidebar.selectbox("Choose Option", page_options)
    if page_selection == "Recommender System":
        # Header contents
        st.write('# Movie Recommender Engine')
        st.write('### EXPLORE Data Science Academy Unsupervised Predict')
        st.image('resources/imgs/Image_header.png',use_column_width=True)
        # Recommender System algorithm selection
        sys = st.radio("Select an algorithm",
                       ('Content Based Filtering',
                        'Collaborative Based Filtering'))

        # User-based preferences
        st.write('### Enter Your Three Favorite Movies')
        movie_1 = st.selectbox('Fisrt Option',title_list[14930:15200])
        movie_2 = st.selectbox('Second Option',title_list[25055:25255])
        movie_3 = st.selectbox('Third Option',title_list[21100:21200])
        fav_movies = [movie_1,movie_2,movie_3]

        # Perform top-10 movie recommendation generation
        if sys == 'Content Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = content_model(movie_list=fav_movies,
                                                            top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


        if sys == 'Collaborative Based Filtering':
            if st.button("Recommend"):
                try:
                    with st.spinner('Crunching the numbers...'):
                        top_recommendations = collab_model(movie_list=fav_movies,
                                                           top_n=10)
                    st.title("We think you'll like:")
                    for i,j in enumerate(top_recommendations):
                        st.subheader(str(i+1)+'. '+j)
                except:
                    st.error("Oops! Looks like this algorithm does't work.\
                              We'll need to fix it!")


    # -------------------------------------------------------------------

    # ------------- SAFE FOR ALTERING/EXTENSION -------------------
    if page_selection == "Solution Overview":
        st.title("Solution Overview")
        st.info("Description of our winning approach")
        st.write(txt.introduction_overview)
        
        st.image('resources/imgs/download.png', caption='Recommenders', use_column_width=True)

        st.write("We considered both the content-based and collaborative filter approaches")
        st.write(txt.systems)
        st.image('resources/imgs/CF_vs_CBF.png')

        st.write(txt.Collaborative)
        
        st.image('resources/imgs/Fig1_HTML.png')

     

    # You may want to add more sections here for aspects such as an EDcompanies A,
    # or to provide your business pitch.

    # Data manipulation
    df = pd.merge(links, movies, on='movieId')
    metadata.dropna(subset=['runtime'])
    casting_database = pd.merge(metadata, movies, on='movieId')
    ## converting the column to numeric
    metadata['runtime'] = pd.to_numeric(metadata['runtime'])

    ## Runtime slider inputs
    min_runtime = int(metadata['runtime'].min())
    max_runtime = int(metadata['runtime'].max())

    if page_selection == "EDA":
        st.title("Exploratory Data Analysis")

        st.write(txt.introduction)
        show_ratings = st.checkbox("Movie ratings")

        if show_ratings:
            ratings_count = counting_plot(ratings, 'rating')

            st.plotly_chart(ratings_count)
            st.write(txt.ratings_countplot_markdown)

            ratings_distribution = distribution_plot(ratings, 'movieId', 'rating')

            st.plotly_chart(ratings_distribution)
            st.write(txt.avg_ratings_markdown)

        show_yearly = st.checkbox("Yearly releases")

        if show_yearly:
            yearly_counter = release_year(movies)

            st.plotly_chart(yearly_counter)

        length_of_movie = st.checkbox("Movie runtime")
        
        if length_of_movie:

            duration = st.slider(
                label='Max duration of movie runtime',
                min_value=min_runtime,
                max_value=max_runtime,
                value=200,
                step=10
            )

            runtime = movie_duration(metadata, duration)

            st.plotly_chart(runtime)

        directors = st.checkbox("Information about directors")

        if directors:
            movie_directors = director_movies_ratings(metadata, ratings)
            st.plotly_chart(movie_directors)


    if page_selection == "Movie App":        
        st.title('The Movies App')

        option = st.sidebar.selectbox(
            label='Movie',
            options=df['title'],
            index=0
        )

        # Get the movie poster and genre
        movie_id = df[df['title'] == option]['imdbId'].iloc[0]
        genres = df[df['title'] == option]['genres'].iloc[0]
        
        # Casting and Director
        director = casting_database[casting_database['title'] == option]['director'].iloc[0]
        casts = casting_database[casting_database['title'] == option]['title_cast'].iloc[0]

        
        img = poster(movie_id)
        st.sidebar.image(img)

        # Plot summary of the movie
        st.subheader("Summary")
        plot_summary = overview(movie_id)
        st.write(plot_summary)
        
        st.subheader("Genre")
        if '|' in genres:
            genre = genres.replace('|', ', ')
            st.write(genre)
        else:
            st.write(genres)  

        st.subheader("Director")
        st.write(director)

        st.subheader("Cast")

        # Check if there is casting members
        if '|' in casts:
            for cast in casts.split('|'):
                st.write(cast)
        else:
            st.write(casts)        

if __name__ == '__main__':
    main()
