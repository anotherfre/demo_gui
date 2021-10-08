import requests
import random
import string


def download_image(text):
    url_list = text.split('//')
    for url in url_list:
        image_name = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        resp = requests.get(url)
        if resp.status_code == 200:
            with open(image_name, 'wb') as f:
                f.write(resp.content)
