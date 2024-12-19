import json
import pandas as pd
from lxml import etree
import jsonpath
import requests
from bs4 import BeautifulSoup
import os
import argparse

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
result_dir = f'{current_directory}\\media\\'

class CSDN_Spider:
    def __init__(self,text):
        self.key_text=text
        self.text_url = f"https://api.juejin.cn/search_api/v1/search?aid=2608&uuid=7448952593832052278&spider=0&query={self.key_text}&id_type=0&cursor=0&limit=20&search_type=0&sort_type=0&version=1"
        self.text_headers= {
            ':authority':'api.juejin.cn',
            ':method':'GET',
            ':path':'/search_api/v1/search?aid=2608&uuid=7448952593832052278&spider=0&query=python&id_type=0&cursor=0&limit=20&search_type=0&sort_type=0&version=1',
            ':scheme':'https',
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding':'gzip, deflate, br, zstd',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cookie':'_tea_utm_cache_2608=undefined; __tea_cookie_tokens_2608=%257B%2522web_id%2522%253A%25227448952593832052278%2522%252C%2522user_unique_id%2522%253A%25227448952593832052278%2522%252C%2522timestamp%2522%253A1734344451148%257D; csrf_session_id=20f110afa026bd01d1a681246f0f7741; passport_csrf_token=2254954b05a49fc1a2cf85902d9c18fc; passport_csrf_token_default=2254954b05a49fc1a2cf85902d9c18fc; sid_guard=03a2803793673990dad411029cefb6ad%7C1734511355%7C31536000%7CThu%2C+18-Dec-2025+08%3A42%3A35+GMT; uid_tt=cadc836fed7d0b9044ac50b6058d4438; uid_tt_ss=cadc836fed7d0b9044ac50b6058d4438; sid_tt=03a2803793673990dad411029cefb6ad; sessionid=03a2803793673990dad411029cefb6ad; sessionid_ss=03a2803793673990dad411029cefb6ad; is_staff_user=false; sid_ucp_v1=1.0.0-KDE1MzgyOGQ3YjNhZDAxODY4YWQwZDI4N2I0ZjMyZTRhMzUyNWIxNTMKFgiTiuCV8M2tARD7lYq7BhiwFDgIQAsaAmxmIiAwM2EyODAzNzkzNjczOTkwZGFkNDExMDI5Y2VmYjZhZA; ssid_ucp_v1=1.0.0-KDE1MzgyOGQ3YjNhZDAxODY4YWQwZDI4N2I0ZjMyZTRhMzUyNWIxNTMKFgiTiuCV8M2tARD7lYq7BhiwFDgIQAsaAmxmIiAwM2EyODAzNzkzNjczOTkwZGFkNDExMDI5Y2VmYjZhZA; store-region=cn-gd; store-region-src=uid; _ga=GA1.2.299914130.1734511356; _gid=GA1.2.1805657751.1734511356; _ga_S695FMNGPJ=GS1.2.1734511356.1.0.1734511356.60.0.0; n_mh=KKCXC0sMQ9IO5vWE_IIvbei97zsKjr1X7l8zMK2hYkI',
            'priority':'u=1,i',
            'referer':'https://www.cnblogs.com/',
            'sec-ch-ua':'"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':"Windows",
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-origin',
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
        }

    def get_json_data(self,num):
        response = requests.get(self.text_url,self.text_headers)

        result_data = []
        if response.status_code == 200:
            res_json = json.loads(response.text)
            title_list=list(jsonpath.jsonpath(res_json, f'$...title'))
            brief_content_list=list(jsonpath.jsonpath(res_json, f'$...brief_content'))
            article_id_list = list(jsonpath.jsonpath(res_json, f'$..{"article_info.article_id"}'))
            for i in range(0,num):
                soup = BeautifulSoup(title_list[i], "html.parser")
                a = soup.get_text()
                result_data.append({
                    'title': a,
                    'description': brief_content_list[i],
                    'url': f'https://juejin.cn/post/{article_id_list[i]}?searchId=20241218165919F890AB95398FA559D906'
                })
            file_path = os.path.join(result_dir, 'JUEJIN.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=4)
                print(f"数据已成功写入 {file_path}")

def run(text, num):
    CNBLOGS = CSDN_Spider(text)
    CNBLOGS.get_json_data(num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="JUEJIN爬虫脚本")
    parser.add_argument('--key_text', type=str, required=True, help="需要爬取的信息")
    parser.add_argument('--num', type=int, required=True, help="需要爬取的数量")
    args = parser.parse_args()

    run(args.key_text, args.num)
