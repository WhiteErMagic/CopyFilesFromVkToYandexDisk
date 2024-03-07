import time

from VK import VKService
from YD import YDService
import json
import os
from os.path import abspath
from tqdm import tqdm
import configparser


config = configparser.ConfigParser() 
config.read("settings.ini")


def create_folder():
	dir_name = os.path.dirname(abspath(__file__))+'/output/'
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)

	return dir_name


def get_users_photos(vk: VKService):
	response = vk.users_photos()
	if response.failure:
		print(f'Error: {response.error}')
		return None
	else:
		return response.value.get('response').get('items')


def save_result(list_photos):
	with open('output_photos.json', 'w') as f_photos:
		json.dump(list_photos, f_photos)

def save_photos(list_users_photos, vk: VKService, yd: YDService):

	yd_catalog = 'myphoto'
	list_photos = []
	list_error = []

	for ind in tqdm(range(len(list_users_photos))):
		value = list_users_photos[ind]
		max_size_photo = value.get('sizes')[len(value.get('sizes')) - 1]
		url_vk_photo = vk.get_photo(max_size_photo.get('url'))

		current_name = str(value.get('date')) + '.jpg'

		yd.create_catalog(yd_catalog)

		result = yd.upload_photo(yd_catalog + '/' + current_name)
		if result.error:
			list_error.append(current_name)
			continue

		current_url_for_upload = result.value.get('href')

		yd.upload_file(current_url_for_upload, url_vk_photo.value)
		list_photos += [{'file_name': current_name,
							 'size': str(max_size_photo.get('height')) + 'x' + str(max_size_photo.get('width'))}]

		time.sleep(1)

	if len(list_error) > 0:
		print(f'Error upload: {", ".join(list_error)}')
	save_result(list_photos)

def processing_photo(vk: VKService):
	yd = YDService(config['keys']['oauth_disk'])
	list_users_photos = get_users_photos(vk)
	if list_users_photos is not None:
		save_photos(list_users_photos, vk, yd)

def main():
	input_data = input('Input Id or Name:')
	input_quantity_photo = input('Input quantity photo:')
	vk = VKService(config['keys']['access_token'], input_data, input_quantity_photo)
	if type(input_data) is str:
		response = vk.users_info()
		if response.success:
			vk.user_code = response.value['response'][0]['id']
			processing_photo(vk)
	else:
		processing_photo(vk)


if __name__ == "__main__":
	main()