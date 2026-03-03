# test_push.py
import requests
from datetime import datetime  # 必须加这一行！

WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=14e53ef1-9f6c-41d9-908c-47b681fd6d77"

payload = {
    "msgtype": "text",
    "text": {
        "content": f"JARVIS 纯文本测试\n时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n收到请回复 1\n来自海波的钢铁侠项目"
    }
}

try:
    resp = requests.post(WEBHOOK, json=payload, timeout=10)
    print("状态码:", resp.status_code)
    print("响应内容:", resp.json())
except Exception as e:
    print("异常:", str(e))