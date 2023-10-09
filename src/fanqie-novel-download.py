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
该程序仅用于学习和研究Python网络爬虫和网页处理技术，不得用于任何非法活动或侵犯他人权益的行为。使用本程序所产生的一切法律责任和风险，均由用户自行承担，与作者和版权持有人无关。作者不对因使用该程序而导致的任何损失或损害承担任何责任。

请在使用本程序之前确保遵守相关法律法规和网站的使用政策，如有疑问，请咨询法律顾问。
"""

# 导入必要的模块
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re

mode = None  # 将mode定义为全局变量


# 输出用户须知
def print_usage():
    print("欢迎使用此程序！")
    print("""用户须知：
此程序开源免费，如果您付费获取，那么您已经被骗了。
本程序灵感及api来自于ibxff所作用户脚本，脚本链接请到更多中查看；
为保护此程序不被用于不良商业行为，此程序使用GPLv3开源，
请您基于此程序开发或混合后，使用GPLv3开源，感谢配合。
用户QQ群(闲聊):621748837
免责声明：
该程序仅用于学习和研究Python网络爬虫和网页处理技术，不得用于任何非法活动或侵犯他人权益的行为。
使用本程序所产生的一切法律责任和风险，均由用户自行承担，与作者和版权持有人无关。
作者不对因使用该程序而导致的任何损失或损害承担任何责任。
""")


# 请用户选择
def main():
    global mode  # 声明mode为全局变量
    print_usage()

    while True:
        print("请选择以下操作：")
        print("1. 同意并进入正常模式")
        print("2. 同意并进入Debug模式")
        print("3. 查看更多")
        print("4. 不同意，退出程序")
        choice = input("请输入您的选择（1/2/3/4）:（回车默认“1”）\n ")

        if not choice:
            choice = '1'

        if choice == '1':
            mode = 0
            break
        elif choice == '2':
            mode = 1
            print("已进入Debug模式，将会给出更多选项和调试信息\n。")
            break
        elif choice == '3':
            print("""作者：星隅（xing-yv）

版权所有（C）2023 星隅（xing-yv）

本软件根据GNU通用公共许可证第三版（GPLv3）发布；
你可以在以下位置找到该许可证的副本：
https://www.gnu.org/licenses/gpl-3.0.html

根据GPLv3的规定，您有权在遵循许可证的前提下自由使用、修改和分发本软件。
请注意，根据许可证的要求，任何对本软件的修改和分发都必须包括原始的版权声明和GPLv3的完整文本。

本软件提供的是按"原样"提供的，没有任何明示或暗示的保证，包括但不限于适销性和特定用途的适用性。作者不对任何直接或间接损害或其他责任承担任何责任。在适用法律允许的最大范围内，作者明确放弃了所有明示或暗示的担保和条件。

免责声明：
该程序仅用于学习和研究Python网络爬虫和网页处理技术，不得用于任何非法活动或侵犯他人权益的行为。使用本程序所产生的一切法律责任和风险，均由用户自行承担，与作者和版权持有人无关。作者不对因使用该程序而导致的任何损失或损害承担任何责任。

请在使用本程序之前确保遵守相关法律法规和网站的使用政策，如有疑问，请咨询法律顾问。

