import json
import re
# bs = b'\xc4\xe3'
# print(type(bs))
# print(bs.decode('gb2312'))

parser_blank_line = re.compile(r'^\r\n')
parser_blank = re.compile(r'^ ')
parser_word = re.compile(r'^[a-z]+\r\n$')
parser_translated = re.compile(r'^[a-z]')
parser_example = re.compile(r'^[A-Z]')
# parser_blank_line(line)

def read_wordbook(filename):
    wordbook = []
    with open(filename, 'rb') as f:
        wordbook_data = f.readlines()
        # wordbook_data = wordbook_data.decode('gb2312')
        # print(wordbook_data)
        word = {}
        for line in wordbook_data:
            line = line.decode('gb2312')
            # print(line)
            if parser_blank_line.match(line):
                # print("\n")
                continue
            elif parser_blank.match(line):
                # print("\n")
                continue
            elif parser_word.match(line):
                if word is not None:
                    old_word = word.copy()
                    wordbook.append(old_word)
                    # print(word)
                    word.clear()
                word['word'] = line.splitlines(False).pop()
                # print('word',line)
            elif parser_translated.match(line):
                word['translated'] = line.splitlines(False).pop()
                # print('translated',line)
            elif parser_example.match(line):
                word['example'] = line.splitlines(False).pop()
                # print('example',line)
            else:
               word['example_cn'] = line.splitlines(False).pop()
                # print('example_cn',line)
    return wordbook


def write_wordbook_json(wordbook_json,filename):
    with open(filename, 'w') as f:
        f.writelines(wordbook_json)

wordbook = read_wordbook('TOEFL.txt')
wordbook_json = json.dumps(wordbook)
write_wordbook_json(wordbook_json, 'wordbook.json')


# print(wordbook_data)
