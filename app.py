from website import create_app
from dotenv import load_dotenv
import os

load_dotenv(override=True)

def main():
    PORT = os.environ.get("PORT")
    DEBUG = os.environ.get("FLASK_DEBUG")
    HOST = os.environ.get("HOST")
    app = create_app()
    app.run(host=HOST, port=PORT, debug=DEBUG)

if __name__ == "__main__":
    main()