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


import fanqie_normal as fn
import fanqie_debug as fd
import fanqie_batch as fb
import fanqie_chapter as fc
import fanqie_update as fu
import fanqie_epub as fe
import os
import re
import requests
import platform
from sys import exit
from packaging import version

# 定义全局变量
mode = None
page_url = None
txt_encoding = None
ua = None
type_path_num = None
return_info = None
user_folder = os.path.expanduser("~")
data_path = os.path.join(user_folder, "fanqie_data")
os.makedirs(data_path, exist_ok=True)
book_id = None
start_chapter_id = "0"


# 用户须知
def print_usage():
    print("欢迎使用此程序！")
    print("""用户须知：
此程序开源免费，如果您付费获取，那么您已经被骗了。
本程序灵感及api来自于ibxff所作用户脚本，脚本链接请到更多中查看；
为保护此程序不被用于不良商业行为，此程序使用GPLv3许可证，

您可以自由地复制、修改和分发本程序副本，但不能销售它。
您可以使用此程序提供有偿代下载服务，但在提供服务的同时，必须向服务的接收者提供此程序的获取方式，
以便他们可以自由使用、修改和分发该软件，同时也必须遵守GPLv3协议的所有其他规定。

用户QQ2群(闲聊):947392854
如果想要指定开始下载的章节，请在输入目录页链接时按Ctrl+C。

免责声明：
该程序仅用于学习和研究Python网络爬虫和网页处理技术，不得用于任何非法活动或侵犯他人权益的行为。
使用本程序所产生的一切法律责任和风险，均由用户自行承担，与作者和项目协作者、贡献者无关。
作者不对因使用该程序而导致的任何损失或损害承担任何责任。
""")


