import requests

image_url = "https://ae01.alicdn.com/kf/Sfff6a98e60df4493b861d96ce0968714F/3000-4000-5000-Ultralight-15kg-Surfcasting.jpg_.webp"
filename = "image.jpg"

response = requests.get(image_url)
if response.status_code == 200:
    with open(filename, 'wb') as file:
        file.write(response.content)
    print(f"Image downloaded and saved as {filename}")
else:
    print("Failed to download the image")