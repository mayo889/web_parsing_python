import requests

username = 'mayo889'

response = requests.get('https://api.github.com/users/' + username + '/repos')
j_body = response.json()

print(f"Список открытых репозиториев пользователя {username}:")
for repo in j_body:
    print(f"\t{repo['name']}")