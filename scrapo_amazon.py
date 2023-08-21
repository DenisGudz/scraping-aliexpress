from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import sqlite3
import time
import requests
import uuid
import os
import shutil


conn = sqlite3.connect('reels.db')
c = conn.cursor()

c.execute('drop table reels')

c.execute('''CREATE TABLE IF NOT EXISTS reels(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR,
            price VARCHAR,
            img_url VARCHAR,
            product_link VARCHAR
            )''')

d = webdriver.Firefox()
d.maximize_window()
d.get('https://www.aliexpress.com')

# d.switch_to.window(driver.window_handles[1])

search_bar = d.find_element(By.XPATH, '//*[@id="search-key"]')
search_bar.send_keys('fishing reel')
search_bar.send_keys(Keys.RETURN)


def empty_directory(directory_path):
    try:
        # Iterate through all files and subdirectories in the specified directory
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                # Remove files
                os.remove(item_path)
            elif os.path.isdir(item_path):
                # Remove subdirectories and their contents recursively
                shutil.rmtree(item_path)
        
        print(f"Directory '{directory_path}' has been emptied.")
    except Exception as e:
        print(f"Error emptying directory: {e}")


empty_directory('C:/Users/DenG/Desktop/desktop/aliexpress copy/static/imgs')


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



x = 0

for i in range(1,310):
    if x == 20:
        break
    try:
        if i == 1:
            time.sleep(4)
        d.implicitly_wait(1)
        print(i)
        current_element = d.find_element(By.XPATH, f'/html/body/div[3]/div[1]/div/div[2]/div/div[2]/div[3]/a[{i}]')
        current_element.click()
        d.switch_to.window(d.window_handles[1])
        time.sleep(3)


        title = d.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[1]/div[1]/div[2]/div[1]/h1').text
        img = d.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[1]/div[1]/div[1]/div/div/div/div[1]/img').get_attribute('src')
        # img = 'https://images.unsplash.com/photo-1422422153408-a3298d6d542c?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80'
        # img = 'https://ae01.alicdn.com/kf/S7e1fb763184947e998189cac889d07edy/YUQIAO-Fishing-Rod-Bag-Protective-Cover-Sleeve-Pocket-Fishing-Tackle-Bag-Folding-Portable-Fishing-Rod-Storage.jpg_220x220.jpg_.webp`'
        url = d.current_url
        price = d.find_element(By.CLASS_NAME, 'product-price-current').text

        filename = str(uuid.uuid4())+'.jpg'

        print(filename)
        # print(url)
        # print(title)
        # print(img)
        # print(price)

        download_image(img,'C:/Users/DenG/Desktop/desktop/aliexpress copy/static/imgs' , filename)
        c.execute(f'INSERT INTO reels (name, price, img_url, product_link) VALUES("{title}", "{price}", "{filename}", "{url}")')

        conn.commit()

        d.close()
        d.switch_to.window(d.window_handles[0])
        if i % 5 == 0:
            time.sleep(0.5)
            d.execute_script('window.scrollBy(0,300)')
            time.sleep(2)



        x+=1

    except Exception as e:
        d.close()
        d.implicitly_wait(2)
        d.switch_to.window(d.window_handles[0])
        print(e)

conn.commit()
conn.close()

