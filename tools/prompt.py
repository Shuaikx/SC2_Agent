import base64
import json

import requests

# # OpenAI API Key
# api_key = "sk-mJLxQ93g550GsibX853e3091A9014549AaE26aC41c59A72d"
from openai import OpenAI
import httpx


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def gpt4v_decision(prompt, image_path):
    # Path to your image
    client = OpenAI(
        base_url="https://api.xty.app/v1",
        api_key="sk-mJLxQ93g550GsibX853e3091A9014549AaE26aC41c59A72d",
        http_client=httpx.Client(
            base_url="https://api.xty.app/v1",
            follow_redirects=True,
        ),
    )
    # Getting the base64 string
    base64_image = encode_image(image_path)
    completion = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=300
    )
    return completion.choices[0].message.content


prompt = ("There are six actions: '0', '1', '2', '3', '4' and '5'. Each action corresponds to a reward value. "
          "For example, '0' corresponds to a reward value of 5. All reward values are in the range of 0-10. "
          "Please return a JSON-formatted output according to this request, requiring each action to be included, and the output content is only json."
          "such as:{'0': 5,'1': 7,'2': 3,'3': 9,'4': 2,'5': 6}")


def replace(prompt,image):
    result = gpt4v_decision(prompt, image)
    modified_string = result.replace("json", "")
    data = json.loads(modified_string)
    max_reward = float("-inf")  # 初始值设为负无穷
    max_reward_key = None

    # 找到最大奖励值及其对应的键
    for key, value in data.items():
        if value > max_reward:
            max_reward = value
            max_reward_key = key
    return int(max_reward_key)
# print(result)
# print(type(result))
# json_string = '''json
# {
#   "0": 5,
#   "1": 7,
#   "2": 3,
#   "3999": 9,
#   "4": 2,
#   "234": 6
# }
# '''
# modified_string = json_string.replace("json", "")
# # print(type(json_string))
# # print(modified_string)
# # #
# data = json.loads(modified_string)
# max_reward = float("-inf")  # 初始值设为负无穷
# max_reward_key = None
#
# # 找到最大奖励值及其对应的键
# for key, value in data.items():
#     if value > max_reward:
#         max_reward = value
#         max_reward_key = key
# print(max_reward_key)
# print(type(data))
