from website import create_app, db
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def main():
    PORT = os.environ.get("PORT")
    DEBUG = os.environ.get("FLASK_DEBUG")
    HOST = os.environ.get("HOST")
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(host=HOST, port=PORT, debug=DEBUG)

if __name__ == "__main__":
    main()