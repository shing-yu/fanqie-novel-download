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

import multiprocessing
import queue
import threading
from multiprocessing import Process
import time
import fanqie_api as fa
from flask import Flask, request, jsonify

app = Flask(__name__)


# 定义爬虫类
class Spider:
    def __init__(self):
        # 初始化URL队列
        self.url_queue = queue.Queue()
        # 设置运行状态为True
        self.is_running = True
        # 初始化任务状态字典
        self.task_status = {}

    @staticmethod
    def crawl(url):
        try:
            # 创建一个新的进程来运行爬虫函数
            p = Process(target=fa.fanqie_l, args=(url, 'utf-8'))
            p.start()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False

    def worker(self):
        # 当运行状态为True时，持续工作
        while self.is_running:
            try:
                # 从URL队列中获取URL
                url = self.url_queue.get(timeout=1)
                # 调用爬虫函数爬取URL，如果出错则标记为失败并跳过这个任务进行下一个
                if Spider.crawl(url):
                    self.task_status[url] = "已完成"
                else:
                    self.task_status[url] = "失败"
                # 完成任务后，标记任务为完成状态
                self.url_queue.task_done()
            except queue.Empty:
                time.sleep(5)
                continue

    def start(self):
        # 启动工作线程
        threading.Thread(target=self.worker, daemon=True).start()

    def add_url(self, url):
        # 检查URL格式是否正确，如果不正确则返回错误信息，否则将URL添加到队列中并返回成功信息
        if "/page/" not in url:
            return "URL格式不正确，请重新输入"
        else:
            if url not in self.task_status or self.task_status[url] == "失败":
                self.url_queue.put(url)
                self.task_status[url] = "等待中"
                return "URL已添加到下载队列"
            else:
                return "URL已存在"

    def stop(self):
        # 设置运行状态为False以停止工作线程
        self.is_running = False


# 创建爬虫实例并启动
spider = Spider()
spider.start()


@app.route('/api', methods=['POST'])
def api():
    # 获取请求数据
    data = request.get_json()
    # 检查请求数据是否包含'class'和'id'字段，如果没有则返回400错误
    if 'class' not in data or 'id' not in data:
        return jsonify({'error': 'Bad Request'}), 400

    # 如果'class'字段的值为'add'，则尝试将URL添加到队列中，并返回相应的信息和位置
    if data['class'] == 'add':
        url = 'https://fanqienovel.com/page/' + data['id']
        message = spider.add_url(url)
        position = list(spider.url_queue.queue).index(url) + 1 if url in list(spider.url_queue.queue) else None
        status = spider.task_status.get(url, None)
        return jsonify({'message': message, 'position': position, 'status': status})

    # 如果'class'字段的值为'search'，则检查URL是否在队列中，并返回相应的信息和位置或不存在的信息
    elif data['class'] == 'search':
        url = 'https://fanqienovel.com/page/' + data['id']
        position = list(spider.url_queue.queue).index(url) + 1 if url in list(spider.url_queue.queue) else None
        status = spider.task_status.get(url, None)
        return jsonify({'exists': status is not None, 'position': position, 'status': status})

    else:
        return jsonify({'error': 'Bad Request'}), 400


if __name__ == "__main__":
    multiprocessing.freeze_support()
    app.run(port=5000)
