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
import multiprocessing
import queue
import threading
import tkinter as tk
import tkinter.messagebox
from multiprocessing import Process, Queue
import time
import fanqie_list as fl


class Spider:
    def __init__(self, output_func, output_queue):
        self.url_queue = queue.Queue()
        self.output_queue = output_queue
        self.is_running = True
        self.output_func = output_func

    @staticmethod
    def crawl(url, output_queue):
        # 创建一个新的进程来运行爬虫函数
        p = Process(target=fl.fanqie_l, args=(url, 'utf-8', output_queue))
        p.start()
        time.sleep(2)

    def worker(self):
        while self.is_running:
            try:
                url = self.url_queue.get(timeout=1)
                Spider.crawl(url, self.output_queue)
                self.url_queue.task_done()
            except queue.Empty:
                continue

    def start(self):
        threading.Thread(target=self.worker, daemon=True).start()

    def add_url(self, url):
        if "/page/" not in url:
            tkinter.messagebox.showinfo("错误", "URL格式不正确，请重新输入")
            return
        else:
            self.url_queue.put(url)
            tkinter.messagebox.showinfo("成功", "URL已添加到下载队列")

    def stop(self):
        self.is_running = False


def main():
    root = tk.Tk()
    root.title("番茄工具队列版")

    # 设置窗口大小
    root.geometry("600x400")

    # 禁止窗口缩放
    root.resizable(False, False)

    output_text = tk.Text(root, state='disabled')
    output_text.pack()

    # 创建滚动条
    scrollbar = tk.Scrollbar(root, command=output_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 设置Text组件的yscrollcommand为滚动条的set方法
    output_text.config(yscrollcommand=scrollbar.set)

    # 手动调整滚动条的位置
    scrollbar.place(x=580, y=0, height=320)

    input_frame = tk.Frame(root)
    input_frame.pack()
    input_entry = tk.Entry(input_frame, width=50)
    input_entry.pack(side=tk.LEFT)

    # 调整输入框的位置
    input_frame.place(x=50, y=350)

    def paste_text():
        input_entry.event_generate('<<Paste>>')

    def show_context_menu(event):
        context_menu.post(event.x_root, event.y_root)

    # 创建上下文菜单
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="粘贴", command=paste_text)

    # 绑定上下文菜单到输入框
    input_entry.bind("<Button-3>", show_context_menu)

    input_entry.bind("<Button-3>", show_context_menu)

    output_queue = Queue()

    spider = Spider(
        lambda text: (
                output_text.config(state='normal') or
                output_text.insert(tk.END, text + "\n") or
                output_text.config(state='disabled')
        ),
        output_queue
    )
    spider.start()

    def add_url():
        url = input_entry.get()
        spider.add_url(url)
        input_entry.delete(0, tk.END)

    add_button = tk.Button(input_frame, text="添加URL", command=add_url)
    add_button.pack(side=tk.LEFT)

    def list_urls():
        urls = list(spider.url_queue.queue)
        tkinter.messagebox.showinfo("队列中的URL", "\n".join(urls))

    list_button = tk.Button(input_frame, text="列出URL", command=list_urls)
    list_button.pack(side=tk.LEFT)

    def stop_spider():
        spider.stop()
        root.quit()

    stop_button = tk.Button(input_frame, text="退出", command=stop_spider)
    stop_button.pack(side=tk.LEFT)

    def check_output_queue():
        while not output_queue.empty():
            message = output_queue.get()
            output_text.config(state='normal')
            output_text.insert(tk.END, message + "\n")
            output_text.config(state='disabled')

            # 滚动到最后一行
            output_text.see(tk.END)

        root.after(100, check_output_queue)  # 每秒检查一次输出队列

    check_output_queue()

    root.mainloop()


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
