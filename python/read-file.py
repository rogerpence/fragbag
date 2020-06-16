def read_file(full_file_path):
    content = None
    with open(full_file_path, 'r', encoding='utf-8') as fr:
        content = fr.read()
        fr.close()
    return content