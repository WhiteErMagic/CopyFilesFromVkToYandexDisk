import time

from VK import VKService
from YD import YDService
import json
import os
from os.path import abspath
from tqdm import tqdm, trange
from time import sleep


with open('keys.txt', 'r', encoding='utf-8') as f_keys:
    lines = f_keys.read().splitlines()

dict_keys = {}
for line in lines:
	key,value = line.split(':')
	dict_keys.update({key:value})

def create_folder():
	dir_name = os.path.dirname(abspath(__file__))+'/output/'
	if not os.path.exists(dir_name):
		os.makedirs(dir_name)

	return dir_name


vk = VKService(dict_keys.get('access_token'), dict_keys.get('user_id'))
yd = YDService(dict_keys.get('oauth_disk'))
dir_name = create_folder()
list_response = vk.users_photos().get('response').get('items')
list_photos = []
yd_catalog = 'myphoto'
num_f = 0

for ind in tqdm(range(len(list_response))):
	value = list_response[ind]
	max_size_photo = value.get('sizes')[len(value.get('sizes'))-1]
	photo = vk.get_photo(max_size_photo.get('url'))

	# С одинаковым количеством лайков последний файл запишется
	likes = value.get('likes').get('count')
	if likes > num_f:
		num_f = likes
	else:
		num_f += 1

	current_name = str(num_f) + '.jpg'

	with open(dir_name+current_name, 'wb') as f_output:
		f_output.write(photo.content)

	resp = yd.create_catalog(yd_catalog)

	current_url_for_upload = yd.upload_photo(yd_catalog+'/'+current_name)
	status_code = current_url_for_upload.status_code
	if(status_code != 200):
		continue

	current_url_for_upload = current_url_for_upload.json().get('href')

	with open(dir_name+current_name, 'rb') as file:
		response = yd.upload_file(current_url_for_upload, file)
		list_photos += [{'file_name': current_name,
						 'size': str(max_size_photo.get('height')) + 'x' + str(max_size_photo.get('width'))}]

	time.sleep(1)


with open('output_photos.txt', 'w') as f_photos:
	json.dump(list_photos, f_photos)


