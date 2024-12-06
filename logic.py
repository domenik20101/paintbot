import json
import time
import base64
import requests


class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }
        self.styles={   
            "фото":"DEFAULT",
            "качество":"UHD",
            "аниме":"ANIME",
            "обстракция":"KANDINSKY"
        }
        self.key_style = "фото"

    def  decode(self,code):
       
        # Убираем префикс, если он есть (например, data:image/png;base64,)
        if code.startswith("data:"):
            code = code.split(",")[1]

        # Декодируем Base64 в байты
        image_data = base64.b64decode(code)

        # Сохраняем декодированное изображение в файл
        output_file_path = "decoded_image.png"  # Путь для сохранения
        with open(output_file_path, "wb") as file:
            file.write(image_data)

        print(f"Картинка сохранена в {output_file_path}")

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "style": self.styles[self.key_style],
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


if __name__ == '__main__':
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '3988AFA3DCE5FA1AB4E33610B29A594E', '2DC712E71431CE82A0F25C2E0E4BE01D')
    model_id = api.get_model()
    api.key_style = "фото"
    uuid = api.generate("закат", model_id)
    images = api.check_generation(uuid)
    print(type(images))
    api.decode(images[0])

#Не забудьте указать именно ваш YOUR_KEY и YOUR_SECRET.