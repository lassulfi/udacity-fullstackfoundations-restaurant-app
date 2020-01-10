from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# Mock data
#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        restaurantName = request.form['name']
        restaurantId = len(restaurants) + 1
        restaurant = {'name': restaurantName, 'id': restaurantId}
        restaurants.append(restaurant)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = restaurants[restaurant_id - 1]
    if request.method == 'POST':
        editedRestaurant['name'] =  request.form['name']
        restaurants.insert(editedRestaurant.id - 1, editedRestaurant)
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant=editedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = restaurants[restaurant_id - 1]
    if request.method == 'POST':
        restaurants.remove(deletedRestaurant)
        return redirect(url('showRestaurants'))
    else: 
        return render_template('deleterestaurant.html', restaurant=deletedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = restaurants[restaurant_id - 1]
    return render_template('menu.html', restaurant=restaurant, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = restaurants[restaurant_id - 1]
    if request.method == 'POST':
        item = {}
        item['id'] = len(items)
        if request.form['name']:
            item['name'] = request.form['name']
        else:
            item['name'] = ''
        if request.form['description']:
            item['description'] = request.form['description']
        else:
            item['descritpion'] = ''
        if request.form['price']:
            item['price'] = request.form['price']
        else:
            item['price'] = ''
        item['course'] = request.form['course']
        items.append(item)
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    restaurant = restaurants[restaurant_id - 1]
    item = items[menu_id - 1]
    if item != []:
        if request.method =='POST':
            if request.form['name']:
                item['name'] = request.form['name']
            else:
                item['name'] = ''
            if request.form['description']:
                item['description'] = request.form['description']
            else:
                item['descritpion'] = ''
            if request.form['price']:
                item['price'] = request.form['price']
            else:
                item['price'] = ''
            item['course'] = request.form['course']
            items.index(item.id - 1, item)
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        else:
            return render_template('editmenuitem.html', restaurant_id=restaurant_id, item=item)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    restaurant = restaurants[restaurant_id - 1]
    try:
        deletedItem = items[menu_id - 1]
        if deletedItem != []:
            if request.method == 'POST':
                restaurants.remove(deletedItem)
                return redirect(url_for('showMenu', restaurant_id=restaurant_id))
            else:
                return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item=deletedItem)
    except:
        return render_template('menunotfound.html', restaurant_id=restaurant_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)