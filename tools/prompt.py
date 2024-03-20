import base64
import json
import logging
import re
import requests
from tools.llm_control import *
from openai import OpenAI
import httpx
from openai import OpenAI

logging.basicConfig(filename='example.log', filemode='w', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# openai（）中放置key
def gpt_4_turbo_preview():
    logging.basicConfig(filename='gpt_4_turbo_preview.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    client = OpenAI()
    prompt2 = read_prompt(r"C:\ai\RL\SCII-agent-main\sc2_agent\prompt\action_decision.prompt",
                          r"C:\ai\RL\SCII-agent-main\sc2_agent\input")

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": "You're a StarCraft II game assistant."},
            {"role": "user", "content": prompt2},
        ]
    )
    logging.info(response.choices[0].message.content)
    result = response.choices[0].message.content
    return result


def read_json():
    result = gpt_4_turbo_preview()
    json_str_match = re.search(r"\{.*\}", result, re.DOTALL)

    if json_str_match:
        json_str = json_str_match.group(0)
        # 将JSON字符串转换为Python字典
        json_data = json.loads(json_str)
        print(json_data)
        return json_data
    else:
        print("No JSON content found.")
        return "bug"


def max_action():
    data = read_json()
    # 初始化最大奖励值和对应的动作
    max_reward = float('-inf')
    max_action = None

    # 遍历字典，找到最大奖励值及其对应的动作
    for tactic, info in data.items():
        if info['reward'] > max_reward:
            max_reward = info['reward']
            max_action = info['action']
    return max_action



def gpt4v_decision(prompt):
    # Path to your image
    client = OpenAI(
        base_url="https://api.xty.app/v1",
        http_client=httpx.Client(
            base_url="https://api.xty.app/v1",
            follow_redirects=True,
        ),
    )
    # Getting the base64 string
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
                ]
            }
        ],
        max_tokens=300
    )
    print(completion)
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content


# prompt = ("There are six actions: '0', '1', '2', '3', '4' and '5'. Each action corresponds to a reward value. "
#           "For example, '0' corresponds to a reward value of 5. All reward values are in the range of 0-10. "
#           "Please return a JSON-formatted output according to this request, requiring each action to be included, "
#           "and the output content is only json."
#           "such as:{'0': 5,'1': 7,'2': 3,'3': 9,'4': 2,'5': 6}")
# prompt2 = read_prompt(r"C:\ai\RL\SCII-agent-main\sc2_agent\prompt\action_decision.prompt",r"C:\ai\RL\SCII-agent-main\sc2_agent\input")
# gpt4v_decision(prompt2)

def replace(prompt):
    result = gpt4v_decision(prompt)
    print(result)
    modified_string = result.replace("json", "")
    data = json.loads(modified_string)
    max_reward = float("-inf")  # 初始值设为负无穷
    max_reward_key = None

    # 找到最大奖励值及其对应的键
    for key, value in data.items():
        if value > max_reward:
            max_reward = value
            max_reward_key = key
    return int(max_reward_key), result

