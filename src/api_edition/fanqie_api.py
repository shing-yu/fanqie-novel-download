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
该程序仅用于学习和研究Python网络爬虫和网页处理技术，不得用于任何非法活动或侵犯他人权益的行为。使用本程序所产生的一切法律责任和风险，均由用户自行承担，与作者和项目贡献者无关。作者不对因使用该程序而导致的任何损失或损害承担任何责任。

请在使用本程序之前确保遵守相关法律法规和网站的使用政策，如有疑问，请咨询法律顾问。

无论您对程序进行了任何操作，请始终保留此信息。
"""
import os

# 导入必要的模块
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
from os import path
import time
import public as p


# 定义正常模式用来下载番茄小说的函数
def fanqie_l(url, encoding):

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
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

    # 定义文件名
    file_path = path.join('output', f'{title}.txt')

    os.makedirs("output", exist_ok=True)

    try:
        # 遍历每个章节链接
        for chapter in chapters:
            time.sleep(1)
            # 获取章节标题
            chapter_title = chapter.find("a").get_text()

            # 获取章节网址
            chapter_url = urljoin(url, chapter.find("a")["href"])

            # 获取章节 id
            chapter_id = re.search(r"/(\d+)", chapter_url).group(1)

            # 构造 api 网址
            api_url = f"https://novel.snssdk.com/api/novel/book/reader/full/v1/?device_platform=android&parent_enterfrom=novel_channel_search.tab.&aid=2329&platform_id=1&group_id={chapter_id}&item_id={chapter_id}"

            # 尝试获取章节内容
            chapter_content = None
            retry_count = 1
            while retry_count < 4:  # 设置最大重试次数
                # 获取 api 响应
                api_response = requests.get(api_url, headers=headers)

                # 解析 api 响应为 json 数据
                api_data = api_response.json()

                if "data" in api_data and "content" in api_data["data"]:
                    chapter_content = api_data["data"]["content"]
                    break  # 如果成功获取章节内容，跳出重试循环
                else:
                    retry_count += 1  # 否则重试

            if retry_count == 4:
                continue  # 重试次数过多后，跳过当前章节

            # 提取文章标签中的文本
            chapter_text = re.search(r"<article>([\s\S]*?)</article>", chapter_content).group(1)

            # 将 <p> 标签替换为换行符
            chapter_text = re.sub(r"<p>", "\n", chapter_text)

            # 去除其他 html 标签
            chapter_text = re.sub(r"</?\w+>", "", chapter_text)

            chapter_text = p.fix_publisher(chapter_text)

            # 在小说内容字符串中添加章节标题和内容
            content += f"\n\n\n{chapter_title}\n{chapter_text}"

        # 根据编码转换小说内容字符串为二进制数据
        data = content.encode(encoding, errors='ignore')

        # 保存文件
        with open(file_path, "wb") as f:
            f.write(data)

    except BaseException as e:
        # 捕获所有异常，及时保存文件
        # 根据转换小说内容字符串为二进制数据
        data = content.encode(encoding, errors='ignore')

        # 保存文件
        with open(file_path, "wb") as f:
            f.write(data)
        raise Exception(f"下载失败: {e}")
