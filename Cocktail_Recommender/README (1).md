# Cocktail Recommender

**AI in Computing and Robotics Research — Project 1**

A Python-based cocktail recommendation tool that suggests five cocktails based on ingredients a user has at home. Users can select a recommendation to view its category, glass type, ingredient measurements, and preparation instructions.

The project explores **unsupervised machine learning and text-based similarity** using TF-IDF vectorization, cosine similarity, K-Means clustering, and Principal Component Analysis (PCA).

## Features

- **Ingredient-based recommendations:** Enter a comma-separated list of ingredients to find cocktails with similar ingredient descriptions.
- **Top-five results:** Ranks cocktails by cosine similarity to the entered ingredients.
- **Cocktail details:** View a selected drink's category, glass type, ingredient quantities, and instructions.
- **Ingredient clustering:** Groups cocktails into five clusters using K-Means.
- **2D visualization:** Uses PCA to project ingredient vectors into two dimensions for a scatter plot of the clusters.
- **Interactive terminal workflow:** Request new recommendations, select a drink, or exit the program.

## How It Works

The recommendation pipeline has four main stages:

1. **Data preprocessing**
   - Loads `final_cocktails.csv` with pandas.
   - Removes the `drinkThumbnail`, `text`, and columns containing `Unnamed`.
   - Saves the cleaned table as `cleaned_dataset.csv`.
   - Converts the `alcoholic` field to a binary value: alcoholic and optional-alcohol drinks become `1`, while non-alcoholic drinks become `0`.

2. **TF-IDF vectorization**
   - `TfidfVectorizer` converts each cocktail's `ingredients` text into a numerical vector.
   - The same fitted vectorizer transforms the user's ingredient list into a vector in the same feature space.

3. **Similarity ranking and clustering**
   - **Cosine similarity** compares the user's ingredient vector with each cocktail's ingredient vector.
   - The five cocktails with the highest similarity scores are displayed.
   - **K-Means** groups the cocktail vectors into five clusters. The program also predicts a cluster for the user's ingredient vector and displays that cluster number alongside each recommendation.

4. **PCA visualization**
   - Principal Component Analysis reduces the ingredient vectors to two dimensions.
   - A scatter plot colors the cocktails by their K-Means cluster, providing a visual overview of the grouping.

### Important interpretation notes

- This is a content-based recommender: it compares ingredient text, not user ratings, popularity, or personal preferences.
- The displayed similarity percentage is the cosine similarity score multiplied by 100. It is **not** a probability that the user will like the cocktail.
- In the current implementation, clustering is used for analysis and visualization, and the predicted cluster is printed with the recommendations. The top-five ranking itself is calculated across the full dataset rather than being restricted to that cluster.
- TF-IDF uses the ingredient text as provided. Differences in spelling, ingredient naming, or formatting can affect matches.

## Technologies

- **Python**
- **pandas** — loading, cleaning, and handling the cocktail dataset
- **NumPy** — numerical operations
- **scikit-learn**
  - `TfidfVectorizer` — text-to-feature conversion
  - `cosine_similarity` — ingredient similarity scoring
  - `KMeans` — unsupervised clustering
  - `PCA` — dimensionality reduction for visualization
- **Matplotlib** — plotting the clusters
- **Seaborn** — imported in the script, though not directly used in the shown code
- **scikit-image** — imported in the script, though not directly used in the shown code

## Dataset

The project uses the **Cocktails** dataset from Kaggle:

[View and download the dataset on Kaggle](https://www.kaggle.com/datasets/aadyasingh55/cocktails)

The script expects a file named `final_cocktails.csv` in the working directory. The data should include the columns referenced by the program, including `name`, `ingredients`, `ingredientMeasures`, `alcoholic`, `category`, `glassType`, and `instructions`.

## Setup and Usage

### 1. Clone or download the project

Place the Python script and `final_cocktails.csv` in the same directory.

### 2. Install dependencies

Make sure Python 3 is installed, then run:

```bash
python -m pip install pandas numpy matplotlib seaborn scikit-image scikit-learn
```

### 3. Run the program

Save the script as, for example, `cocktail_recommender.py`, then run:

```bash
python cocktail_recommender.py
```

The script will preprocess the dataset, generate the cluster visualization, and prompt you to enter ingredients.

### 4. Enter ingredients

At the prompt, enter ingredients separated by commas. For example:

```text
rum, lime juice, sugar
```

The program prints five recommendations with similarity scores. Enter a number from `1` to `5` to view a cocktail's details.

At the selection prompt:

- Enter `1`–`5` to view the corresponding recipe.
- Enter `new` to provide another ingredient list.
- Enter `done` to exit.

You can also enter `done` at the initial prompt to quit.

## Output

The program produces:

- `cleaned_dataset.csv` — the dataset after the script's column cleanup.
- A PCA scatter plot titled **“cocktail clusters (ingredients)”**.
- Five ranked cocktail recommendations for each ingredient list.
- Recipe details for a selected cocktail, including measurements and instructions.

## Model Configuration

| Setting | Current value | Purpose |
|---|---:|---|
| Number of clusters | 5 | Sets the number of K-Means groups |
| K-Means `random_state` | 44 | Makes clustering reproducible for the same data and environment |
| K-Means `n_init` | 10 | Runs multiple initializations and keeps the best solution |
| PCA components | 2 | Projects ingredient vectors into two dimensions |
| Recommendations | 5 | Number of highest-similarity cocktails returned |

The number of clusters is configurable. The code comments suggest evaluating alternative values with an elbow-method analysis; the current script uses five clusters.

## Current Limitations

- **Ingredient matching is text-based.** The system does not automatically recognize synonyms or equivalent ingredients (for example, different names for the same ingredient).
- **No quantity-aware matching.** The recommendation score does not account for ingredient measurements or whether the user has enough of each ingredient.
- **No preference learning.** The system does not learn from ratings, past selections, or feedback.
- **Cluster count is fixed.** The current implementation uses five clusters rather than selecting the number through a model-selection procedure.
- **PCA is for visualization.** The plotted two-dimensional coordinates are a simplified projection and do not capture every detail of the original ingredient vectors.

## Future Improvements

- Normalize ingredient names and handle synonyms.
- Filter recommendations by alcoholic or non-alcoholic preference.
- Distinguish ingredients the user has from ingredients they would need to purchase.
- Evaluate different cluster counts with an elbow plot and/or silhouette score.
- Add a graphical or web-based interface.
- Add tests for empty input, missing dataset values, and recipe formatting.

## Project Context

This project was developed for **AI in Computing and Robotics Research** to explore how machine-learning methods can be applied to a practical recommendation task. It combines text feature extraction, similarity-based ranking, unsupervised clustering, and dimensionality reduction in an interactive Python application.
