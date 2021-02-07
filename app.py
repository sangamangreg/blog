from app import app


@app.route( '/', methods=["GET"] )
def home():
    return "<h1>Welcome to new blog site. This page will move to blog listing page later</h1>"


if __name__ == '__main__':
    app.run( debug=True )  # on production remove debug. take this parameter from env