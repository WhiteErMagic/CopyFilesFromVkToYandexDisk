import requests


class VKService:

    def __init__(self, access_token, user_id, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}


    def users_info(self):
        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


    def users_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.id,
                  'rev': 0,
                  'extended': 1,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'count': 1000}
        response = requests.get(url, params={**self.params, **params})
        return response.json()


    def get_photo(self, url):
        response = requests.get(url)
        return response
