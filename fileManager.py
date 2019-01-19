import json


def read_json_file(filename: str):
    try:
        with open('files/' + filename, encoding='utf-8') as f:
            return json.load(f)
    except:
        print('警告：没有此文件！')


def write_json_file(content, filename: str):
    try:
        with open('files/' + filename, 'w', encoding='utf-8') as f:
            json.dump(content, f)
            return True
    except:
        print('警告：写文件失败！')
        return False


def read_text_file(filename: str):
    try:
        with open('files/' + filename, encoding='utf-8') as f:
            return f.read()
    except:
        print('警告：没有此文件！')


def write_text_file(content, filename: str):
    try:
        with open('files/' + filename, 'w', encoding='utf-8') as f:
            f.write(content)
            return True
    except:
        print('警告：写文件失败！')
        return False