ibxff所作用户脚本:https://greasyfork.org/zh-CN/scripts/476688
开源仓库地址:https://github.com/xing-yv/fanqie-novel-download
作者B站主页:https://space.bilibili.com/1920711824
提出反馈:https://github.com/xing-yv/fanqie-novel-download/issues/new
(请在右侧Label处选择issue类型以得到更快回复)
""")
        elif choice == '4':
            print("退出程序。\n")
            exit()
        else:
            print("无效的选择，请重新输入。")


# 定义一个函数，用来下载小说
def download_novel(url, encoding):
    global mode  # 声明mode为全局变量
    # 定义 User-Agent
    if mode == 1:
        user_agent_choice = input("是否自行输入User-Agent？(y/n): ")
        if user_agent_choice.lower() == "y":
            user_agent = input("请输入自定义的User-Agent: \n")
            headers = {
                "User-Agent": user_agent
            }
        else:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
            }
    else:
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

    if mode == 1:
        print(f"已获取小说标题")

    # 获取小说信息
    info = soup.find("div", class_="page-header-info").get_text()

    if mode == 1:
        print(f"已获取小说信息")

    # 获取小说简介
    intro = soup.find("div", class_="page-abstract-content").get_text()

    if mode == 1:
        print(f"已获取小说简介")

    # 拼接小说内容字符串
    content = f"使用 @星隅(xing-yv) 所作开源工具下载\n开源仓库地址:https://github.com/xing-yv/fanqie-novel-download\n\n{title}\n{info}\n{intro}\n"

    if mode == 1:
        print(f"已拼接小说内容字符串")

    # 获取所有章节链接
    chapters = soup.find_all("div", class_="chapter-item")

    if mode == 1:
        print(f"已获取所有章节链接")

    # 遍历每个章节链接
    for chapter in chapters:
        # 获取章节标题
        chapter_title = chapter.find("a").get_text()

        # 获取章节网址
        chapter_url = urljoin(url, chapter.find("a")["href"])

        # 获取章节 id
        chapter_id = re.search(r"/(\d+)", chapter_url).group(1)

        if mode == 1:
            print(f"章节id:{chapter_id}")

        # 构造 api 网址
        api_url = f"https://novel.snssdk.com/api/novel/book/reader/full/v1/?device_platform=android&parent_enterfrom=novel_channel_search.tab.&aid=2329&platform_id=1&group_id={chapter_id}&item_id={chapter_id}"

        if mode == 1:
            print(f"api网址:{api_url}")

        # 获取 api 响应
        api_response = requests.get(api_url, headers=headers)

        if mode == 1:
            print(f"HTTP状态码:{api_response}")

        # 解析 api 响应为 json 数据
        api_data = api_response.json()

        # 获取章节内容
        chapter_content = api_data["data"]["content"]

        # 提取文章标签中的文本
        chapter_text = re.search(r"<article>([\s\S]*?)</article>", chapter_content).group(1)

        # 将 <p> 标签替换为换行符
        chapter_text = re.sub(r"<p>", "\n", chapter_text)

        # 去除其他 html 标签
        chapter_text = re.sub(r"</?\w+>", "", chapter_text)
        '''
        # 将 <p> 标签转换为换行符
        chapter_text = chapter_text.replace("<p>", "\n")

        # 去除 html 标签和空白字符
        chapter_text = re.sub(r"<\w+>|</\w+>|\s+", "", chapter_text)
        '''

        # 在小说内容字符串中添加章节标题和内容
        content += f"\n\n{chapter_title}\n{chapter_text}"

        # 打印进度信息
        print(f"已获取 {chapter_title}")

    # 根据编码转换小说内容字符串为二进制数据
    if encoding == "utf-8":
        data = content.encode("utf-8", errors='ignore')
    elif encoding == "gb2312":
        data = content.encode("gb2312", errors='ignore')
    else:
        print("不支持的编码")
        return

    # 定义文件名
    filename = title + ".txt"

    # 保存文件
    with open(filename, "wb") as f:
        f.write(data)

    # 打印完成信息
    print(f"已保存 {filename}")


# 程序开始
main()

while True:
    n_url = input("请输入目录页链接：\n")

    # 检查 url 是否是小说目录页面
    if "/page/" not in n_url:
        print("请输入正确的小说目录页面链接")
    else:
        break  # 如果是正确的链接，则退出循环

while True:
    n_encoding = input("请输入保存文件所使用的编码：1 -> utf-8 | 2 -> gb2312\n")

    if not n_encoding:
        n_encoding = '1'

    # 检查用户选择文件编码是否正确
    if n_encoding == '1':
        n_encoding_f = 'utf-8'
        break
    elif n_encoding == '2':
        n_encoding_f = 'gb2312'
        break
    else:
        print("输入无效，请重新输入。")

print(f"你选择的保存编码是：{n_encoding_f}")

download_novel(n_url, n_encoding_f)

input("按任意键退出...")
