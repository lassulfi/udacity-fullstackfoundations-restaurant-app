from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurant_menu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# Mock data
# #Fake Restaurants
# restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

# restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
# items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
# item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant=editedRestaurant)
    

@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        return redirect(url('showRestaurants'))
    else: 
        return render_template('deleterestaurant.html', restaurant=deletedRestaurant)

@app.route('/restaurant/<int:restaurant_id>/')
@app.route('/restaurant/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    showMenuRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    showMenuItems = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', restaurant=showMenuRestaurant, items=showMenuItems)

@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    newMenuItemRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if newMenuItemRestaurant != []:
        if request.method == 'POST':
            addedItem = MenuItem(name=request.form['name'], 
                description=request.form['description'],
                price=request.form['price'],
                course=request.form['course'],
                restaurant_id=newMenuItemRestaurant.id)
            session.add(addedItem)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id=newMenuItemRestaurant.id))
        else:
            return render_template('newmenuitem.html', restaurant_id=restaurant_id)
    else:
        return render_template('restaurantnotfound.html')

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedMenuItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if editedMenuItem != []:
        if request.method =='POST':
            if request.form['name']:
                editedMenuItem['name'] = request.form['name']
            else:
                editedMenuItem['name'] = ''
            if request.form['description']:
                editedMenuItem['description'] = request.form['description']
            else:
                editedMenuItem['descritpion'] = ''
            if request.form['price']:
                editedMenuItem['price'] = request.form['price']
            else:
                editedMenuItem['price'] = ''
            editedMenuItem['course'] = request.form['course']
            session.add(editedMenuItem)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        else:
            return render_template('editmenuitem.html', restaurant_id=restaurant_id, item=editedMenuItem)
    else:
        return render_template('menunotfound.html')

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if deletedItem != []:
        if request.method == 'POST':
            session.delete(deletedItem)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
        else:
            return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item=deletedItem)
    else:
        return render_template('menunotfound.html', restaurant_id=restaurant_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)