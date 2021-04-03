from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client.instagram
collections = ['khramov_v_a', 'ermakovamash']
status = ['follower', 'following']

for collection in collections:
    for stat in status:
        results = db[collection].find({'status': stat})
        print(f"\n\n\n{'*' * 40}\n{collection}")
        print(f"{stat}\n{'*' * 40}")
        for result in results:
            pprint(result)

# Пример вывода (По 1 подписчику и подписке для каждого пользователя
# ****************************************
# khramov_v_a
# follower
# ****************************************
# {'_id': ObjectId('60686fe0a3d20f48cfab8819'),
#  'follow_id': '44646804732',
#  'follow_pic_url': {'checksum': 'b86ddf143f58fa802f6655c36d9428a9',
#                     'path': 'khramov_v_a/follower/zolnikovdn.jpg',
#                     'status': 'downloaded',
#                     'url': 'https://instagram.fkul13-1.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.fkul13-1.fna.fbcdn.net&_nc_ohc=NyXVWUpcBzMAX-wgQP7&edm=AD35FJ8AAAAA&ccb=7-4&oh=574ed0f497ddeb7125c5475162ce85ce&oe=608E2CCF&_nc_sid=74408c&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4'},
#  'follow_username': 'zolnikovdn',
#  'status': 'follower',
#  'user_id': '5840540785',
#  'username': 'khramov_v_a'}
#
# ****************************************
# khramov_v_a
# following
# ****************************************
# {'_id': ObjectId('60686fdfa3d20f48cfab8818'),
#  'follow_id': '42339642138',
#  'follow_pic_url': {'checksum': 'b86ddf143f58fa802f6655c36d9428a9',
#                     'path': 'khramov_v_a/following/lastsoul696.jpg',
#                     'status': 'downloaded',
#                     'url': 'https://instagram.fbom3-2.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=instagram.fbom3-2.fna.fbcdn.net&_nc_ohc=NyXVWUpcBzMAX_m8xaq&edm=AEsR1pMAAAAA&ccb=7-4&oh=682a5b97f2f666c3f74b3655b50b4859&oe=608E2CCF&_nc_sid=3f45ac&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4'},
#  'follow_username': 'lastsoul696',
#  'status': 'following',
#  'user_id': '5840540785',
#  'username': 'khramov_v_a'}
#
# ****************************************
# ermakovamash
# follower
# ****************************************
# {'_id': ObjectId('60686fdda3d20f48cfab8811'),
#  'follow_id': '34223828779',
#  'follow_pic_url': {'checksum': 'b86ddf143f58fa802f6655c36d9428a9',
#                     'path': 'ermakovamash/follower/926474637__.jpg',
#                     'status': 'downloaded',
#                     'url': 'https://scontent-frx5-1.cdninstagram.com/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?_nc_ht=scontent-frx5-1.cdninstagram.com&_nc_ohc=NyXVWUpcBzMAX_UyZ5M&edm=AI8ESKwAAAAA&ccb=7-4&oh=a24bf638a6ed4872311cfe6ea25283bc&oe=608E2CCF&_nc_sid=195af5&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4'},
#  'follow_username': '926474637__',
#  'status': 'follower',
#  'user_id': '539119743',
#  'username': 'ermakovamash'}
#
# ****************************************
# ermakovamash
# following
# ****************************************
# {'_id': ObjectId('60686fdba3d20f48cfab880e'),
#  'follow_id': '7629731064',
#  'follow_pic_url': {'checksum': '255ffd930de0392bbdb6180280dff2dc',
#                     'path': 'ermakovamash/following/alesya.isteleva.jpg',
#                     'status': 'downloaded',
#                     'url': 'https://scontent-arn2-2.cdninstagram.com/v/t51.2885-19/s150x150/43344951_329262574335684_2413018480656777216_n.jpg?tp=1&_nc_ht=scontent-arn2-2.cdninstagram.com&_nc_ohc=FEp_stryGTAAX_otg_m&edm=ANg5bX4AAAAA&ccb=7-4&oh=32f425f22ad9d17eacd48d05ff4c4fb1&oe=608DE1FF&_nc_sid=55937d'},
#  'follow_username': 'alesya.isteleva',
#  'status': 'following',
#  'user_id': '539119743',
#  'username': 'ermakovamash'}
