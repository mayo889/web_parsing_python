import requests
from pprint import pprint

token = '-'
main_link = 'https://api.vk.com/method/groups.get'
params = {'user_id': '445111559',
          'access_token': token,
          'extended': '1',
          'v': '5.130',
          'fields': 'members_count'
          }

response = requests.get(main_link, params=params)
j_body = response.json()

print(f"Пользователь {params['user_id']} состоит в {j_body['response']['count']} группах:")

group_list = [(group['name'], group['members_count']) for group in j_body['response']['items']]
group_list.sort(key=lambda x: x[1], reverse=True)
for group in group_list:
    print('- ', group[0])