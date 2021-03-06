import cgi

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant

# Create session and connect to DB
engine = create_engine('sqlite:///restaurant_menu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += '<h1>Hello, World!</h1>'
                output += '''
                    <form method='POST' enctype='multipart/form-data' action='/hello'>
                        <h2>What would you like to say?</h2>
                        <input name='message' type='text'>
                        <input type='submit' value='Submit'>
                </form>
                '''
                output += '</body></html>'
                self.wfile.write(output)
                print output 
                return
            if self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += '''&#161Hola, Mundo! <a href='/hello'>Back to Hello</a>'''
                output += '''
                    <form method='POST' enctype='multipart/form-data' action='/hello'>
                        <h2>What would you like to say?</h2>
                        <input name='message' type='text'>
                        <input type='submit' value='Submit'>
                </form>
                '''
                output += '</body></html>'
                self.wfile.write(output)
                print output 
                return
            if self.path.endswith('/restaurants'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                restaurants = session.query(Restaurant).all()   

                output = ''
                output += '<html><body>'
                output += '<h1>Restaurants</h1>'
                output += '''<a href='/restaurants/new'><h2>Make a new restaurant</h2></a>'''
                for restaurant in restaurants:
                    output +=  restaurant.name
                    output += ''' <a href='/restaurants/%s/edit'>Edit</a>''' % restaurant.id
                    output += ''' <a href='/restaurants/%s/delete'>Delete</a>''' % restaurant.id
                    output += '</br>'
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ''
                output += '<html><body>'
                output += '<h1>Make a new Restaurant</h1>'
                output += '''
                    <form method='POST' enctype='multipart/form-data' action='/restaurants/new'>
                        <input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>
                        <input type='submit' value='Create'>
                    </form>
                '''
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/edit'):
                restaurantIdPath = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIdPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                output = ''
                output += '<html><body>'
                output += '<h3> %s </h3>' % myRestaurantQuery.name
                output += '''
                    <form method='POST' enctype='multipart/form-data' action='/restaurants/{}/edit'>
                        <input name='newRestaurantName' type='text' placeholder='{}'>
                        <input type='submit' value='Update'>
                    </form>
                '''.format(myRestaurantQuery.id, myRestaurantQuery.name)
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/delete'):
                restaurantIdPath = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIdPath).one()
                if myRestaurantQuery != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')           
                    self.end_headers()     

                output = ''
                output += '<html><body>'
                output += '<h1>Are you sure you want to delete %s </h1>' % myRestaurantQuery.name
                output += '''
                    <form method='POST' enctype='multipart/form-data' action='/restaurants/{}/delete'>
                        <input type='submit' value='Delete'>
                    </form>
                '''.format(myRestaurantQuery.id)
                output += '</body></html>'  
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, 'File Not Found %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/hello') or self.path.endswith('/hola'):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('message')
                output = ''
                output += '<html><body>'
                output += '<h2>Okay, how about this: </h2>'
                output += '<h1> %s </h1>' % messageContent[0]
                output += '''
                <form method='POST' enctype='multipart/form-data' action='/hello'>
                    <h2>What would you like to say?</h2>
                    <input name='message' type='text'>
                    <input type='submit' value='Submit'>
                </form> 
                '''
                self.wfile.write(output)
                print output
                return
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('newRestaurantName')

                    newRestaurant = Restaurant(name = messageContent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return
            if self.path.endswith('/edit'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if(ctype == 'multipart/form-data'):
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messageContent = fields.get('newRestaurantName')
                    
                    restaurantIdPath = self.path.split('/')[2]
                    
                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIdPath).one()
                    if myRestaurantQuery != []:
                        myRestaurantQuery.name = messageContent[0]
                        session.add(myRestaurantQuery)
                        session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return
            if self.path.endswith('/delete'):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if(ctype == 'multipart/form-data'):
                    restaurantIdPath = self.path.split('/')[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIdPath).one()
                    if myRestaurantQuery != []:
                        session.delete(myRestaurantQuery)
                        session.commit
                    
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                return
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print 'Web server running on port %s' % port
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C entered, stoping web server...' 
        server.socket.close()

if __name__ == '__main__':
    main()