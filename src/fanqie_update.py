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
import datetime
import re
import os
import public as p


# 定义番茄更新函数
def fanqie_update(user_agent, data_folder):

    # 请用户选择更新模式
    while True:
        update_mode = input("请选择更新模式:1 -> 单个更新 2-> 批量更新\n")
        if not update_mode:
            update_mode = '1'
        if update_mode == '1':
            onefile(user_agent, data_folder)
            return
        elif update_mode == '2':
            break
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
            encoding = lines[3].strip()
            print(f"上次更新时间{last_update_time}")
            result = download_novel(url, encoding, user_agent, last_chapter_id, txt_file_path)
            if result == "DN":
                print(f"{novel_name} 已是最新，不需要更新。\n")
            else:
                print(f"{novel_name} 已更新完成。\n")
                # 获取当前系统时间
                current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # 创建要写入元信息文件的内容
                new_content = f"{current_time}\n{url}\n{result}\n{encoding}"
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

    headers = {
        "User-Agent": user_agent
    }

    # 获取网页源码
    response = requests.get(url, headers=headers)
    html = response.text

    # 解析网页源码
    soup = BeautifulSoup(html, "html.parser")

    # 获取所有章节链接
    chapters = soup.find_all("div", class_="chapter-item")

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
        # 从起始章节开始遍历每个章节链接
        for chapter in chapters[start_index:]:
            # 获取章节标题
            chapter_title = chapter.find("a").get_text()

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

            chapter_text = p.fix_publisher(chapter_text)

            # 在小说内容字符串中添加章节标题和内容
            content = f"\n\n\n{chapter_title}\n{chapter_text}"

            # 根据编码转换小说内容字符串为二进制数据
            data = content.encode(encoding, errors='ignore')

            # 将数据追加到文件中
            f.write(data)

            # 打印进度信息
            print(f"已增加: {chapter_title}")

    # 返回更新完成
    return last_chapter_id


def onefile(user_agent, data_folder):

    txt_file_path = None
    while True:
        # 提示用户输入路径
        user_path = input("请将要更新的小说拖动到窗口中，然后按 Enter 键:\n")
        if '.txt' not in user_path:
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
        encoding = lines[3].strip()
        print(f"上次更新时间{last_update_time}")
        result = download_novel(url, encoding, user_agent, last_chapter_id, txt_file_path)
        if result == "DN":
            print(f"{novel_name} 已是最新，不需要更新。\n")
        else:
            print(f"{novel_name} 已更新完成。\n")
            # 获取当前系统时间
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 创建要写入元信息文件的内容
            new_content = f"{current_time}\n{url}\n{result}\n{encoding}"
            # 打开文件并完全覆盖内容
            with open(upd_file_path, "w") as file:
                file.write(new_content)
    else:
        print(f"{txt_file} 不是通过此工具下载，无法更新")