# 请用户同意协议并选择模式
def start():
    global mode  # 声明mode为全局变量
    global return_info

    # 定义变量flag控制是否退出程序
    flag = True
    while True:
        print_usage()
        print("请选择以下操作：")
        print("1. 同意并进入正常模式")
        print("2. 同意并进入自动批量模式")
        print("3. 同意并进入分章保存模式(测试)")
        print("4. 同意并进入Debug模式")
        print("5. 同意并进入Epub电子书模式(测试)")
        print("6. 查看更多")
        print("7. 更新已下载的小说")
        print("8. 查看贡献（赞助）者名单")
        print("9. 不同意，退出程序")
        choice = input("请输入您的选择（1/2/3/4/5/6/7/8/9）:（默认“1”）\n")

        # 通过用户选择，决定模式，给mode赋值
        if not choice:
            choice = '1'

        if choice == '1':
            mode = 0
            clear_screen()
            print("您已进入正常下载模式：")
            break
        elif choice == '2':
            mode = 2
            clear_screen()
            print("您已进入自动批量下载模式:")
            break
        elif choice == '3':
            mode = 3
            clear_screen()
            print("您已进入分章保存模式(测试):")
            break
        elif choice == '4':
            mode = 1
            clear_screen()
            print("您已进入Debug模式，将会给出更多选项和调试信息。\n")
            break
        elif choice == '5':
            mode = 4
            clear_screen()
            print("您已进入Epub模式，将保留一定的小说格式。\n")
            break
        elif choice == '6':
            clear_screen()
            print("""作者：星隅（xing-yv）
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

ibxff所作用户脚本:https://greasyfork.org/zh-CN/scripts/476688
开源仓库地址:https://github.com/xing-yv/fanqie-novel-download
gitee地址:https://gitee.com/xingyv1024/fanqie-novel-download
作者B站主页:https://space.bilibili.com/1920711824
提出反馈:https://github.com/xing-yv/fanqie-novel-download/issues/new
(请在右侧Label处选择issue类型以得到更快回复)
""")
            input("按Enter键返回...")
            clear_screen()
        elif choice == '7':
            clear_screen()
            print("您已进入更新模式")
            # 调用番茄更新函数
            return_info = fu.fanqie_update(ua, data_path)
            return
        elif choice == '8':
            clear_screen()
            contributors_url = 'https://gitee.com/xingyv1024/fanqie-novel-download/raw/main/CONTRIBUTORS.md'
            try:
                contributors = requests.get(contributors_url)

                # 检查响应状态码
                if contributors.status_code == 200:
                    contributor_md_content = contributors.text
                    print(contributor_md_content)
                else:
                    print(f"获取贡献名单失败，HTTP响应代码: {contributors.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"发生错误: {e}")
            input("按Enter键返回...")
            clear_screen()
        elif choice == '9':
            clear_screen()
            # 确认退出
            while True:
                qd = input("您确定要退出程序吗(yes/no)(默认:no): ")
                if not qd:
                    qd = "no"
                if qd.lower() == "yes":
                    input("按Enter退出程序...")
                    break
                elif qd.lower() == "no":
                    flag = False
                    break
                else:
                    print("输入无效，请重新输入。")
            if flag is True:
                exit(0)
            else:
                clear_screen()
                continue
        else:
            print("无效的选择，请重新输入。")
    get_parameter(retry=False)


def get_parameter(retry):
    global page_url
    global txt_encoding
    global ua
    global type_path_num
    global book_id
    global start_chapter_id

    page_url = None

    # 判断是否是批量下载模式
    if mode == 2:
        if not os.path.exists('urls.txt'):
            with open('urls.txt', 'x') as _:
                pass
        if retry is True:
            print("您在urls.txt中输入的内容有误，请重新输入")
            print("请重新在程序同文件夹(或执行目录)下的urls.txt中，以每行一个的形式写入目录页链接")
        elif retry is False:
            print("请在程序同文件夹(或执行目录)下的urls.txt中，以每行一个的形式写入目录页链接")
        input("完成后请按Enter键继续:")
    else:
        # 不是则让用户输入小说目录页的链接
        while True:
            try:
                page_url = input("请输入目录页链接：\n")

                # 预留七猫小说判断
                # if "qimao" in page_url:
                #   if mode == 0:
                #      mode = 2
                #   elif mode == 1:
                #      mode = 3
                # elif "fanqie" in page_url:

                # 检查 url 是否是小说目录页面
                if "/page/" not in page_url:
                    print("请输入正确的小说目录页面链接")
                else:
                    book_id = re.search(r"/(\d+)", page_url).group(1)
                    break  # 如果是正确的链接，则退出循环
            # 当用户按下Ctrl+C是，可以自定义起始章节id
            except KeyboardInterrupt:
                while True:
                    start_chapter_id = input("您已按下Ctrl+C，请输入起始章节的id\n(输入help以查看帮助，"
                                             "epub电子书模式不支持起始章节，再次按下Ctrl+C以强制关闭程序):\n")
                    if start_chapter_id == 'help':
                        print("\n打开小说章节阅读界面，上方链接中的数字即为章节id\n请输入您想要开始下载的章节的id\n")
                        continue
                    elif start_chapter_id.isdigit():
                        break
                    else:
                        print("无效的输入，请重新输入")

    # 让用户选择保存文件的编码
    while True:
        if mode == 4:
            break
        txt_encoding_num = input("请输入保存文件所使用的编码(默认:1)：1 -> utf-8 | 2 -> gb2312\n")

        if not txt_encoding_num:
            txt_encoding_num = '1'

        # 检查用户选择文件编码是否正确
        if txt_encoding_num == '1':
            txt_encoding = 'utf-8'
            break
        elif txt_encoding_num == '2':
            txt_encoding = 'gb2312'
            break
        else:
            print("输入无效，请重新输入。")

    if mode != 4:
        print(f"你选择的保存编码是：{txt_encoding}")

    # 初始化“ua”
    ua = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/118.0.0.0 "
        "Safari/537.36"
    )

    # 定义 User-Agent
    if mode == 1:  # 判断用户是否处于调试模式
        while True:
            ua_choice = input("是否自行输入User-Agent？(yes/no)(默认:no): ")
            if not ua_choice:
                ua_choice = "no"
            # 是则询问是否自定义ua
            if ua_choice.lower() == "yes":
                ua = input("请输入自定义的User-Agent: \n")
                break
            elif ua_choice.lower() == "no":
                break
            else:
                print("输入无效，请重新输入。")
                continue

    type_path_num = None

    # 询问用户是否自定义保存路径
    while True:

        type_path = input("是否自行选择保存路径(yes/no)(默认:no):")

        if not type_path:
            type_path = "no"

        if type_path.lower() == "yes":
            type_path_num = 1
            if mode == 2:
                print("您选择了自定义保存文件夹，请在文件检查后选择保存文件夹。")
            else:
                print("您选择了自定义保存路径，请在获取完成后选择保存路径。")
            break

        elif type_path.lower() == "no":
            type_path_num = 0
            if mode == 2 or mode == 3:
                print("您未选择自定义保存路径，请在获取完成后到程序文件夹下output文件夹寻找文件。")
                print("(如果您在命令行中执行程序，请到执行目录下寻找output文件夹)")
            else:
                print("您未选择自定义保存路径，请在获取完成后到程序相同文件夹下寻找文件。")
                print("(如果您在命令行中执行程序，请到执行目录下寻找文件)")
            break

        else:
            print("输入无效，请重新输入。")
            continue
    perform_user_mode_action()


