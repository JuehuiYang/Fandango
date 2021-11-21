import os
import re
from collections import Counter

root_path = 'D:\\fandango-algo'


def title_handler(raw_title):
    title_text = raw_title.lstrip('#').rstrip('\n').strip(' ')
    # !!!如果标题中包含了更多标题符号，这里都要处理掉，总之目录标题定位中不能够包含标点符号
    title_marker = '#' + title_text.lower().replace(' ', '-').replace('.', '').replace('&', '').replace(':',
                                                                                                        '-').replace(
        '(', '-').replace(')', '-')
    level = Counter(raw_title)['#']

    print(
        f'Get title: {title_text} --- marker: {title_marker} --- title level: {level}')

    title_loc = '    ' * (level - 1) + '* [{}]({})'.format(title_text, title_marker) + '\n'
    # title_loc = markdown.markdown(title_loc)
    print(title_loc)
    return title_loc


def add_toc_for_github(folder, file_name):
    path = folder + '\\' + file_name
    bak_path = path + '.bak'
    toc_path = path + '.toc'

    with open(path, 'r', encoding='utf-8') as f1, open(toc_path, 'w', encoding='utf-8') as f2:
        for line in f1:
            if line.startswith('#'):
                toc_line = title_handler(line)
                f2.write(toc_line)

    with open(toc_path, 'r', encoding='utf-8') as f1, open(path, 'r', encoding='utf-8') as f2, open(bak_path, 'w',
                                                                                                    encoding='utf-8') as f3:
        for line in f1:
            f3.write(line)

        for line in f2:
            if 'toc' not in line:
                f3.write(line)

    os.remove(path)
    os.remove(toc_path)
    os.rename(bak_path, path)
    print(f'Transfer successful: {path}')


def modify_file():
    pattern = re.compile(r'(.*)\\(.*\.md)')
    folder, file_name = re.match(pattern, root_path).group(1, 2)
    add_toc_for_github(folder, file_name)


def modify_folder():
    for folder, subfolders, file_names in os.walk(root_path):
        print(f'The current folder is {folder}\n-----\n')
        for subfolder in subfolders:
            print(f'The subfolder in current folder is {subfolder}')
        for file_name in file_names:
            if '.md' in file_name:
                print(f'File inside {folder}: {file_name}\n')
                add_toc_for_github(folder, file_name)


if __name__ == "__main__":
    if '.md' in root_path:
        modify_file()
    else:
        modify_folder()
