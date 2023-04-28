import requests
import time
from tqdm import tqdm

def new_folder(ya_token):
    params = {'path': 'Фотографии с вк'}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'OAuth {}'.format(ya_token)
    }
    r = requests.put('https://cloud-api.yandex.net/v1/disk/resources', headers=headers, params=params)
    if r.status_code == 201:
        print('Папка "Фотографии с вк" создана!')
def dump_to_yadisk(ya_token, photo_url, photo_name):
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(ya_token)
        }
    params = {
            'path': f'Фотографии с вк/{photo_name}',
            'url': photo_url
        }
    response = requests.post(upload_url, headers=headers, params=params)
    if response.status_code == 202:
        print('Фотография загружена')
def put_vk_photos_in_yadisk(owner_id, ya_token):
    new_folder(ya_token)
    with open('token.txt', 'r') as file_obj:
        token = file_obj.read().strip()
    params = {
        'access_token': token,
        'v': '5.131',
        'owner_id': owner_id,
        'album_id': '292866854',
        'extended': '1',
        'photo_sizes': '1',
    }
    r = requests.get('https://api.vk.com/method/photos.get', params=params)
    results = []
    list_likes = []
    for item in tqdm(r.json()['response']['items']):
        height_photo = 0
        photo_url = ''
        type_photo = ''
        for size in item['sizes']:
            if size['height'] > height_photo:
                height_photo = size['height']
                photo_url = size['url']
                type_photo = size['type']
        likes = item["likes"]["user_likes"]
        date = item["date"]

        if not likes in list_likes:
            results.append({'filename': f'{likes}.png', 'size': type_photo})
            dump_to_yadisk(ya_token, photo_url, f'{likes}.png')
        else:
            results.append({'filename': f'{date}.png', 'size': type_photo})
            dump_to_yadisk(ya_token, photo_url, f'{date}.png')

        list_likes.append(likes)
        with open('vk-photos-data.json', 'w') as data_load:
            data_load.write(str(results))
        time.sleep(1)


if __name__ == '__main__':
    yadisk_token = 'y0_AgAAAAAXx97qAADLWwAAAADgH--KGSdWObIcTimzTI9XGF2ORU5emqo'
    vk_id = '795502811'
    put_vk_photos_in_yadisk(vk_id, yadisk_token)
