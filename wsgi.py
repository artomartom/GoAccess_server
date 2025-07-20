from app import app

from settings import LISTEN,  DEBUG, PORT
if __name__ == '__main__':
    app.run(host=LISTEN, port=int(PORT), debug=DEBUG)