from flask import Flask, render_template, jsonify
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import folium
import time
import threading


hostname = "1o7.h.filess.io"

database = "adams_wearforce"

port = "3307"

username = "adams_wearforce"

password = "086bb173a54213e78a9d31b06b0f32b70da0adc4"

app = Flask(__name__)
db = mysql.connector.connect(
    host=hostname,
    user=username,
    password=password,
    database=database,
    port = port
)

def query_db(query):
    cursor = db.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)
    cursor.close()
    return df

