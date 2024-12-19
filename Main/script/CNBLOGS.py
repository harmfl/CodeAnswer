import json
import pandas as pd
from lxml import etree
import jsonpath
import requests
from bs4 import BeautifulSoup
import os
import argparse

# proxy = {'http': '127.0.0.1:5000', 'https': '127.0.0.1:5000'}
current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
result_dir = f'{current_directory}\\media\\'

class CSDN_Spider:
    def __init__(self,text):
        self.key_text=text
                       # https://so.csdn.net/api/v3/search?q=%E7%A8%8B%E5%BA%8F%E7%94%A8&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=&ct=-1&pnt=-1&ry=-1&ss=-1&dct=-1&vco=-1&cc=-1&sc=-1&akt=-1&art=-1&ca=-1&prs=&pre=&ecc=-1&ebc=-1&urw=&ia=1&dId=&cl=-1&scl=-1&tcl=-1&platform=pc&ab_test_code_overlap=&ab_test_random_cod
        self.text_url = f"https://zzk.cnblogs.com/s/blogpost?w={self.key_text}"
                       #f'https://so.csdn.net/api/v3/search?q={self.key_text}&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=&ct=-1&pnt=-1&ry=-1&ss=-1&dct=-1&vco=-1&cc=-1&sc=-1&akt=-1&art=-1&ca=-1&prs=&pre=&ecc=-1&ebc=-1&urw=&ia=1&dId=&cl=-1&scl=-1&tcl=-1&platform=pc&ab_test_code_overlap=&ab_test_random_code='
        self.text_headers= {
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-encoding':'gzip, deflate, br, zstd',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'connection':'keep-alive',
            'cookie':'_ga=GA1.1.282376121.1708526907; Hm_lvt_866c9be12d4a814454792b1fd0fed295=1734344303,1734433701; HMACCOUNT=F5CEFF2B5C3D8298; .Cnblogs.AspNetCore.Cookies=CfDJ8DfB03_iObVLoqH7ndAeeDgW8NVADek8m5ZrbNfHMze10IQa4-Ef-zVBaORSsHxPUyjlTjp_yBus0wwQHhdA4bwHqtL9OmpDDpKQkG9t0pz5tG-7_nEpQCTocVobAGUv4gm0PrbAF7BXOacZAUI7bKfCs62ESErX8AyJueZ9BeNZlqLF-skGI8Je9rg09ZIqlXLjzD3z5M3bV6ARXmLt5jx7_JTIIXoCNP4kBVi1xKmZX7ZICU4BYauNRQIfcOR2Ctx1oRu1AFbEnBKX0_JccL5CrRf9Kv54y3U0OHJ3hi4z4SVFtUJB83Lg1v_Wa62AFOBzJ7ILWPuD__coxJY4FTIB7UHmdUs1wXFVVXgsABEcA_DLu-IOh7uG0ltomgQt-77lpuGVGDT3t9Dz7RvoInO9HHdxSH8d767U3S5-bxdctFux8OSup06J2L9BiUrGEw-_Ik_8zen88-AUN-ULjyjXlrLmfy3_Fud8m29qZiVRevj9logpWMBm_VJRDBhzlsjR6KgzeaV71kchiJQBhsAjCZuDeBw2m9H9CCwAkX17gyz0e4DvC2yFu57lWkEkFA; .CNBlogsCookie=0EEE92AC2E65EED40523646E668BD30C1827C910CCAE8E7AA0616549C4F798B19BA2D7755EB86E235DADC5E76A3C1940D637F36A2AE9F5252157343A7A78C8E22312E349BA66E9C0BFA82AAB2893EC6A0319186C; _ga_3Q0DVSGN10=GS1.1.1734433702.1.1.1734433712.50.0.0; Hm_lpvt_866c9be12d4a814454792b1fd0fed295=1734433712; affinity=1734433737.058.42.806215|a6728cc07008ec0fd0d6b7ff6028a867; _ga_M95P3TTWJZ=GS1.1.1734433701.2.1.1734433734.0.0.0; __utma=59123430.282376121.1708526907.1720854128.1734433735.3; __utmc=59123430; __utmz=59123430.1734433735.3.3.utmcsr=cnblogs.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmt=1; __utmb=59123430.2.10.1734433735',
            'priority':'u=0, i',
            'referer':'https://zzk.cnblogs.com/s?w=C',
            'sec-ch-ua':'"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':"Windows",
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-origin',
            'user-agent':'Mozilla/5.0(Windows NT 10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/131.0.0.0Safari/537.36Edg/131.0.0.0'
        }

    def get_html_data(self,num):
        response = requests.get(self.text_url, headers=self.text_headers)

        if response.status_code == 200:
            response.encoding = response.apparent_encoding
            html = etree.HTML(response.text)

            a_tags = html.xpath('/html/body/div[3]/div/div[2]/div/h3/a')
            descriptions = html.xpath('/html/body/div[3]/div/div[2]/div/span')

            result_data = []
            for i in range(0,num):
                href = a_tags[i].attrib.get("href", "未找到链接")
                all_texts = a_tags[i].xpath('.//text()')  # 使用 '.' 表示当前 <a> 标签的子孙节点
                full_text = "".join(all_texts)  # 将文本拼接成一个字符串

                # 获取 <span> 的所有文字内容，包括 <strong> 中的文字
                description_texts = descriptions[i].xpath('.//text()')  # 获取当前 <span> 中所有子孙节点的文本
                full_description = "".join(description_texts).strip()

                result_data.append({
                    'title': full_text,
                    'description': full_description,
                    'url': href
                })
            file_path = os.path.join(result_dir, 'CNBLOGS.json')
            with open(file_path, 'w',encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=4)
                print(f"数据已成功写入 {file_path}")
                # print(full_text)  # 立即输出当前 <a> 的所有文字内容
                # print(f"{full_description}")  # 输出 <span> 的文字内容
                # print(f"链接: {href}")
                # print("-" * 50)

def run(text, num):
    CNBLOGS = CSDN_Spider(text)
    CNBLOGS.get_html_data(num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CNBLOGS爬虫脚本")
    parser.add_argument('--key_text', type=str, required=True, help="需要爬取的信息")
    parser.add_argument('--num', type=int, required=True, help="需要爬取的数量")
    args = parser.parse_args()

    run(args.key_text, args.num)
