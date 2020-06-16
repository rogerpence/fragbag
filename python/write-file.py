def write_file(full_file_path, content):
    with open(full_file_path, 'w', encoding='utf-8') as fw:
        fw.write(content)
        fw.close()

