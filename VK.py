import requests
from Result import Result

class VKService:

    def __init__(self, access_token, user_code, input_quantity_photo, version='5.131'):
        self.token = access_token
        self.user_code = user_code
        self.version = version
        self.input_quantity_photo = input_quantity_photo
        self.params = {'access_token': self.token, 'v': self.version}


    def users_info(self):
        url = 'https://api.vk.com/method/users.get'

        #params = {}
        #url = f'https://vk.com/id{self.user_code}'
        response = requests.get(url, params={**self.params})

        if response.status_code == 200:
            return Result(True, response.json(), "")
        else:
            return Result(False, response.json(), response.json())


    def users_photos(self)->Result:
        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.user_code,
                  'rev': 0,
                  'extended': 1,
                  'album_id': 'profile',
                  'photo_sizes': 1,
                  'count': self.input_quantity_photo}
        response = requests.get(url, params={**self.params, **params})

        if response.status_code == 200:
            if response.json().get('error'):
                return Result(False, response.json().get('error'), str(response.json().get('error')))
            else:
                return Result(True, response.json(), "")
        else:
            return Result(False, response.json(), response.json())


    def get_photo(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return Result(True, response.content, "")
        else:
            return Result(False, response.text, response.text)
