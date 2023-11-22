# fanqie-novel-download
番茄小说下载的Python实现。这是一个用于从番茄小说网站下载小说的Python程序。  
它提供了一个简单的命令行界面，可以输入小说目录页面的URL并选择保存下载内容的编码格式。  
**如果需要下载七猫小说。可以使用此项目的变体项目 [7mao-novel-downloader](https://github.com/xing-yv/7mao-novel-downloader)。**  
本程序灵感即api均来源于ibxff所作用户脚本（MIT），你可以在[此处](https://greasyfork.org/zh-CN/scripts/476688-%E7%95%AA%E8%8C%84%E5%85%A8%E6%96%87%E5%9C%A8%E7%BA%BF%E5%85%8D%E8%B4%B9%E8%AF%BB)获取。  
软件QQ2群（闲聊）：947392854  
感谢贡献（赞助）者们对本项目的支持，你可以在[此处](https://github.com/xing-yv/fanqie-novel-download/blob/main/CONTRIBUTORS.md)获取贡献和赞助者名单。

## 特点

- 从番茄网站下载小说。
- 允许用户在保存文件时选择UTF-8和GB2312编码之间的编码格式。
- 用户友好的命令行界面，具有提示和选项。
- 支持保存txt、epub两种格式

## 使用方法

1. 到[Releases](https://github.com/xing-yv/fanqie-novel-download/releases)界面下载最新版本可执行程序
2. 将程序放到合适的目录，双击运行
3. 按照提示选择模式并同意条款和条件。
4. 在提示时输入小说目录页面的URL。
5. 在提示时选择保存文件时的编码格式（UTF-8或GB2312）。
6. 选择是否自定义保存路径
7. 程序将下载小说章节并将它们保存到以小说标题命名的文本文件中。
8. 下载完成后，您可以在选择的目录中找的小说文件。

## 贡献

我们非常欢迎并感谢所有的贡献者。如果你对这个项目有兴趣并希望做出贡献，以下是一些你可以参与的方式：

### 报告问题

如果你在使用过程中发现了问题，或者有任何改进的建议，欢迎通过 [Issues](https://github.com/xing-yv/fanqie-novel-download/issues) 页面提交问题或建议。

### 提交代码

如果你想直接改进代码，可以 [Fork 本项目](https://github.com/xing-yv/fanqie-novel-download/fork)，然后提交 Pull Request。

在提交 Pull Request 之前：

- 请确保您的代码符合Python的[PEP8](https://www.python.org/dev/peps/pep-0008/)规范。
- 请确保您的代码在所有操作系统上都能正常运行。
- 如果您想在本项目中添加新功能，请先创建一个issue，并在issue中详细描述您的想法。
- 建议：在您的代码中添加明确注释，以帮助其他人理解。
- 可选：在您的commit信息中使用[约定式提交](https://www.conventionalcommits.org/zh-hans/v1.0.0/)规范。
- 可选：使用 GPG 密钥签名您的提交。  

(使用可选项可以帮助我们快速审查您的Pull Request。)

我们会将您的贡献计入贡献者名单。您可以在[此处](https://github.com/xing-yv/fanqie-novel-download/blob/main/CONTRIBUTORS.md)获取贡献和赞助者名单。
感谢您的贡献！




## 自行封装&修改

在封装&修改此脚本之前，请确保已安装以下内容：

- Python 3.x
- 所需的Python库：requests、beautifulsoup4、packaging、ebooklib

您可以从从src目录获取程序源代码

您可以使用pip安装所需的库（标准版本）：

```shell
pip install -r requirements.txt
```

或（全部版本）

```shell
pip install -r requirements-all.txt
```

## 许可证

为保护此程序不被用于不良商业行为，

此程序根据GNU通用公共许可证第3版（GPLv3）发布，

您可以在[这里](https://www.gnu.org/licenses/gpl-3.0.html)找到许可证的副本，

请确保在使用及修改程序时遵守此许可证的条款，

请您基于此程序开发或混合后，使用GPLv3开源，感谢配合。

## 免责声明

此程序旨在用于与Python网络爬虫和网页处理技术相关的教育和研究目的。不应将其用于任何非法活动或侵犯他人权利的行为。用户对使用此程序引发的任何法律责任和风险负有责任，作者和项目贡献者不对因使用程序而导致的任何损失或损害承担责任。

在使用此程序之前，请确保遵守相关法律法规以及网站的使用政策，并在有任何疑问或担忧时咨询法律顾问。

## 作者

- 作者：星隅（xing-yv）
- GitHub仓库：[https://github.com/xing-yv/fanqie-novel-download](https://github.com/xing-yv/fanqie-novel-download)
- Gitee仓库:  [https://gitee.com/xingyv1024/fanqie-novel-download](https://gitee.com/xingyv1024/fanqie-novel-download)

## 反馈

如果您遇到问题或有改进建议，请将其提交到此项目的[GitHub issues](https://github.com/xing-yv/fanqie-novel-download/issues)页面。

## 赞助

如果您想要支持我的开发，欢迎赞助，感谢您的支持！

![mm_reward_qrcode_1696844640908](https://xyy-1314663891.cos.ap-nanjing.myqcloud.com/202310091746639.png)

![1697873019858](https://xyy-1314663891.cos.ap-nanjing.myqcloud.com/202310211527121.jpg)
