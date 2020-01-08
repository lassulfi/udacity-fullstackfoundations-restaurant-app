from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurant_menu.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()

myFirstRestaurant = Restaurant(name = 'Pizza Palace')

session.add(myFirstRestaurant)
session.commit()

#Check if the data was stored
print(session.query(Restaurant).all())

cheesePizza = MenuItem(name = 'Cheese Pizza', 
    description = 'Made with all natural ingredients and fresh mozzarella', 
    course = 'Entree', 
    price = '$8.99',
    restaurant = myFirstRestaurant)

session.add(cheesePizza)
session.commit()

print(session.query(MenuItem).all())