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
from urllib.parse import urljoin
import re
import datetime
import os
import time
from tqdm import tqdm
import hashlib
import public as p
from colorama import Fore, Style, init

init(autoreset=True)


# 定义正常模式用来下载番茄小说的函数
def fanqie_n(url, encoding, user_agent, path_choice, data_folder, start_chapter_id):

    headers, title, content, chapters = p.get_fanqie(url, user_agent)

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

    elif path_choice == 0:
        # 定义文件名
        file_path = title + ".txt"

    chapter_id = None

    try:
        # 遍历每个章节链接
        for chapter in tqdm(chapters[start_index:]):
            time.sleep(0.25)

            result = p.get_api(chapter, headers, url)

            if result is None:
                continue
            else:
                chapter_title, chapter_text = result

            # 在小说内容字符串中添加章节标题和内容
            content += f"\n\n\n{chapter_title}\n{chapter_text}"

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
