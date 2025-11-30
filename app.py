from flask import Flask, render_template, request, redirect, session, url_for
import requests

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

API_KEY = "a0549a0e70454ffbabd835484df10254"

# In-memory mock databases
users = {}       # {username: password}
favorites = {}   # {username: [recipe_ids]}

@app.route('/', methods=['GET', 'POST'])
def index():
    recipes = []
    if request.method == 'POST':
        ingredients = request.form.get('ingredients')
        if ingredients:
            url = 'https://api.spoonacular.com/recipes/findByIngredients'
            params = {
                'ingredients': ingredients,
                'number': 8,
                'apiKey': API_KEY
            }

            response = requests.get(url, params=params)
            print("Fetching recipes for:", ingredients)
            print("Status Code:", response.status_code)

            if response.status_code == 200:
                recipes_data = response.json()
                print("Recipes found:", len(recipes_data))

                for recipe in recipes_data:
                    details_url = f'https://api.spoonacular.com/recipes/{recipe["id"]}/information'
                    info = requests.get(details_url, params={'apiKey': API_KEY})

                    if info.status_code == 200:
                        recipe_info = info.json()
                        recipes.append({
                            'id': recipe_info['id'],
                            'title': recipe_info['title'],
                            'image': recipe_info['image'],
                            'ingredients': [i['original'] for i in recipe_info.get('extendedIngredients', [])],
                            'instructions': recipe_info.get('instructions', 'No instructions provided.')
                        })
                    else:
                        print(f"Error fetching details for ID {recipe['id']}: {info.status_code}")
            else:
                print("API error:", response.status_code, response.text)
        else:
            print("No ingredients entered.")

    return render_template('index.html', recipes=recipes, user=session.get('user'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if users.get(user) == pwd:
            session['user'] = user
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Invalid credentials")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user in users:
            return render_template('register.html', error="Username already exists")
        users[user] = pwd
        favorites[user] = []
        session['user'] = user
        return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/favorite/<int:recipe_id>')
def favorite(recipe_id):
    user = session.get('user')
    if user:
        if recipe_id not in favorites[user]:
            favorites[user].append(recipe_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True ) 