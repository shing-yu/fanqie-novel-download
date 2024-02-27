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
import time
# 导入必要的模块
from urllib.parse import urljoin
import datetime
import re
import os

import requests
import yaml
from bs4 import BeautifulSoup
from ebooklib import epub
from tqdm import tqdm
import hashlib
import public as p
from requests.exceptions import Timeout
from colorama import Fore, Style, init

init(autoreset=True)


# 定义番茄更新函数
def fanqie_update(user_agent, data_folder):
    # 请用户选择更新模式
    while True:
        update_mode = input("请选择更新模式:1 -> 单个更新 2-> 批量更新 3-> epub批量\n")
        if not update_mode:
            update_mode = '1'
        if update_mode == '1':
            onefile(user_agent, data_folder)
            return
        elif update_mode == '2':
            break
        elif update_mode == '3':
            epub_batch_update(user_agent)
            return
        else:
            print("无效的选择，请重新输入。")

    # 指定小说文件夹
    novel_folder = "更新"

    os.makedirs(novel_folder, exist_ok=True)

    input("请在程序目录下”更新“文件夹内放入需更新的文件\n按 Enter 键继续...")

    novel_files = [file for file in os.listdir(novel_folder) if file.endswith(".txt")]

    if not novel_files:
        print("没有可更新的文件")
        return

    no_corresponding_files = True  # 用于标记是否存在对应的txt和upd文件

    for txt_file in novel_files:
        txt_file_path = os.path.join(novel_folder, txt_file)
        # 寻找book_id
        # with open(txt_file_path, "r") as tmp:
        #     # 读取第一行
        #     first_line = tmp.readline().strip()  # 读取并去除前后空白字符
        #
        #     # 检测是否全部是数字
        #     if first_line.isdigit():
        #         book_id = first_line
        #     else:
        #         print(f"{txt_file} 不是通过此工具下载，无法更新")

        upd_file_path = os.path.join(data_folder, txt_file.replace(".txt", ".upd"))
        novel_name = txt_file.replace(".txt", "")

        if os.path.exists(upd_file_path):

            print(f"正在尝试更新: {novel_name}")
            # 读取用于更新的文件元数据
            with open(upd_file_path, 'r') as file:
                lines = file.readlines()

            # 保存上次更新时间和上次章节id到变量
            last_update_time = lines[0].strip()
            url = lines[1].strip()
            last_chapter_id = lines[2].strip()
            if last_chapter_id == "None":
                print(Fore.RED + Style.BRIGHT + "信息文件已损坏，可能由于使用2.8.0/1/2版本导致，请重新下载此小说")
                continue
            encoding = lines[3].strip()
            if len(lines) >= 5:
                save_sha256 = lines[4].strip()
                skip_hash = 0
            else:
                print(Fore.YELLOW + Style.BRIGHT + "此小说可能由老版本下载，跳过hash校验")
                save_sha256 = None
                skip_hash = 1
            hash_sha256 = hashlib.sha256()
            with open(txt_file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            fact_sha256 = hash_sha256.hexdigest()
            if skip_hash == 0:
                if fact_sha256 != save_sha256:
                    print(Fore.RED + Style.BRIGHT + "hash校验未通过！")
                    while True:
                        upd_choice = input(f"这往往意味着文件已被修改，是否继续更新？(yes/no):")
                        if upd_choice == "yes":
                            skip_this = 0
                            break
                        elif upd_choice == "no":
                            skip_this = 1
                            break
                        else:
                            print("输入错误，请重新输入")
                    if skip_this == 1:
                        print(Fore.RED + Style.BRIGHT + f"《{novel_name}》的更新已取消")
                        continue
                else:
                    print(Fore.GREEN + Style.BRIGHT + "hash校验通过！")
            print(f"上次更新时间{last_update_time}")
            result = download_novel(url, encoding, user_agent, last_chapter_id, txt_file_path)
            if result == "DN":
                print(f"{novel_name} 已是最新，不需要更新。\n")
            elif result == "Timeout":
                print(Fore.RED + Style.BRIGHT + "更新失败")
            elif result == "Not Found":
                print(Fore.RED + Style.BRIGHT + "更新失败")
            else:
                print(f"{novel_name} 已更新完成。\n")
                # 计算文件 sha256 值
                hash_sha256 = hashlib.sha256()
                with open(txt_file_path, "rb") as f:
                    for chunk in iter(lambda: f.read(4096), b""):
                        hash_sha256.update(chunk)
                sha256_hash = hash_sha256.hexdigest()
                # 获取当前系统时间
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 创建要写入元信息文件的内容
                new_content = f"{current_time}\n{url}\n{result}\n{encoding}\n{sha256_hash}"
                # 打开文件并完全覆盖内容
                with open(upd_file_path, "w") as file:
                    file.write(new_content)

            no_corresponding_files = False
        else:
            print(f"{novel_name} 不是通过此工具下载，无法更新")

    if no_corresponding_files:
        print("没有可更新的文件")


# 定义更新番茄小说的函数
def download_novel(url, encoding, user_agent, start_chapter_id, txt_file_path):
    try:
        headers, _, content, chapters = p.get_fanqie(url, user_agent)
    except Timeout:
        print(Fore.RED + Style.BRIGHT + "连接超时，请检查网络连接是否正常。")
        return "Timeout"
    except AttributeError:
        print(Fore.RED + Style.BRIGHT + "该小说已不存在或禁止网页阅读！（或网络连接异常）")
        return "Not Found"

    last_chapter_id = None
    # 找到起始章节的索引
    start_index = 0
    for i, chapter in enumerate(chapters):
        chapter_url_tmp = urljoin(url, chapter.find("a")["href"])
        chapter_id_tmp = re.search(r"/(\d+)", chapter_url_tmp).group(1)
        if chapter_id_tmp == start_chapter_id:  # 更新函数，所以前进一个章节
            start_index = i + 1
        last_chapter_id = chapter_id_tmp

    # 判断是否已经最新
    if start_index >= len(chapters):
        return "DN"  # 返回Don't Need.

    # 打开文件
    with open(txt_file_path, 'ab') as f:
        chapter_id_now = start_chapter_id
        try:
            # 从起始章节开始遍历每个章节链接
            for chapter in tqdm(chapters[start_index:]):

                result = p.get_api(chapter, headers)

                if result is None:
                    continue
                else:
                    chapter_title, chapter_text, chapter_id_now = result

                # 在小说内容字符串中添加章节标题和内容
                content = f"\n\n\n{chapter_title}\n{chapter_text}"

                # 根据编码转换小说内容字符串为二进制数据
                data = content.encode(encoding, errors='ignore')

                # 将数据追加到文件中
                f.write(data)

                # 打印进度信息
                tqdm.write(f"已增加: {chapter_title}")

        except BaseException as e:

            # 捕获所有异常，及时保存文件
            print(Fore.RED + Style.BRIGHT + f"发生异常: \n{e}")
            print(Fore.RED + Style.BRIGHT + f"更新已被中断")

            return chapter_id_now

    # 返回更新完成
    return last_chapter_id


def onefile(user_agent, data_folder):
    txt_file_path = None
    while True:
        m_epub = False
        # 提示用户输入路径
        user_path = input("请将要更新的小说拖动到窗口中，然后按 Enter 键:（支持新版本下载的epub）\n")
        if ".txt" in user_path:
            pass
        elif ".epub" in user_path:
            m_epub = True
            print(Fore.YELLOW + Style.BRIGHT + "EPUB更新模式处于测试阶段，如发现问题请及时反馈。")
        else:
            print("路径不正确，请重新输入")
            continue

        # 使用os.path.normpath()来规范化路径
        txt_file_path = os.path.normpath(user_path)
        # 检测文件是否存在
        if os.path.exists(txt_file_path):
            break
        else:
            print("文件不存在，请重新输入")
            continue

    if m_epub is True:
        fanqie_epub_update(user_agent, user_path)
        return

    txt_file = os.path.basename(txt_file_path)
    # # 寻找book_id
    # with open(txt_file_path, "r") as tmp:
    #     # 读取第一行
    #     first_line = tmp.readline().strip()  # 读取并去除前后空白字符
    #
    #     # 检测是否全部是数字
    #     if first_line.isdigit():
    #         book_id = first_line
    #     else:
    #         print(f"{txt_file} 不是通过此工具下载，无法更新")

    upd_file_path = os.path.join(data_folder, txt_file.replace(".txt", ".upd"))
    novel_name = txt_file.replace(".txt", "")

    if os.path.exists(upd_file_path):

        print(f"正在尝试更新: {novel_name}")
        # 读取用于更新的文件元数据
        with open(upd_file_path, 'r') as file:
            lines = file.readlines()

        # 保存上次更新时间和上次章节id到变量
        last_update_time = lines[0].strip()
        url = lines[1].strip()
        last_chapter_id = lines[2].strip()
        if last_chapter_id == "None":
            print(Fore.RED + Style.BRIGHT + "信息文件已损坏，可能由于使用2.8.0/1/2版本导致，请重新下载此小说")
            return
        encoding = lines[3].strip()
        if len(lines) >= 5:
            save_sha256 = lines[4].strip()
            skip_hash = 0
        else:
            print(Fore.YELLOW + Style.BRIGHT + "此小说可能由老版本下载，跳过hash校验")
            save_sha256 = None
            skip_hash = 1
        hash_sha256 = hashlib.sha256()
        with open(txt_file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        fact_sha256 = hash_sha256.hexdigest()
        if skip_hash == 0:
            if fact_sha256 != save_sha256:
                print(Fore.RED + Style.BRIGHT + "hash校验未通过！")
                while True:
                    upd_choice = input(f"这往往意味着文件已被修改，是否继续更新？(yes/no):")
                    if upd_choice == "yes":
                        break
                    elif upd_choice == "no":
                        print(Fore.RED + Style.BRIGHT + "更新已取消")
                        return
                    else:
                        print("输入错误，请重新输入")
            else:
                print(Fore.GREEN + Style.BRIGHT + "hash校验通过！")
        print(f"上次更新时间{last_update_time}")
        result = download_novel(url, encoding, user_agent, last_chapter_id, txt_file_path)
        if result == "DN":
            print(f"{novel_name} 已是最新，不需要更新。\n")
        elif result == "Timeout":
            print(Fore.RED + Style.BRIGHT + "更新失败")
        elif result == "Not Found":
            print(Fore.RED + Style.BRIGHT + "更新失败")
        else:
            print(f"{novel_name} 已更新完成。\n")
            # 计算文件 sha256 值
            hash_sha256 = hashlib.sha256()
            with open(txt_file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_sha256.update(chunk)
            sha256_hash = hash_sha256.hexdigest()
            # 获取当前系统时间
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 创建要写入元信息文件的内容
            new_content = f"{current_time}\n{url}\n{result}\n{encoding}\n{sha256_hash}"
            # 打开文件并完全覆盖内容
            with open(upd_file_path, "w") as file:
                file.write(new_content)
    else:
        print(f"{txt_file} 不是通过此工具下载，无法更新")


def epub_batch_update(user_agent):
    print(Fore.YELLOW + Style.BRIGHT + "EPUB更新模式处于测试阶段，如发现问题请及时反馈。")
    # 指定小说文件夹
    novel_folder = "epub更新"

    os.makedirs(novel_folder, exist_ok=True)

    input("请在程序目录下”epub更新“文件夹内放入需更新的epub文件\n按 Enter 键继续...")

    novel_files = [file for file in os.listdir(novel_folder) if file.endswith(".epub")]

    if not novel_files:
        print("没有可更新的文件")
        return

    for epub_file in novel_files:
        print(f"正在更新: {epub_file}")
        epub_file_path = os.path.join(novel_folder, epub_file)
        # noinspection PyBroadException
        try:
            fanqie_epub_update(user_agent, epub_file_path)
        except Exception:
            # 导入打印异常信息的模块
            import traceback
            # 打印异常信息
            print(Fore.RED + Style.BRIGHT + "发生错误，请保存以下信息并联系开发者：")
            traceback.print_exc()


def fanqie_epub_update(user_agent, book_path):

    headers = {
        "User-Agent": user_agent
    }

    # 读取需要更新的epub文件
    book_o = epub.read_epub(book_path, {'ignore_ncx': True})

    # 创建epub电子书
    book = epub.EpubBook()

    # 获取book_id
    try:
        yaml_item = book_o.get_item_with_id('yaml')
        yaml_content = yaml_item.get_content().decode('utf-8')
        book_id = yaml.safe_load(yaml_content)['fqid']
    except AttributeError:
        print('当前仅支持更新2.10版本及以上下载的epub小说')
        return

    # 获取网页源码
    try:
        response = requests.get(f'https://fanqienovel.com/page/{book_id}',
                                headers=headers,
                                timeout=20,
                                proxies=p.proxies)
        html = response.text

        # 解析网页源码
        soup = BeautifulSoup(html, "html.parser")

        # 获取小说标题
        title = soup.find("h1").get_text()
        # , class_ = "info-name"
        title = p.rename(title)

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
    except Timeout:
        print(Fore.RED + Style.BRIGHT + "连接超时，请检查网络连接是否正常。")
        return
    except AttributeError:
        print(Fore.RED + Style.BRIGHT + "该小说已不存在或禁止网页阅读！（或网络连接异常）")
        return
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

    # 获取卷标
    page_directory_content = soup.find('div', class_='page-directory-content')
    nested_divs = page_directory_content.find_all('div', recursive=False)

    # intro chapter
    intro_e = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='hr')
    intro_e.content = (f'<img src="image.jpg" alt="Cover Image"/>'
                       f'<h1>{title}</h1>'
                       f'<p>{intro}</p>')
    book.add_item(intro_e)

    font_file = p.asset_path("HarmonyOS_Sans_SC_Regular.ttf")
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
        file_name="fonts/HarmonyOS_Sans_SC_Regular.ttf",  # 这将是字体文件在epub书籍中的路径和文件名
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
                # 获取章节标题
                chapter_title = chapter.find("a").get_text()

                # 获取章节网址
                chapter_url = urljoin(f'https://fanqienovel.com/page/{book_id}', chapter.find("a")["href"])

                # 获取章节 id
                chapter_id = re.search(r"/(\d+)", chapter_url).group(1)

                context = book_o.get_item_with_href(f'chapter_{volume_id}_{chapter_id_name}.xhtml')
                if context is not None:
                    # 提取文章标签中的文本
                    chapter_text = re.search(r"<body>([\s\S]*?)</body>", context.get_content().decode()).group(1)
                    chapter_text = re.sub(r'<h2.*?>.*?</h2>', '', chapter_text)
                else:
                    time.sleep(0.25)
                    # 构造 api 网址
                    api_url = (f"https://novel.snssdk.com/api/novel/book/reader/full/v1/?device_platform=android&"
                               f"parent_enterfrom=novel_channel_search.tab.&aid=2329&platform_id=1&group_id="
                               f"{chapter_id}&item_id={chapter_id}")

                    # 尝试获取章节内容
                    chapter_content = None
                    retry_count = 1
                    while retry_count < 4:  # 设置最大重试次数
                        try:
                            # 获取 api 响应
                            api_response = requests.get(api_url, headers=headers, timeout=5, proxies=p.proxies)

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
                        tqdm.write(f"无法获取章节内容: {chapter_title}，跳过。")
                        continue  # 重试次数过多后，跳过当前章节

                    # 提取文章标签中的文本
                    chapter_text = re.search(r"<article>([\s\S]*?)</article>", chapter_content).group(1)

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

    # 添加 navigation 文件
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    yaml_data = {
        'fqid': book_id
    }
    yaml_content = yaml.dump(yaml_data)

    # 设置 fqid 元数据
    yaml_item = epub.EpubItem(uid='yaml', file_name='metadata.yaml', media_type='application/octet-stream',
                              content=yaml_content)
    book.add_item(yaml_item)

    epub.write_epub(book_path, book, {})

    print("文件已保存！更新结束！")
    return
