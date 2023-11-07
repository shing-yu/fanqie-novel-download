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

# 导入必要的模块
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import os
import time
import public as p


# 定义分章节保存模式用来下载番茄小说的函数
def fanqie_c(url, encoding, user_agent, path_choice, start_chapter_id):

    headers = {
        "User-Agent": user_agent
    }

    # 获取网页源码
    response = requests.get(url, headers=headers)
    html = response.text

    # 解析网页源码
    soup = BeautifulSoup(html, "html.parser")

    # 获取小说标题
    title = soup.find("h1").get_text()
    # , class_ = "info-name"

    # 替换非法字符
    title = p.rename(title)

    # 获取保存路径
    book_folder = get_folder_path(path_choice, title)
    # 创建保存文件夹
    os.makedirs(book_folder, exist_ok=True)
    # 获取小说信息
    info = soup.find("div", class_="page-header-info").get_text()

    # 获取小说简介
    intro = soup.find("div", class_="page-abstract-content").get_text()

    # 拼接小说内容字符串
    introduction = f"""使用 @星隅(xing-yv) 所作开源工具下载
开源仓库地址:https://github.com/xing-yv/fanqie-novel-download
Gitee:https://gitee.com/xingyv1024/fanqie-novel-download/
任何人无权限制您访问本工具，如果有向您提供代下载服务者未事先告知您工具的获取方式，请向作者举报:xing_yv@outlook.com

{title}
{info}
{intro}
"""
    # 转换简介内容格式
    introduction_data = introduction.encode(encoding, errors='ignore')

    # 获取所有章节链接
    chapters = soup.find_all("div", class_="chapter-item")

    # 定义简介路径
    introduction_use = False
    introduction_path = None

    # 检查用户是否指定起始章节
    start_index = 0
    if start_chapter_id == '0':
        pass
    else:
        # 找到起始章节的索引
        for i, chapter in enumerate(chapters):
            chapter_url_tmp = urljoin(url, chapter.find("a")["href"])
            chapter_id_tmp = re.search(r"/(\d+)", chapter_url_tmp).group(1)
            if chapter_id_tmp == start_chapter_id:  # 将 开始索引设置为用户的值
                start_index = i

    # 遍历每个章节链接
    for chapter in chapters[start_index:]:

        time.sleep(0.25)
        # 获取章节标题
        chapter_title = chapter.find("a").get_text()

        # 替换非法字符
        chapter_title = p.rename(chapter_title)

        # 获取章节网址
        chapter_url = urljoin(url, chapter.find("a")["href"])

        # 获取章节 id
        chapter_id = re.search(r"/(\d+)", chapter_url).group(1)

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
                api_response = requests.get(api_url, headers=headers)

                # 解析 api 响应为 json 数据
                api_data = api_response.json()
            except Exception as e:
                if retry_count == 1:
                    print(f"错误：{e}")
                    print(f"{chapter_title} 获取失败，正在尝试重试...")
                print(f"第 ({retry_count}/3) 次重试获取章节内容")
                retry_count += 1  # 否则重试
                continue

            if "data" in api_data and "content" in api_data["data"]:
                chapter_content = api_data["data"]["content"]
                break  # 如果成功获取章节内容，跳出重试循环
            else:
                if retry_count == 1:
                    print(f"{chapter_title} 获取失败，正在尝试重试...")
                print(f"第 ({retry_count}/3) 次重试获取章节内容")
                retry_count += 1  # 否则重试

        if retry_count == 4:
            print(f"无法获取章节内容: {chapter_title}，跳过。")
            continue  # 重试次数过多后，跳过当前章节

        # 提取文章标签中的文本
        chapter_text = re.search(r"<article>([\s\S]*?)</article>", chapter_content).group(1)

        # 将 <p> 标签替换为换行符
        chapter_text = re.sub(r"<p>", "\n", chapter_text)

        # 去除其他 html 标签
        chapter_text = re.sub(r"</?\w+>", "", chapter_text)

        # 针对性去除所有 出版物 所携带的标签
        chapter_text = p.fix_publisher(chapter_text)

        # 在章节内容字符串中添加章节标题和内容
        content_all = f"{chapter_title}\n{chapter_text}"

        # 转换章节内容格式
        data = content_all.encode(encoding, errors='ignore')

        # 重置file_path
        # noinspection PyUnusedLocal
        file_path = None

        # 生成最终文件路径

        # 使用用户选择的文件夹路径和默认文件名来生成完整的文件路径

        file_path = os.path.join(book_folder, f"{chapter_title}.txt")
        if introduction_use is False:
            introduction_path = os.path.join(book_folder, "简介.txt")

        if introduction_use is False:
            with open(introduction_path, "wb") as f:
                f.write(introduction_data)
            print("简介已保存")
            # 将简介保存标记为已完成
            introduction_use = True

        with open(file_path, "wb") as f:
            f.write(data)

        # 打印进度信息
        print(f"已获取: {chapter_title}")


def get_folder_path(path_choice, title):
    folder_path = None
    # 如果用户选择自定义路径
    if path_choice == 1:
        import tkinter as tk
        from tkinter import filedialog
        # 创建一个Tkinter窗口，但不显示它
        root = tk.Tk()
        root.withdraw()

        print("您选择了自定义保存路径，请您在弹出窗口中选择保存文件夹。")

        while True:

            # 弹出文件对话框以选择保存位置和文件名
            folder_path = filedialog.askdirectory()

            # 检查用户是否取消了对话框
            if not folder_path:
                # 用户取消了对话框，提示重新选择
                print("您没有选择保存文件夹，请重新选择！")
                continue
            else:
                print("已选择保存文件夹")
                break
    elif path_choice == 0:

        # 在程序文件夹下新建output文件夹，并定义文件路径

        folder_path = "output"

        os.makedirs(folder_path, exist_ok=True)
    return os.path.join(folder_path, f"{title}")
