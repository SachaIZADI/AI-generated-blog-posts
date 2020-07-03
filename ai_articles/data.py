import requests
import functools
import json
from goose3 import Goose
import time
import pandas as pd

class Data(object):
    def __init__(self):
        pass

    @property
    @functools.lru_cache()
    def posts_urls(self):
        posts_urls = []
        for year in range(2017, 2021):
            posts_urls.extend(self.get_posts_by_year(year))
        return posts_urls

    def get_posts_by_year(self, year=2020):
        headers = {
            'authority': 'medium.com',
            'x-obvious-cid': 'web',
            'accept': 'application/json',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
            'content-type': 'application/json',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://medium.com/bcggamma/archive',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,fr;q=0.7',
        }

        response = requests.get(f'https://medium.com/bcggamma/archive/{year}', headers=headers)

        if response.status_code != 200:
            raise ConnectionError

        response_data = str(response.text).replace('])}while(1);</x>', '')
        payload = json.loads(response_data)["payload"]
        posts = payload["references"]["Post"]
        posts_url = [f"https://medium.com/bcggamma/{post['uniqueSlug']}" for _, post in posts.items()]

        return posts_url

    @property
    @functools.lru_cache()
    def posts_contents(self):
        posts_contents = [self.get_post_content("https://medium.com/bcggamma/the-complex-challenge-of-demand-forecasting-for-business-cfb50a269a41")]
        for post_url in self.posts_urls:
            post_content = self.get_post_content(post_url)
            posts_contents.append(post_content)
            print(post_content["title"])
            time.sleep(5)

        return posts_contents

    def get_post_content(self, post_url):
        g = Goose()
        article = g.extract(post_url)
        return {"title": article.title, "content": article.cleaned_text}

    def download(self, dst="data/posts"):
        posts_contents_table = pd.DataFrame(self.posts_contents)
        posts_contents_table.to_csv(f'{dst}.csv', index=False, sep="|")

        posts_contents_table["article"] = \
            "=========== " + posts_contents_table["title"] + " ===========" + "\n" + posts_contents_table["content"]
        full_content = posts_contents_table["article"].str.cat(sep="\n")

        with open(f'{dst}.txt', 'w+') as f:
            f.write(full_content)
