from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

def setup_openai_api(api_key):
    openai.api_key = api_key

def get_perfume_recommendation(adjective):
    prompt = f"향수 추천가로서, '{adjective}'이(가) 주요 특징인 향수를 1개 추천해주세요. 향수 이름과 그 특징을 설명해주세요."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000
    )
    return response.choices[0].text.strip()

def create_imaginary_perfume_image(perfume_name, description):
    prompt = f"상상 속의 향수 이미지: 향수 이름은 '{perfume_name}'이고, 설명은 '{description}'입니다."
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    return response.data[0]["url"]

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    message = data['message']
    recommendation = get_perfume_recommendation(message)
    perfume_name, description = recommendation.split(":", 1)
    image_url = create_imaginary_perfume_image(perfume_name.strip(), description.strip())
    return jsonify({'message': recommendation, 'image_url': image_url})

@app.route('/')
def index():
    return app.send_static_file('index.html')

if __name__ == "__main__":
    api_key = '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'
    setup_openai_api(api_key)
    app.run(host='0.0.0.0', port=5000)
        
