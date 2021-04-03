import scrapy
import re
import json
from urllib.parse import urlencode
from copy import deepcopy
from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem

class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://www.instagram.com/']

    inst_login = 'mayo_866'
    inst_pwd = '#'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    parse_users = ['khramov_v_a', 'ermakovamash']

    graphql_url = 'https://www.instagram.com/graphql/query/?'
    followed_hash = '5aefa9893005572d237da5068082d8d5'
    follow_hash = '3dec7e2c57367ef3da3d987d89f9dbc8'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.user_parse,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def user_parse(self, response: HtmlResponse):
        j_body = json.loads(response.text)
        if j_body['authenticated']:
            for user in self.parse_users:
                yield response.follow(
                    f"/{user}",
                    callback=self.user_data_parse,
                    cb_kwargs={'username': user}
                )

    def user_data_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'include_reel': 'true',
                     'fetch_mutual': 'false',
                     'first': 49}
        url_followed = f"{self.graphql_url}query_hash={self.followed_hash}&{urlencode(variables)}"
        url_follows = f"{self.graphql_url}query_hash={self.follow_hash}&{urlencode(variables)}"

        yield response.follow(
            url_followed,
            callback=self.user_follow_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'edge': 'edge_followed_by',
                       'query_hash': self.followed_hash,
                       'variables': deepcopy(variables)}
        )

        yield response.follow(
            url_follows,
            callback=self.user_follow_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'edge': 'edge_follow',
                       'query_hash': self.follow_hash,
                       'variables': deepcopy(variables)}
        )

    # Для обработки подписчиков и подписок используем одну функцию,
    # так как структура JSON у них отличается только в одном месте
    # вложенный словарь edge_followed_by для подписчиков и edge_follow для подписок
    # различия храним в переменной edge.
    # query_hash также передаем в cb_kwargs, чтобы не дублировать код
    def user_follow_parse(self, response: HtmlResponse, username, user_id, edge, query_hash, variables):
        j_data = json.loads(response.text)
        page_info = j_data['data']['user'][edge]['page_info']
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            url_users = f"{self.graphql_url}query_hash={query_hash}&{urlencode(variables)}"
            yield response.follow(
                url_users,
                callback=self.user_follow_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'edge': edge,
                           'query_hash': query_hash,
                           'variables': deepcopy(variables)}
            )
        users = j_data['data']['user'][edge]['edges']
        status = 'follower' if edge == 'edge_followed_by' else 'following'
        for user in users:
            yield InstaparserItem(
                user_id=user_id,
                username=username,
                status=status,
                follow_id=user['node']['id'],
                follow_username=user['node']['username'],
                follow_pic_url=user['node']['profile_pic_url'],
                # follow_data=user['node']
            )

    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search('{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text).group()
        return json.loads(matched).get('id')
