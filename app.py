import pickle
import streamlit as st
import requests
import os 

from dotenv import load_dotenv

load_dotenv()  
API_KEY = os.getenv("TMDB_API_KEY")


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url)
    data = data.json()
    
    # ✅ Check if the API response contains 'poster_path'
    if "poster_path" in data and data["poster_path"]:
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    
    # ✅ If poster is missing, return a placeholder image
    return "https://upload.wikimedia.org/wikipedia/commons/1/14/Movie_clapper_board.jpg"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:16]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

# Add custom CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css") 


st.header('Movie Recommender System')
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    st.subheader('Recommended Movies for: {}'.format(selected_movie))
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    # Now, when you display the movies:
    for i in range(5):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text(recommended_movie_names[i*3+0])
            st.image(recommended_movie_posters[i*3+0])
        with col2:
            st.text(recommended_movie_names[i*3+1])
            st.image(recommended_movie_posters[i*3+1])

        with col3:
            st.text(recommended_movie_names[i*3+2])
            st.image(recommended_movie_posters[i*3+2])
      
    