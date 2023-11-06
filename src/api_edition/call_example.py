import requests
import json

# 定义请求的URL
url = 'http://localhost:5000/api'

# 定义请求的数据
data = {
    'class': 'add',
    'id': '7288189907074288674'
}

# 将数据转换为JSON格式
json_data = json.dumps(data)

# 定义请求头部
headers = {'Content-Type': 'application/json'}

# 发送POST请求
response = requests.post(url, data=json_data, headers=headers)

# 打印响应内容
print(response.json())

input()
