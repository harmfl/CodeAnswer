import json
import pandas as pd
from lxml import etree
import jsonpath
import requests
from bs4 import BeautifulSoup
import re
import os
import argparse

current_directory = os.getcwd()
parent_directory = os.path.dirname(current_directory)
result_dir = f'{current_directory}\\media\\'

class CSDN_Spider:
    def __init__(self,text):
        self.key_text=text
        self.text_url = f"https://so.csdn.net/api/v3/search?q={self.key_text}&t=all&p=1&s=0&tm=0&lv=-1&ft=0&l=&u=&ct=-1&pnt=-1&ry=-1&ss=-1&dct=-1&vco=-1&cc=-1&sc=-1&akt=-1&art=-1&ca=-1&prs=&pre=&ecc=-1&ebc=-1&urw=&ia=1&dId=&cl=-1&scl=-1&tcl=-1&platform=pc&ab_test_code_overlap=&ab_test_random_code="
        self.text_headers= {
            'accept':'application/json, text/plain, */*',
            'accept-encoding':'gzip, deflate, br, zstd',
            'accept-language':'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'connection':'keep-alive',
            'cookie':'Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22m0_74630006%22%2C%22scope%22%3A1%7D%7D; cf_clearance=S7I4u5Uq0fW0f.XkdQ74Ql13G39mLP9pv5zW12dKzIc-1714909557-1.0.1.1-PislYV9xkCA.Mds2dduOOM247_zN06LrFncrDK.1b0Ny7ea2Ftf.bzDccQ3hPss9xRh8YVJBFHrMBa1M7.qw.A; chat-version=2.1.1; cf_clearance=ForU1LS9UDxxAQxwfLUopmhKdM6XJXQAMku9myVrwbA-1716723966-1.0.1.1-z80Ks3Wo_wSxygx72MWTvY9pQ0b7WaO.ue7pvpdcIc7B7h9vXlag2nsgHcDm8pGTlBItyHr_sqqqq18dSYwAGQ; UN=m0_74630006; uuid_tt_dd=10_36584747540-1722062903137-256286; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_36584747540-1722062903137-256286!5744*1*m0_74630006; fid=20_50373850408-1723202837899-276634; historyList-new=%5B%5D; FCCDCF=%5Bnull%2Cnull%2Cnull%2Cnull%2Cnull%2Cnull%2C%5B%5B13%2C%22%5B%5C%22DBABL~BVQqAAAAAg%5C%22%2C%5B%5B7%2C%5B1733279473%2C860584000%5D%5D%5D%5D%22%5D%5D%5D; loginbox_strategy=%7B%22taskId%22%3A317%2C%22abCheckTime%22%3A1733554151201%2C%22version%22%3A%22ExpA%22%2C%22nickName%22%3A%22m0_74630006%22%7D; UserName=m0_74630006; UserInfo=f23ef8bd73a4497490cb8e28257052dc; UserToken=f23ef8bd73a4497490cb8e28257052dc; UserNick=; AU=5B3; BT=1733554185349; p_uid=U010000; csdn_newcert_m0_74630006=1; c_hasSub=true; creative_btn_mp=3; _clck=1xin1mw%7C2%7Cfrr%7C0%7C1810; c_segment=14; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1734323459,1734324814,1734326137,1734340593; HMACCOUNT=F5CEFF2B5C3D8298; dc_sid=98163b673ef0b9217aa3bfd3457d5e11; bc_bot_fp=4f28042d000ca4aca0ebf18a26e22298; dc_session_id=10_1734343453480.881931; referrer_search=1734343466878; bc_bot_session=1734344269ced70b581b897634; https_waf_cookie=4b15631a-56da-432b161fcad303a07b3a4b9043a42a9aea19; c_first_ref=cn.bing.com; __gads=ID=59686ee71498d14c:T=1733819175:RT=1734344333:S=ALNI_Mbnlr92GQWKZP6s8MxAfdKUyRdT3w; __gpi=UID=00000f893a232692:T=1733819175:RT=1734344333:S=ALNI_MYGrk_iEm2x6I8J--eC-3p4BPRVLg; __eoi=ID=166852229b09035f:T=1733819175:RT=1734344333:S=AA-Afjb4SVwOj5JY9ocHnccPvuPb; c_first_page=https%3A//blog.csdn.net/lzjgame/article/details/88914291; c_dsid=11_1734344352079.214656; c_page_id=default; _clsk=lwec6p%7C1734346533595%7C5%7C0%7Cr.clarity.ms%2Fcollect; c_pref=https%3A//blog.csdn.net/qq_42534026/article/details/105049343%3Fops_request_misc%3D%25257B%252522request%25255Fid%252522%25253A%252522f6e08ede7a14c8572c34279ded8dc2c6%252522%25252C%252522scm%252522%25253A%25252220140713.130102334..%252522%25257D%26request_id%3Df6e08ede7a14c8572c34279ded8dc2c6%26biz_id%3D0%26utm_medium%3Ddistribute.pc_search_result.none-task-blog-2%7Eall%7Esobaiduend%7Edefault-1-105049343-null-null.142%5Ev100%5Epc_search_result_base1%26utm_term%3D%25E4%25B8%25AD%25E6%2596%2587%25E7%25BB%25B4%25E5%259F%25BA%25E7%2599%25BE%25E7%25A7%2591%26spm%3D1018.2226.3001.4187; c_ref=https%3A//www.csdn.net/%3Fspm%3D1001.2101.3001.4476; bc_bot_token=1001734344269ced70b581b897634bf305b; bc_bot_rules=-; creativeSetApiNew=%7B%22toolbarImg%22%3A%22https%3A//img-home.csdnimg.cn/images/20230921102607.png%22%2C%22publishSuccessImg%22%3A%22https%3A//img-home.csdnimg.cn/images/20240229024608.png%22%2C%22articleNum%22%3A1%2C%22type%22%3A2%2C%22oldUser%22%3Atrue%2C%22useSeven%22%3Afalse%2C%22oldFullVersion%22%3Atrue%2C%22userName%22%3A%22m0_74630006%22%7D; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1734348107; log_Id_pv=11; log_Id_view=519; dc_tos=sol3mb; fe_request_id=1734348182108_2188_6904821; log_Id_click=20',
            'host':'so.csdn.net',
            'referer':'https://so.csdn.net/so/search?',
            'sec-ch-ua':'"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            'sec-ch-ua-mobile':'?0',
            'sec-ch-ua-platform':"Windows",
            'sec-fetch-dest':'empty',
            'sec-fetch-mode':'cors',
            'sec-fetch-site':'same-origin',
            'user-agent':'Mozilla/5.0(Windows NT 10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/131.0.0.0Safari/537.36Edg/131.0.0.0'
        }

    def get_json_data(self, num):
        response = requests.get(self.text_url, headers=self.text_headers)

        # 确保请求成功
        if response.status_code == 200:
            res_json = json.loads(response.text)

            # 获取标题、描述和URL
            title_list = list(jsonpath.jsonpath(res_json, f'$...{"title"}'))
            description_list = list(jsonpath.jsonpath(res_json, f'$...{"digest"}'))
            url_list = list(jsonpath.jsonpath(res_json, f'$...{"url"}'))

            # 确保保存目录存在
            os.makedirs(result_dir, exist_ok=True)

            # 用于保存结果的列表
            result_data = []

            # 遍历每个条目，提取并保存信息
            for i in range(num):
                soup = BeautifulSoup(title_list[i], "html.parser")
                title = soup.get_text()

                description = re.sub(r'</?em>', '', description_list[i])
                url = url_list[i+1] if i < len(url_list) else ''

                # 创建一个字典保存该条目的数据
                result_data.append({
                    'title': title,
                    'description': description,
                    'url': url
                })

            # 定义文件路径
            file_path = os.path.join(result_dir, 'CSDN.json')

            # 将数据写入到 JSON 文件中
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, ensure_ascii=False, indent=4)

            print(f"数据已成功写入 {file_path}")


def run(key_text,num):
    CSDN = CSDN_Spider(key_text)
    CSDN.get_json_data(num)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="CSDN爬虫脚本")
    parser.add_argument('--key_text', type=str, required=True, help="需要爬取的信息")
    parser.add_argument('--num', type=int, required=True, help="需要爬取的数量")
    args = parser.parse_args()

    run(args.key_text, args.num)
