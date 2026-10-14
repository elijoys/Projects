import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import skimage.io
import sklearn
import sklearn.datasets

# import vectorizer, cosine similarity, kmeans, and PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# preprocessing data
df = pd.read_csv("final_cocktails.csv")
df = df.drop(columns=["drinkThumbnail","text"])
df = df.drop(columns=[col for col in df.columns if "Unnamed" in col])
df.to_csv("cleaned_dataset.csv",index = False)

df["alcoholic"] = df["alcoholic"].map({
    "Alcoholic": 1,
    "Optional alcohol": 1,
    "Non alcoholic": 0
})

print(df.head(5))


# store dataset as "cocktails"
cocktails = df

# vectorizer
vectorizer = TfidfVectorizer()

# convert the ingredients column into TF-IDF vectors (text -> numerical data basically)
ingredient_vectors = vectorizer.fit_transform(cocktails["ingredients"])

# clustering: apply kmeans, cluster cocktails basefd on ingredients
num_clusters = 5

kmeans = KMeans(n_clusters = num_clusters, random_state = 44, n_init = 10)
cocktails['cluster'] = kmeans.fit_predict(ingredient_vectors)
#^ num_clusters: tested values -> can use elbow method to figure out best value
#^ random_state guarantees same results, n_init set to 10 to fix an error 

# principal component analysis (PCA) -> simplify data, take out most important features
# helps when visualizing
pca = PCA(n_components = 2) # set to 2 for 2D
pca_components = pca.fit_transform(ingredient_vectors.toarray())

print("pca shape: ", pca_components.shape)
print(cocktails[['name','cluster']].head())

# plot clusters
plt.figure(figsize=(10,6)) # google said this was a common size
plt.scatter(pca_components[:, 0], pca_components[:,1], c = cocktails['cluster'], cmap = 'viridis')
plt.title("cocktail clusters (ingredients)")
plt.xlabel("pca 1")
plt.ylabel("pca 2")
plt.show()


# function to find top 5 similar cocktails
def recommend_cocktails(user_input):
    
    # user list of ingredients ->  string
    user_input_str = ", ".join(user_input)  # ["rum", "lime juice", "sugar"] -> "rum, lime juice, sugar"
    
    # user input -> TF-IDF vector
    user_vector = vectorizer.transform([user_input_str])  
    
    # cosine similarity between the user's input and each cocktail's ingredients 
    similarities = cosine_similarity(user_vector, ingredient_vectors).flatten()
    
    # get the indices of the top 5 most similar cocktails
    top_5 = similarities.argsort()[-5:][::-1]  # select the top 5 cocktails by highest similarity first
    
    # predict user's cluster based on their inputted ingredients
    cluster_prediction = kmeans.predict(user_vector)[0] 
    cluster_cocktails = cocktails[cocktails['cluster'] == cluster_prediction]
    
    # print the top 5 recommended cocktails and their similarity scores
    print("\nYour top 5 cocktail recommendations:")
    for i,idx in enumerate(top_5):
        print(f"\t{i+1}. {cocktails.iloc[idx]['name']} - Similarity: {similarities[idx]*100:.2f}% (Cluster #{cluster_prediction})") 
    return top_5


while True:
    user_input = input("Enter a list of ingredients, separated by commas and a space. For example: rum, lime juice, sugar. Or, type 'done' to exit: ")
    
    if user_input == 'done':
            print("Enjoy the cocktail!")
            break
            
    if not user_input:
        print("You must type at least one ingredient.")
        continue
            
    user_input_list = [item.strip() for item in user_input.split(',') if item.strip()]
    
    if not user_input_list:
        print("I dont have those ingredients in my dataset, sorry!")
        continue
    
    top_5_recommended = recommend_cocktails(user_input_list)

    while True:
        choice = input("\nIf you like a recommendation, type and enter its corresponding number (1-5). 'new' to enter a new list.\n Your choice: ").strip().lower()
        print("\n************************************************************")
        
        if choice == 'done':
            print("Enjoy the cocktail!")
            exit()
        
        if choice == 'new':
            break
        
        if choice.isdigit():
            choice_int = int(choice)
            if choice_int > 5 or choice_int < 1:
                print("ERROR! Decision is out of range, must be a value between 1 and 5 - re-enter a number, or enter 'new' to enter new ingredients/n")
            else :
                index = top_5_recommended[choice_int - 1] 
                drink = df.iloc[index]
                print("\n************************************************************")
                print(f"\nDrink: {drink['name']}")
                print("\n************************************************************")
                print(f"\nCategory: {drink['category']}")
                print("\n************************************************************")
                print(f"\nGlass Type: {drink['glassType']}")
                print("\n************************************************************")
                
                print(f"\nIngredients: ")
                ingredient_list = drink['ingredients'].strip("[]").replace("'", "").split(', ')
                measurement_list = drink['ingredientMeasures'].strip("[]").replace("'", "").split(', ')
                
                for measure, ingredient in zip(measurement_list, ingredient_list):
                    new_measure = measure.strip()
                    new_ingredient = ingredient.strip()
                    print(f"{new_measure} of {new_ingredient}")
                
                print("\n************************************************************")
                print(f"\nInstructions: {drink['instructions']}")
                print("\n************************************************************")
                print("\nIf finished, type 'done'")
        else :
            print("Please enter a number between 1 and 5, or 'new', or 'done'")
