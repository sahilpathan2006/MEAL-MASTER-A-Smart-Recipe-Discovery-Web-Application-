import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)


API_KEY = os.getenv("SPOONACULAR_KEY")

@app.route('/', methods=['GET', 'POST'])
def home():
    recipes = []
    user_query = ""
    
    if request.method == 'POST':
        user_query = request.form.get('ingredients')
        selected_cuisine = request.form.get('cuisine')


        url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": API_KEY,
            "query": user_query,         
            "cuisine": selected_cuisine,  
            "number": 12,                 
            "addRecipeInformation": True,
            "fillIngredients": True
        }
        
        try:
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                recipes = data.get('results', [])
            elif response.status_code == 402:
                print("Note: Daily API limit reached. Try again tomorrow!")
            else:
                print(f"Something went wrong. Error code: {response.status_code}")
                
        except Exception as e:
            print(f"Connection error: {e}")

    return render_template('index.html', recipes=recipes, query=user_query)

if __name__ == '__main__':
    app.run(debug=True)