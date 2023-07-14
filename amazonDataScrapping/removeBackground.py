import requests
import json
import os
import pandas as pd


def download_image(image_url, photo_path):
    response = requests.get(image_url)
    response.raise_for_status()
    with open(photo_path, "wb") as photo:
        photo.write(response.content)


def remove_background(photo_path):
    url = "https://api.removal.ai/3.0/remove"
    files = [
        ('image_file', ('image.jpg', open(photo_path, 'rb'), 'image/jpeg'))
    ]
    headers = {
        'Rm-Token': '64ac55f8c1a0f6.82394338'
    }
    response = requests.post(url, headers=headers, files=files)
    response_data = json.loads(response.text)
    image_url = response_data["url"]
    image_response = requests.get(image_url)
    if image_response.status_code == 200:
        with open(photo_path, "wb") as image_file:
            image_file.write(image_response.content)


def without_background(file_name):
    data = {'title': [], 'price': [], 'rating': [], 'reviews': [], 'image_link': []}
    df = pd.read_csv(file_name + '.csv')
    data['title'].extend(df['title'].tolist())
    data['price'].extend(df['price'].tolist())
    data['rating'].extend(df['rating'].tolist())
    data['reviews'].extend(df['reviews'].tolist())
    data['image_link'].extend(df['image_link'].tolist())
    for i in range(len(data['image_link'])):
        filename = os.path.basename(data['image_link'][i])
        temp = "productImages/" + filename
        photo_path = os.path.join("..", temp)
        download_image(data['image_link'][i], photo_path)
        remove_background(photo_path)
        data['image_link'][i] = filename
    new_csv_file = file_name + "_ameliorated"
    updated_csv = pd.DataFrame.from_dict(data)
    updated_csv.to_csv(new_csv_file + '.csv', header=True, index=False)


if __name__ == '__main__':
    file_names = ['home_audio', 'computer_accessories']
    for i in file_names:
        without_background(i)
