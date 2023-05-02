import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import threading
import time

previous_values = []
cred = credentials.Certificate('C:/ADAMS/AdAMS/uitesting/firebase setup testing/credentials/adams-76a2c-firebase-adminsdk-aopv9-879a7bfbe5.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://adams-76a2c-default-rtdb.firebaseio.com/'
})

ref = db.reference('key_value_pairs')

value = 'new value'
timestamp = int(time.time() * 1000)  # convert current time to milliseconds

ref.push({
    'value': [0].append('123'),
    'timestamp': timestamp
})