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
                    output += ''' <a href='#'>Edit</a>'''
                    output += ''' <a href='#'>Delete</a>'''
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