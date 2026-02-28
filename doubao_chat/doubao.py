import os
from volcenginesdkarkruntime import Ark

# 从环境变量中获取您的API KEY，配置方法见：https://www.volcengine.com/docs/82379/1399008
api_key = os.getenv('ARK_API_KEY')

client = Ark(
    base_url='https://ark.cn-beijing.volces.com/api/v3',
    api_key=api_key,
)

response = client.responses.create(
    model="doubao-seed-2-0-pro-260215",
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "上午好"
                },
            ],
        }
    ]
)

# 只输出模型的回复内容
for output in response.output:
    if hasattr(output, 'type') and output.type == 'message':
        for content in output.content:
            if content.type == "output_text":
                print(content.text)
