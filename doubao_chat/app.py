import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from volcenginesdkarkruntime import Ark

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# 从环境变量中获取API KEY
api_key = os.getenv('ARK_API_KEY')

client = Ark(
    base_url='https://ark.cn-beijing.volces.com/api/v3',
    api_key=api_key,
)

@app.route('/')
def index():
    return app.send_static_file('doubao_chat.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': '消息不能为空'}), 400
        
        response = client.responses.create(
            model="doubao-seed-2-0-pro-260215",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": user_message
                        },
                    ],
                }
            ]
        )
        
        # 提取模型回复
        reply = ""
        for output in response.output:
            if hasattr(output, 'type') and output.type == 'message':
                for content in output.content:
                    if content.type == "output_text":
                        reply = content.text
                        break
        
        return jsonify({
            'success': True,
            'reply': reply
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)