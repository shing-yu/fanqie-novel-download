"""
作者：星隅（xing-yv）

版权所有（C）2023 星隅（xing-yv）

本软件根据GNU通用公共许可证第三版（GPLv3）发布；
你可以在以下位置找到该许可证的副本：
https://www.gnu.org/licenses/gpl-3.0.html

根据GPLv3的规定，您有权在遵循许可证的前提下自由使用、修改和分发本软件。
请注意，根据许可证的要求，任何对本软件的修改和分发都必须包括原始的版权声明和GPLv3的完整文本。

本软件提供的是按"原样"提供的，没有任何明示或暗示的保证，包括但不限于适销性和特定用途的适用性。作者不对任何直接或间接损害或其他责任承担任何责任。在适用法律允许的最大范围内，作者明确放弃了所有明示或暗示的担保和条件。

免责声明：
该程序仅用于学习和研究Python网络爬虫和网页处理技术，不得用于任何非法活动或侵犯他人权益的行为。使用本程序所产生的一切法律责任和风险，均由用户自行承担，与作者和项目协作者、贡献者无关。作者不对因使用该程序而导致的任何损失或损害承担任何责任。

请在使用本程序之前确保遵守相关法律法规和网站的使用政策，如有疑问，请咨询法律顾问。

无论您对程序进行了任何操作，请始终保留此信息。
"""

import json
import re
import os
import sys
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
from colorama import Fore, Style, init

init(autoreset=True)
proxies = {
    "http": None,
    "https": None
}
headers = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 "
                  "Mobile Safari/537.36"
}


# 替换非法字符
def rename(name):
    # 定义非法字符的正则表达式模式
    illegal_characters_pattern = r'[\/:*?"<>|]'

    # 定义替换的中文符号
    replacement_dict = {
        '/': '／',
        ':': '：',
        '*': '＊',
        '?': '？',
        '"': '“',
        '<': '＜',
        '>': '＞',
        '|': '｜'
    }

    # 使用正则表达式替换非法字符
    sanitized_path = re.sub(illegal_characters_pattern, lambda x: replacement_dict[x.group(0)], name)

    return sanitized_path


def fix_publisher(text):
    # 针对性去除所有 出版物 所携带的标签
    text = re.sub(r'<p class=".*?">', '', text)
    text = re.sub(r'<!--\?xml.*?>', '', text)
    text = re.sub(r'<link .*?/>', '', text)
    text = re.sub(r'<meta .*?/>', '', text)
    text = re.sub(r'<h1 .*?>', '', text)
    text = re.sub(r'<br/>', '', text)
    text = re.sub(r'<!DOCTYPE html .*?>', '', text)
    text = re.sub(r'<span .*?>', '', text)
    text = re.sub(r'<html .*?>', '', text)
    return text


def get_fanqie(url, mode='default'):

    # 获取网页源码

    response = requests.get(url, timeout=20, proxies=proxies)
    html = response.text

    # 解析网页源码
    soup = BeautifulSoup(html, "html.parser")

    # 获取小说标题
    title = soup.find("h1").get_text()
    # , class_ = "info-name"
    # 替换非法字符
    title = rename(title)

    # 获取小说信息
    info = soup.find("div", class_="page-header-info").get_text()

    # 获取小说简介
    intro = soup.find("div", class_="page-abstract-content").get_text()

    # 拼接小说内容字符串
    content = f"""如果需要小说更新，请勿修改文件名
使用 @星隅(xing-yv) 所作开源工具下载
开源仓库地址:https://github.com/xing-yv/fanqie-novel-download
Gitee:https://gitee.com/xingyv1024/fanqie-novel-download/
任何人无权限制您访问本工具，如果有向您提供代下载服务者未事先告知您工具的获取方式，请向作者举报:xing_yv@outlook.com

{title}
{info}
{intro}
"""

    # 获取所有章节链接
    chapters = soup.find_all("div", class_="chapter-item")

    if mode == 'epub':
        # 获取小说作者
        author_name = soup.find('span', class_='author-name-text').get_text()

        # 找到type="application/ld+json"的<script>标签
        script_tag = soup.find('script', type='application/ld+json')

        # 提取每个<script>标签中的JSON数据
        json_data = json.loads(script_tag.string)
        images_data = json_data.get('image', [])
        # 打印提取出的images数据
        img_url = images_data[0]

        return soup, title, author_name, intro, img_url

    return title, content, chapters


