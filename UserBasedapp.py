from pathlib import Path
from flask import Flask, request, render_template
import requests
import pandas as pd
import pickle

app = Flask(__name__)
BASE_DIR = Path(__file__).resolve().parent

# Load data
movies = pd.read_csv(BASE_DIR / 'imdb_top_1000.csv')
movies.columns = [c.strip().lower().replace(' ', '_') for c in movies.columns]

if 'series_title' in movies.columns:
    movies = movies.rename(columns={'series_title': 'title'})

if 'title' not in movies.columns:
    raise ValueError('The movie dataset does not contain a title column.')

if 'id' not in movies.columns:
    movies['id'] = pd.NA

model_path = BASE_DIR / 'knn_with_means_model.pkl'
loaded_algo = None

try:
    with model_path.open('rb') as model_file:
        _, loaded_algo = pickle.load(model_file)
except Exception:
    loaded_algo = None


# function to fetch movie poster
def fetch_poster(movie_id):
    if pd.isna(movie_id):
        return "https://via.placeholder.com/500x750?text=No+Poster"

    url = "https://api.themoviedb.org/3/movie/{}?api_key=390e76286265f7638bb6b19d86474639&language=en-US".format(movie_id)
    try:
        data = requests.get(url, timeout=10).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
    except Exception:
        pass
    return "https://via.placeholder.com/500x750?text=No+Poster"


# function to get recommended movies
def get_recommendations(movie):
    if not movie:
        return [], []

    match = movies[movies['title'].str.lower() == movie.strip().lower()]
    if match.empty:
        return [], []

    idx = match.index[0]

    if loaded_algo is not None:
        try:
            sim_scores = list(enumerate(loaded_algo.similarities[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:21]
            movie_indices = [i[0] for i in sim_scores]
        except Exception:
            movie_indices = [i for i in movies.index if i != idx][:20]
    else:
        movie_indices = [i for i in movies.index if i != idx][:20]

    movie_titles = movies['title'].iloc[movie_indices].tolist()
    movie_posters = []
    for i in movie_indices:
        movie_id = movies['id'].iloc[i]
        movie_posters.append(fetch_poster(movie_id))

    return movie_titles, movie_posters


# home page
@app.route('/')
def home():
    movie_list = movies['title'].tolist()
    return render_template('index.html', movie_list=movie_list,
                           recommended_movie_titles=[],
                           recommended_movie_posters=[])


# recommendation page
@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form.get('selected_movie', '')
    recommended_movie_titles, recommended_movie_posters = get_recommendations(movie_title)
    return render_template('index.html', movie_list=movies['title'].tolist(),
                           recommended_movie_titles=recommended_movie_titles,
                           recommended_movie_posters=recommended_movie_posters)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)