from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from flask import Flask, render_template
from flask_cors import CORS, cross_origin
import sqlite3
import time
import requests
import uuid
import os
import shutil

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


conn = sqlite3.connect('reels.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS reels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            price VARCHAR,
            img_url VARCHAR,
            product_link VARCHAR
            )''')

def download_image(url, directory, filename):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the request was not successful
        
        # Create the full path by joining the directory and filename
        full_path = os.path.join(directory, filename)
        
        with open(full_path, 'wb') as f:
            f.write(response.content)
        
        print(f"Image downloaded as '{full_path}'")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image: {e}")





@app.route('/', methods=["GET"])
@cross_origin()              
def base_page():
    conn = sqlite3.connect('reels.db')
    c = conn.cursor()
    c.execute('SELECT * FROM reels')
    all_products = c.fetchall()
    conn.commit()
    conn.close()
    print(len(all_products))

    return render_template('index.html', all = all_products) 




@app.route('/buy/<product_id>', methods=['GET'])
def asdf(product_id):
    conn = sqlite3.connect('reels.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM reels WHERE id = {product_id}')
    print(product_id)
    product = c.fetchall()
    print(product)
    conn.commit()
    conn.close()
    return render_template("buy.html", product = product[0])
"""
index : value       bn
0:id
1:name
2:price
3:img url
4:link  
"""



app.run()
conn.commit()
conn.close()