import re
import json


def replace_placeholders(prompt_file, json_file):
    # 读取 .prompt 文件内容
    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt_content = f.read()

    # 匹配 <$$> 格式的占位符
    placeholders = re.findall(r'<\$\w+\.\w+\$>', prompt_content)
    placeholderss = re.findall(r'<\$\w+\$>', prompt_content)
    placeholders = placeholders + placeholderss
    print(placeholders)
    # 读取对应的 JSON 文件内容
    with open(json_file, "r", encoding="utf-8") as f:
        json_content = json.load(f)

    # 替换占位符
    for placeholder in placeholders:
        key = placeholder.strip('<>$')
        parts = key.split('.')
        value = json_content
        for part in parts:
            value = value.get(part)
        prompt_content = prompt_content.replace(placeholder, str(value))

    return prompt_content


# # 指定 .prompt 文件和对应的 JSON 文件
# prompt_file = "a.prompt"
# json_file = "a.json"
#
# # 调用函数替换占位符并打印结果
# result = replace_placeholders(prompt_file, json_file)
# print(result)


