import streamlit as st
import pickle
import pandas as pd
import requests
import gzip

# --- Custom Styling ---
st.set_page_config(page_title="Movie Recommender", layout="wide")

# Apply custom CSS
st.markdown("""
<style>
        .main {
            background-color: #f4f4f4;
        }
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        .stButton button {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
            padding: 0.6em 1em;
            border-radius: 8px;
        }
        /* Style the dropdown container */
        .stSelectbox div[data-baseweb="select"] {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 8px;
            font-size: 16px;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        }

        /* Style the dropdown label */
        .stSelectbox label {
            font-weight: bold;
            font-size: 20px;
            color: #00838f;

        }

        h1 {
            color: #ff4b4b;
        }
        .movie-title {
            font-size: 18px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# --- Functions ---
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    )
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# --- Load Data ---
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))

with gzip.open('similarity.pkl.gz', 'rb') as f:
    similarity = pickle.load(f)


# --- App UI ---
st.title('🎬 Movie Recommender System')

st.markdown("#### Select a movie you like, and get 5 similar recommendations!")
selected_movie_name = st.selectbox(
    '🎥 Choose a movie:',
    movies['title'].values
)

if st.button('📽️ Recommend'):
    names, posters = recommend(selected_movie_name)

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], use_column_width=True)
            st.markdown(f"<p class='movie-title'>{names[idx]}</p>", unsafe_allow_html=True)
