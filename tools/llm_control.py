import re
import json
import sys

sys.path.append(r'C:\ai\RL\SCII-agent-main')
import json
import re
import os


def replace_placeholder_with_json_content(prompt, json_files_dir):
    # 使用正则表达式查找所有的占位符
    placeholders = re.findall(r"<\$(.*?)\$>", prompt)

    for placeholder in placeholders:
        json_file_path = os.path.join(json_files_dir, f"{placeholder}.json")
        print(json_file_path)
        try:
            # 尝试打开并读取JSON文件
            with open(json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # 将占位符替换为JSON内容的字符串表示
                json_str = json.dumps(data, indent=4)
                prompt = prompt.replace(f"<${placeholder}$>", json_str)
        except FileNotFoundError:
            print(f"文件未找到: {json_file_path}")
        except json.JSONDecodeError:
            print(f"解析JSON时出错: {json_file_path}")

    return prompt


def read_prompt(prompt_file,json_path):
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_content = f.read()
    filled_prompt = replace_placeholder_with_json_content(prompt_content,json_path)
    print(filled_prompt)
    return filled_prompt

# read_prompt(r"C:\ai\RL\SCII-agent-main\sc2_agent\prompt\action_decision.prompt")
