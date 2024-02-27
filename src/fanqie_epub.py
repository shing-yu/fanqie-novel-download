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
import os
import yaml

# 导入必要的模块
import requests
from bs4 import BeautifulSoup
from ebooklib import epub
import re
import time
import json
from tqdm import tqdm
import public as p
from requests.exceptions import Timeout
from colorama import Fore, Style, init

init(autoreset=True)


# 定义正常模式用来下载番茄小说的函数
def fanqie_epub(url, user_agent, path_choice, config_path):
    headers = {
        "User-Agent": user_agent
    }

    # 创建epub电子书
    book = epub.EpubBook()

    proxies = {
        "http": None,
        "https": None
    }

    # 获取书籍id
    book_id = re.search(r'\d+', url).group()

    # 获取网页源码
    try:
        response = requests.get(url, headers=headers, timeout=20, proxies=proxies)
    except Timeout:
        print(Fore.RED + Style.BRIGHT + "连接超时，请检查网络连接是否正常。")
        return
    except AttributeError:
        print(Fore.RED + Style.BRIGHT + "获取详情失败：该小说不存在或禁止网页阅读！（或网络连接异常）")
        return
    html = response.text

    # 解析网页源码
    soup = BeautifulSoup(html, "html.parser")

    # 获取小说标题
    title = soup.find("h1").get_text()
    # , class_ = "info-name"
    # 替换非法字符
    title = p.rename(title)

    # 获取小说信息
    # info = soup.find("div", class_="page-header-info").get_text()

    # 获取小说简介
    intro = soup.find("div", class_="page-abstract-content").get_text()

    # 获取小说作者
    author_name = soup.find('span', class_='author-name-text').get_text()

    # 找到type="application/ld+json"的<script>标签
    script_tag = soup.find('script', type='application/ld+json')

    # 提取每个<script>标签中的JSON数据
    json_data = json.loads(script_tag.string)
    images_data = json_data.get('image', [])
    # 打印提取出的images数据
    img_url = images_data[0]

    # 下载封面
    response = requests.get(img_url, timeout=20)
    # 获取图像的内容
    img_data = response.content

    # 保存图像到本地文件
    with open("cover.jpg", "wb") as f:
        f.write(img_data)

    # 创建一个封面图片
    book.set_cover("image.jpg", open('cover.jpg', 'rb').read())

    # 删除封面
    os.remove('cover.jpg')

    # 设置书的元数据
    book.set_title(title)
    book.set_language('zh-CN')
    book.add_author(author_name)
    book.add_metadata('DC', 'description', intro)

    yaml_data = {
        'fqid': book_id
    }
    yaml_content = yaml.dump(yaml_data)

    # 设置 fqid 元数据
    yaml_item = epub.EpubItem(uid='yaml', file_name='metadata.yaml', media_type='application/octet-stream',
                              content=yaml_content)
    book.add_item(yaml_item)

    # 获取卷标
    page_directory_content = soup.find('div', class_='page-directory-content')
    nested_divs = page_directory_content.find_all('div', recursive=False)

    # intro chapter
    intro_e = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='hr')
    intro_e.content = (f'<img src="image.jpg" alt="Cover Image"/>'
                       f'<h1>{title}</h1>'
                       f'<p>{intro}</p>')
    book.add_item(intro_e)

    font_file = p.asset_path("Xingyv-Regular.ttf")
    css1_file = p.asset_path("page_styles.css")
    css2_file = p.asset_path("stylesheet.css")
    # 打开资源文件
    with open(font_file, 'rb') as f:
        font_content = f.read()
    with open(css1_file, 'r', encoding='utf-8') as f:
        css1_content = f.read()
    with open(css2_file, 'r', encoding='utf-8') as f:
        css2_content = f.read()

    # 创建一个EpubItem实例来存储你的字体文件
    font = epub.EpubItem(
        uid="font",
        file_name="fonts/Xingyv-Regular.ttf",  # 这将是字体文件在epub书籍中的路径和文件名
        media_type="application/x-font-ttf",
        content=font_content,
    )
    # 创建一个EpubItem实例来存储你的CSS样式
    nav_css1 = epub.EpubItem(
        uid="style_nav1",
        file_name="style/page_styles.css",  # 这将是CSS文件在epub书籍中的路径和文件名
        media_type="text/css",
        content=css1_content,
    )
    nav_css2 = epub.EpubItem(
        uid="style_nav2",
        file_name="style/stylesheet.css",  # 这将是CSS文件在epub书籍中的路径和文件名
        media_type="text/css",
        content=css2_content,
    )

    # 将资源文件添加到书籍中
    book.add_item(font)
    book.add_item(nav_css1)
    book.add_item(nav_css2)

    # 创建索引
    book.toc = (epub.Link('intro.xhtml', '简介', 'intro'),)
    book.spine = ['nav', intro_e]

    try:
        volume_id = 0
        # 遍历每个卷
        for div in nested_divs:
            first_chapter = None
            volume_id += 1
            volume_div = div.find('div', class_='volume')
            # 提取 "卷名" 文本
            volume_title = volume_div.text
            print(volume_title)
            chapters = div.find_all("div", class_="chapter-item")

            # 定义目录索引
            toc_index = ()

            chapter_id_name = 0
            # 遍历每个章节链接
            for chapter in tqdm(chapters):
                chapter_id_name += 1
                time.sleep(0.25)

                # 获取章节内容
                chapter_title, chapter_text, chapter_id = p.get_api(chapter, headers, mode='epub')

                # 在小说内容字符串中添加章节标题和内容
                text = epub.EpubHtml(title=chapter_title, file_name=f'chapter_{volume_id}_{chapter_id_name}.xhtml')
                text.add_item(nav_css1)
                text.add_item(nav_css2)
                text.content = (f'<h2 class="titlecss">{chapter_title}</h2>'
                                f'{chapter_text}')

                toc_index = toc_index + (text,)
                book.spine.append(text)

                # 寻找第一章
                if chapter_id_name == 1:
                    first_chapter = f'chapter_{volume_id}_{chapter_id_name}.xhtml'

                # 加入epub
                book.add_item(text)

                # 打印进度信息
                tqdm.write(f"已获取 {chapter_title}")
            # 加入书籍索引
            book.toc = book.toc + ((epub.Section(volume_title, href=first_chapter),
                                   toc_index,),)
    except BaseException as e:
        # 捕获所有异常
        print(Fore.RED + Style.BRIGHT + f"发生异常: \n{e}")
        return

    # 添加 navigation 文件
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    file_path = None
    # 根据main.py中用户选择的路径方式，选择自定义路径或者默认
    if path_choice == 1:
        import tkinter as tk
        from tkinter import filedialog
        # 创建一个Tkinter窗口，但不显示它
        root = tk.Tk()
        root.withdraw()

        print("您选择了自定义保存路径，请您在弹出窗口中选择路径。")

        # 设置默认文件名和扩展名
        default_extension = ".epub"
        default_filename = f"{title}"

        while True:

            # 弹出文件对话框以选择保存位置和文件名
            file_path = filedialog.asksaveasfilename(
                defaultextension=default_extension,
                filetypes=[("Text Files", "*" + default_extension)],
                initialfile=default_filename
            )

            # 检查用户是否取消了对话框
            if not file_path:
                # 用户取消了对话框，提示重新选择
                print("您没有选择路径，请重新选择！")
                continue
            break
        # 询问用户是否保存此路径
        cho = input("是否使用此路径覆盖此模式默认保存路径（y/n(d)）？")
        if not cho or cho == "n":
            pass
        else:
            # 提取文件夹路径
            folder_path = os.path.dirname(file_path)
            # 如果配置文件不存在，则创建
            if not os.path.exists(config_path):
                with open(config_path, "w") as c:
                    json.dump({"path": {"epub": folder_path}}, c)
            else:
                with open(config_path, "r") as c:
                    config = json.load(c)
                config["path"]["epub"] = folder_path
                with open(config_path, "w") as c:
                    json.dump(config, c)

    elif path_choice == 0:
        # 定义文件名，检测是否有默认路径
        if not os.path.exists(config_path):
            file_path = title + ".epub"
        else:
            with open(config_path, "r") as c:
                config = json.load(c)
            if "epub" in config["path"]:
                file_path = os.path.join(config["path"]["epub"], f"{title}.epub")
            else:
                file_path = title + ".epub"

    epub.write_epub(file_path, book, {})

    print("文件已保存！")
    return
