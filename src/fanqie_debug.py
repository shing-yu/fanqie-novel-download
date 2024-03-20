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

import re
import datetime
import os
import time
import json
import base64
from tqdm import tqdm
import hashlib
import public as p
from requests.exceptions import Timeout
from colorama import Fore, Style, init

init(autoreset=True)


# 定义调试模式用来下载番茄小说的函数
def fanqie_d(url, encoding, path_choice, data_folder, start_chapter_id,
             config_path):

    # 询问是否自定义ua
    choice = input("是否使用自定义UA(y/n)？")
    if choice == "y":
        # 获取自定义UA
        ua = input("请输入自定义UA：")
        headers = {
            "User-Agent": ua
        }
    else:
        # 使用默认UA
        headers = p.headers

    proxies = {
        "http": None,
        "https": None
    }

    # 获取网页源码
    try:
        response = requests.get(url, timeout=20, proxies=proxies)
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

    print(Fore.YELLOW + Style.BRIGHT + f"[DEBUG]已获取小说标题")

    # 替换非法字符
    title = p.rename(title)

    print(Fore.YELLOW + Style.BRIGHT + f"[DEBUG]已尝试替换非法字符")

    # 获取小说信息
    info = soup.find("div", class_="page-header-info").get_text()

    # if mode == 1:
    print(Fore.YELLOW + Style.BRIGHT + f"[DEBUG]已获取小说信息")

    # 获取小说简介
    intro = soup.find("div", class_="page-abstract-content").get_text()

    # if mode == 1:
    print(Fore.YELLOW + Style.BRIGHT + f"[DEBUG]已获取小说简介")

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

    # if mode == 1:
    print(Fore.YELLOW + Style.BRIGHT + f"[DEBUG]已拼接小说简介字符串")

    # 获取所有章节链接
    chapters = soup.find_all("div", class_="chapter-item")

    # if mode == 1:
    print(Fore.YELLOW + Style.BRIGHT + f"[DEBUG]已获取所有章节链接")

    # 检查用户是否指定起始章节
    start_index = 0
    if start_chapter_id == '0':
        pass
    else:
        # 找到起始章节的索引
        for i, chapter in enumerate(chapters):
            chapter_url_tmp = chapter.find("a")["href"]
            chapter_id_tmp = re.search(r"/reader/(\d+)", chapter_url_tmp).group(1)
            if chapter_id_tmp == start_chapter_id:  # 将 开始索引设置为用户的值
                start_index = i

    file_path = None

    # 根据main.py中用户选择的路径方式，选择自定义路径或者默认
    if path_choice == 1:
        import tkinter as tk
        from tkinter import filedialog
        # 创建一个Tkinter窗口，但不显示它
        root = tk.Tk()
        root.withdraw()
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]已创建tkinter隐形窗口")

        print("您选择了自定义保存路径，请您在弹出窗口中选择路径。")

        # 设置默认文件名和扩展名
        default_extension = ".txt"
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
                    json.dump({"path": {"debug": folder_path}}, c)
            else:
                with open(config_path, "r") as c:
                    config = json.load(c)
                config["path"]["debug"] = folder_path
                with open(config_path, "w") as c:
                    json.dump(config, c)

    elif path_choice == 0:
        # 定义文件名，检测是否有默认路径
        if not os.path.exists(config_path):
            file_path = title + ".txt"
        else:
            with open(config_path, "r") as c:
                config = json.load(c)
            if "debug" in config["path"]:
                file_path = os.path.join(config["path"]["debug"], f"{title}.txt")
            else:
                file_path = title + ".txt"

    chapter_id = None

    length = len(chapters)
    encryption_index = length // 2

    try:
        # 遍历每个章节链接
        for i, chapter in enumerate(tqdm(chapters[start_index:], desc="下载进度")):

            time.sleep(0.25)
            # 获取章节标题
            chapter_title = chapter.find("a").get_text()
            tqdm.write(Fore.YELLOW + Style.BRIGHT + f"[DEBUG]正在获取章节:{chapter_title}")

            # 获取章节网址
            chapter_url = chapter.find("a")["href"]

            # 获取章节 id
            chapter_id = re.search(r"/reader/(\d+)", chapter_url).group(1)

            tqdm.write(Fore.YELLOW + Style.BRIGHT + f"[DEBUG]章节id:{chapter_id}")

            # 构造 api 网址
            api_url = (f"https://novel.snssdk.com/api/novel/book/reader/full/v1/?device_platform=android&"
                       f"version_code=973&app_name=news_article&version_name=9.7.3&app_version=9.7.3&device_id=1&"
                       f"channel=google&device_type=1&os_api=33&os_version=13&item_id={chapter_id}&aid=1319")
            tqdm.write(Fore.YELLOW + Style.BRIGHT + f"[DEBUG]api网址:{api_url}")

            # 尝试获取章节内容
            chapter_content = None
            while True:
                retry_count = 1
                skip = False
                terminate = False
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
                    button1 = tk.Button(button1_frame, text="跳过此章节 (1)", command=lambda: on_button_click("1"),
                                        font=font1)
                    button1.pack(pady=5)

                    button2_frame = tk.Frame(window)
                    button2_frame.pack()
                    button2 = tk.Button(button2_frame, text="再次重试 (2)", command=lambda: on_button_click("2"),
                                        font=font1)
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
                        skip = True
                    elif choice == "2":
                        continue
                    elif choice == "3":
                        terminate = True
                    break
                else:
                    break

            if skip:
                continue
            if terminate:
                break

            # 提取文章标签中的文本
            chapter_text = re.search(r"<article>([\s\S]*?)</article>", chapter_content).group(1)

            # 将 <p> 标签替换为换行符
            chapter_text = re.sub(r"<p\b[^>]*>", "\n", chapter_text)

            # 去除其他 html 标签
            chapter_text = re.sub(r"<[\x00-\x7F]*?>", "", chapter_text)

            # 针对性去除所有 出版物 所携带的标签
            chapter_text = p.fix_publisher(chapter_text)

            # 在小说内容字符串中添加章节标题和内容
            content += f"\n\n\n{chapter_title}\n{chapter_text}"

            if i == encryption_index:
                content += base64.b64decode("CgoK5pys5bCP6K+06YCa6L+H5YWN6LS55byA5rqQ"
                                            "5LiL6L295bel5YW3IGh0dHBzOi8vc291cmwuY24vZHZGS0VSIOS4i+i9veOAguWmguaenOaCqO"
                                            "mBh+WIsOaUtui0ue+8jOivt+S4vuaKpeW5tuiBlOezu+S9nOiAhQoK").decode()

            # 打印进度信息
            tqdm.write(f"已获取 {chapter_title}")

        # 根据编码转换小说内容字符串为二进制数据
        data = content.encode(encoding, errors='ignore')

        # 保存文件
        with open(file_path, "wb") as f:
            f.write(data)

        # 打印完成信息
        print(f"已保存{title}.txt")

        # 计算文件 sha256 值
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        sha256_hash = hash_sha256.hexdigest()

        # 保存小说更新源文件
        upd_file_path = os.path.join(data_folder, f"{title}.upd")
        # 获取当前系统时间
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 创建要写入元信息文件的内容
        meta_content = f"{current_time}\n{url}\n{chapter_id}\n{encoding}\n{sha256_hash}"
        # 打开文件并完全覆盖内容
        with open(upd_file_path, "w") as file:
            file.write(meta_content)
        print(Fore.YELLOW + Style.BRIGHT + "[DEBUG]已保存.upd更新元数据文件到用户文件夹")
        print("已完成")

    except BaseException as e:
        # 捕获所有异常，及时保存文件
        print(Fore.RED + Style.BRIGHT + f"发生异常: \n{e}")
        print("正在尝试保存文件...")
        # 根据编码转换小说内容字符串为二进制数据
        data = content.encode(encoding, errors='ignore')

        # 保存文件
        with open(file_path, "wb") as f:
            f.write(data)

        print("文件已保存！")
        return
