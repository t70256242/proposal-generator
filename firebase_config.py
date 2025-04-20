import pyrebase
import os
from dotenv import load_dotenv

load_dotenv()

firebaseConfig = {
    "apiKey": os.getenv("API_KEY"),
    "authDomain": os.getenv("AUTH_DOMAIN"),
    "databaseURL": os.getenv("database_url"),
    "projectId": os.getenv("project_id"),
    "storageBucket": os.getenv("storage_bucket"),
    "messagingSenderId": os.getenv("messaging_sender_id"),
    "appId": os.getenv("app_id"),
    "measurementId": os.getenv("MEASUREMENT_ID")
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


