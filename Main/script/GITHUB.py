import json
import pandas as pd
from lxml import etree
import jsonpath
import requests
from bs4 import BeautifulSoup
import html
import re
import os
import argparse

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
result_dir = f'{current_directory}\\media\\'
proxy = {'http': '127.0.0.1:10809', 'https': '127.0.0.1:7890'}

class GITHUB_Spider:
    def __init__(self,text):
        self.key_text=text
        self.text_url = f"https://github.com/search?q={self.key_text}&type=repositories"
        self.text_headers = {
            # ':authority': 'github.com',
            # ':method': 'GET',
            # ':path': '/search?q=yolo&type=repositories',
            # ':scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding': 'gzip, deflate, br, zstd',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'max-age=0',
            'cookie': '_octo=GH1.1.2023708209.1708420597; _device_id=bc913048c29f7f881c3590ff7bb40b88; saved_user_sessions=125250266%3ApWKAQE2ei1CMP40PRvOYBoxCuP0yMZo5nNqkjrcSJMJh42nY; user_session=pWKAQE2ei1CMP40PRvOYBoxCuP0yMZo5nNqkjrcSJMJh42nY; __Host-user_session_same_site=pWKAQE2ei1CMP40PRvOYBoxCuP0yMZo5nNqkjrcSJMJh42nY; logged_in=yes; dotcom_user=harmfl; color_mode=%7B%22color_mode%22%3A%22light%22%2C%22light_theme%22%3A%7B%22name%22%3A%22light%22%2C%22color_mode%22%3A%22light%22%7D%2C%22dark_theme%22%3A%7B%22name%22%3A%22dark_dimmed%22%2C%22color_mode%22%3A%22dark%22%7D%7D; cpu_bucket=xlg; preferred_color_mode=dark; tz=Asia%2FShanghai; _gh_sess=8RsRXLg5PNCQDCseXTIe1zhYx8ZXnRJ7fgYPWYG93WvoKCA1H1mYMvYaa%2B0%2BItwQrXRMb7w%2BrFPQxPXNLg0KcBmte05H%2B9x4vBYYNPFVlArXLNh%2Bi8mo6pz1BdJYE%2BYFAuj7UgbK5MBhD8CGRpqlVMKqIr5x4rufCanPQQwPyPm1E3ehTTA5LCU%2B6ZdDiAmZ7ODqoc%2FaO8reUL5I3ZKoit5PjqL6OIt9Bw%2FvUKmWa9yVWKHlegkdpB1OnDnXDHRhw9D7fOJHC0ka5WAqwvlhXCwYwTzDcwkcWEUY6XrI7ZWcnLIL4e0Ypk7w12wEGI1bE0mKctu5OR4UShi7gD3uZD5vMa4WW%2BreTOn41hq4fO0VzwMMZuOHZEyHgbD%2F182Rl4T3vwK%2B5HY%2FJGqbAlUWnk4Rw62vk7ObbVbVce%2FcD4u5wfcbNiGMfmc30TMvSodUJSzEk2a%2Bygc%3D--0MJYBbFeSum%2FR1pC--iz6YMqWGumDWLG25JfbAJA%3D%3D',
            'if-none-match': 'W/"7dc36cf4e2d8857a24a3d18030ab5b22"',
            'priority': 'u=0, i',
            'referer': 'https://github.com/',
            'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
        }

    def get_html_data(self,num):
        response = requests.get(self.text_url, headers=self.text_headers, proxies=proxy)
        # response = requests.get(self.text_url, headers=self.text_headers)
        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            soup = BeautifulSoup(response.text, "html.parser")
            # 提取嵌套 JSON 数据
            script_tag = soup.find("script", {"type": "application/json", "data-target": "react-app.embeddedData"})
            if script_tag is None:
                print("Target script tag not found.")
                return
            json_text = script_tag.string
            parsed_data = json.loads(json_text)
            # 提取 hl_name 和 hl_trunc_description
            results = parsed_data['payload']['results']
            result_data=[]
            for result in results[:num]:  # 仅取前 5 个结果
                hl_name = html.unescape(result['hl_name'])
                hl_description = html.unescape(result.get('hl_trunc_description', ''))  # 使用 get 防止不存在时出错
                # 去掉 <em> 标签
                clean_name = re.sub(r'</?em>', '', hl_name)
                clean_description = re.sub(r'</?em>', '', hl_description)
                result_data.append({
                    'title': clean_name,
                    'description': clean_description,
                    'url': f"https://github.com/{clean_name}"
                })
            file_path = os.path.join(result_dir, 'GITHUB.json')
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=4)
                print(f"数据已成功写入 {file_path}")

def run(text, num):
    GITHUB = GITHUB_Spider(text)
    GITHUB.get_html_data(num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GITHUB爬虫脚本")
    parser.add_argument('--key_text', type=str, required=True, help="需要爬取的信息")
    parser.add_argument('--num', type=int, required=True, help="需要爬取的数量")
    args = parser.parse_args()

    run(args.key_text, args.num)
