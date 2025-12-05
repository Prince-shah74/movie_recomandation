import streamlit as st
import pickle
import pandas as pd
import requests

# --------------------- Fetch Poster Function ----------------------
@st.cache_data
def fetch_poster(movie_id):
    API_KEY = "0ce9dfad240fbc37c9fdf5d57177b95f"
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"
        response = requests.get(url, timeout=10)  # 10 sec timeout
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

# --------------------- Recommend Function ----------------------
def recommend(movie):
    if movie not in movies['title'].values:
        st.error(f"Movie '{movie}' not found.")
        return [], []
        
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters

# --------------------- Load Data ----------------------
movies_dict = pickle.load(open("movie_dict.pkl", 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", 'rb'))

# --------------------- Streamlit UI ----------------------
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox("Select a movie", movies['title'].values)

if st.button("Recommend"):
    with st.spinner("Fetching recommendations... ⏳"):
        names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.markdown(f"**{names[idx]}**")
            st.image(posters[idx])
