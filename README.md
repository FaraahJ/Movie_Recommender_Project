 # PROJECT 2: Movie Recommender Project

This repository aims to explain the process of building a movie recommender to suggest similar movie titles to users based off of:
- Content
- Ratings

🎥 The main directory contains files for the content based system. In this you will find:

1. [Analysis of the dataset](https://github.com/FaraahJ/Movie_Recommender_Project/blob/main/MovieAnalysis.ipynb) - Natural Language Processing, vectorisation, cosine similarity and stemming were used to 
   compute similar movies based on their overview description, genre, cast and crew. 
2. Two models that were saved using pickle
3. The [framework](https://github.com/FaraahJ/Movie_Recommender_Project/blob/main/movieapp.py) used to load models and build functions for the final application in VSCode

 📈 The [User Based recommender]() directory contains files for the rating based system. In here you will find:

1. The new dataset used for the system, that can be found [here](https://www.kaggle.com/datasets/debanganghosh/imdb-dataset?resource=download) 
2. [Data visualisation](https://github.com/FaraahJ/Movie_Recommender_Project/blob/main/User%20Based%20Recommender/CF_Analysis.ipynb) and [model building](https://github.com/FaraahJ/Movie_Recommender_Project/blob/main/User%20Based%20Recommender/CollaborativeFiltering.ipynb) - (❗Due to circular import errors, the visualisation and modelling were 
   performed separately across Jupyter Notebook and Google Colab). The data was analysed based on the number of counts per 
   IMDB rating, and the number of IMDB ratings per movie title. Surprise library packages were used to create predictions 
   using a range of different algorithms and were evaluated using RMSE metrics. 
3. The KNNWithMeans algorithm showed the best RMSE score, therefore it was the chosen saved model.
4. The [app](https://github.com/FaraahJ/Movie_Recommender_Project/blob/main/User%20Based%20Recommender/UserBasedapp.py) file displays the model loading and final app function creation in VSCode.