def get_api(chapter, mode='default'):

    # 获取章节标题
    chapter_title = chapter.find("a").get_text()
    # 去除非法字符
    chapter_title = rename(chapter_title)

    # 获取章节网址
    chapter_url = chapter.find("a")["href"]

    # 获取章节 id
    chapter_id = re.search(r"/reader/(\d+)", chapter_url).group(1)

    # 构造 api 网址
    api_url = (f"https://novel.snssdk.com/api/novel/book/reader/full/v1/?device_platform=android&"
               f"version_code=973&app_name=news_article&version_name=9.7.3&app_version=9.7.3&device_id=1&"
               f"channel=google&device_type=1&os_api=33&os_version=13&item_id={chapter_id}&aid=1319")
    # 尝试获取章节内容
    chapter_content = None
    while True:
        retry_count = 1
        while retry_count < 4:  # 设置最大重试次数
            try:
                # 获取 api 响应
                api_response = requests.get(api_url, headers=headers, timeout=5, proxies=proxies)

                # 解析 api 响应为 json 数据
                api_data = api_response.json()
            except Exception as e:
                if retry_count == 1:
                    tqdm.write(Fore.RED + Style.BRIGHT + f"发生异常: {e}")
                    tqdm.write(f"{chapter_title} 获取失败，正在尝试重试...")
                tqdm.write(f"第 ({retry_count}/3) 次重试获取章节内容")
                retry_count += 1  # 否则重试
                continue

            if "data" in api_data and "content" in api_data["data"]:
                chapter_content = api_data["data"]["content"]
                break  # 如果成功获取章节内容，跳出重试循环
            else:
                if retry_count == 1:
                    tqdm.write(f"{chapter_title} 获取失败，正在尝试重试...")
                tqdm.write(f"第 ({retry_count}/3) 次重试获取章节内容")
                retry_count += 1  # 否则重试

        if retry_count == 4:
            import tkinter as tk
            from tkinter import font, messagebox
            tqdm.write(Fore.RED + Style.BRIGHT + f"无法获取章节内容: {chapter_title}")
            tqdm.write(Fore.YELLOW + Style.BRIGHT + "请在弹出窗口中选择处理方式")
            choice = None

            def on_button_click(value):
                nonlocal choice
                choice = value
                window.destroy()

            # 弹窗请用户选择处理方式
            window = tk.Tk()
            window.title("番茄下载器 - 选择处理方式")
            # 获取屏幕宽度和高度
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            # 计算窗口宽和高
            x = (screen_width - 400) / 2
            y = (screen_height - 260) / 2
            window.geometry(f"400x260+{int(x)}+{int(y)}")

            # 不允许调整大小
            window.resizable(False, False)

            # 获取默认字体并设置字体大小
            default_font_family = font.nametofont("TkDefaultFont").actual()["family"]
            font1 = font.Font(family=default_font_family, size=12)
            font2 = font.Font(family=default_font_family, size=8)

            label = tk.Label(window, text=f"无法获取章节内容: \n{chapter_title}", pady=10, font=font1)
            label.pack()

            label2 = tk.Label(window, text="已达最大重试次数\n您希望程序如何处理此问题：", font=font2)
            label2.pack()

            button1_frame = tk.Frame(window)
            button1_frame.pack()
            button1 = tk.Button(button1_frame, text="跳过此章节 (1)", command=lambda: on_button_click("1"), font=font1)
            button1.pack(pady=5)

            button2_frame = tk.Frame(window)
            button2_frame.pack()
            button2 = tk.Button(button2_frame, text="再次重试 (2)", command=lambda: on_button_click("2"), font=font1)
            button2.pack(pady=5)

            button3_frame = tk.Frame(window)
            button3_frame.pack()
            button3 = tk.Button(button3_frame, text="终止下载并保存 (3)", command=lambda: on_button_click("3"),
                                font=font1)
            button3.pack(pady=5)

            def on_closing():
                messagebox.showwarning("警告", "您必须选择处理方式，程序才能继续运行")

            window.protocol("WM_DELETE_WINDOW", on_closing)

            window.mainloop()
            if choice == "1":
                return "skip"
            elif choice == "2":
                continue
            elif choice == "3":
                return "terminate"
        else:
            break

    # 提取文章标签中的文本
    chapter_text = re.search(r"<article>([\s\S]*?)</article>", chapter_content).group(1)

    if mode == 'epub':
        return chapter_title, chapter_text, chapter_id

    # 将 <p> 标签替换为换行符
    chapter_text = re.sub(r"<p\b[^>]*>", "\n", chapter_text)

    # 去除其他 html 标签
    chapter_text = re.sub(r"<[\x00-\x7F]*?>", "", chapter_text)

    chapter_text = fix_publisher(chapter_text)

    return chapter_title, chapter_text, chapter_id


def asset_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # noinspection PyProtectedMember
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("assets"), relative_path)