def perform_user_mode_action():
    global return_info
    # 判断用户处于什么模式
    if mode == 0:
        # 调用番茄正常模式函数
        return_info = fn.fanqie_n(page_url, txt_encoding, ua, type_path_num, data_path, start_chapter_id)
    elif mode == 1:
        # 调用番茄调试模式函数
        return_info = fd.fanqie_d(page_url, txt_encoding, ua, type_path_num, data_path, start_chapter_id)
    elif mode == 2:
        # 调用番茄批量模式函数
        return_info = fb.fanqie_b(txt_encoding, ua, type_path_num, data_path)
    elif mode == 3:
        # 调用番茄分章模式函数
        return_info = fc.fanqie_c(page_url, txt_encoding, ua, type_path_num, start_chapter_id)
    elif mode == 4:
        # 调用番茄epub电子书模式函数
        return_info = fe.fanqie_epub(page_url, ua, type_path_num)


# 检查更新
def check_update(now_version):
    owner = "xingyv1024"
    repo = "fanqie-novel-download"
    api_url = f"https://gitee.com/api/v5/repos/{owner}/{repo}/releases/latest"

    print("正在检查更新...")
    print(f"当前版本: v{now_version}")

    # noinspection PyBroadException
    try:
        # 发送GET请求以获取最新的发行版信息
        response = requests.get(api_url)

        if response.status_code != 200:
            print(f"请求失败，状态码：{response.status_code}")
            input("按Enter键继续...\n")
            return 0
        release_info = response.json()
        if "tag_name" in release_info:
            latest_version = release_info["tag_name"]
            release_describe = release_info["body"]
            print(f"最新的发行版是：v{latest_version}")
            result = compare_versions(now_version, latest_version)
            if result == -1:
                print("检测到新版本\n更新可用！请到 https://gitee.com/xingyv1024/fanqie-novel-download/releases 下载最新版")
                print(f"更新内容:\n{release_describe}")
                input("按Enter键继续...\n")
            else:
                print("您正在使用最新版")

        else:
            print("未获取到发行版信息。")
            input("按Enter键继续...\n")

    except BaseException:
        print(":(  检查更新失败...")
        input("按Enter键继续...\n")


def compare_versions(version1, version2):

    # 使用packaging模块进行版本比较
    v1 = version.parse(version1)
    v2 = version.parse(version2)

    if v1 < v2:
        return -1
    elif v1 > v2:
        return 1
    else:
        return 0


def clear_screen():
    # 根据系统类型执行不同的清屏指令
    os.system('cls') if platform.system() == 'Windows' else os.system('clear')
