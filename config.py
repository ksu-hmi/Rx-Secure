from os import environ, path
from dotenv import load_dotenv
import uuid  # Use this instead of requests

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask configuration from .env file"""

    try:
        FLASK_APP = environ.get('FLASK_APP')
        FLASK_ENV = environ.get('FLASK_ENV')    
    except:
        pass

    # Generate a UUID locally instead of calling external service
    SECRET_KEY = str(uuid.uuid4())

    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = True

    