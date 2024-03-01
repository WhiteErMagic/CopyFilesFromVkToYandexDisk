import requests


class YDService:

    def __init__(self, oauth_disk):
        self.oauth_disk = oauth_disk

        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth ' + self.oauth_disk
        }

    def create_catalog(self, name_catalog):
        url = f'https://cloud-api.yandex.net/v1/disk/resources?path={name_catalog}'
        response = requests.put(url, headers=self.headers)
        return response.json()


    def upload_photo(self, name_photo):
        url = f'https://cloud-api.yandex.net/v1/disk/resources/upload'

        params = {
            'path': name_photo
        }
        response = requests.get(url, params=params, headers=self.headers)
        return response

    def upload_file(self, current_url_for_upload, file):
        response = requests.put(current_url_for_upload, files={'file': file})
        return response