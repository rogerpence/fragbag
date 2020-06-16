def write_file(full_file_path, content):
    with open(full_file_path, "w") as fw:
        fw.write(content)
        fw.close()

def read_file(full_file_path):
    content = None
    with open(full_file_path, 'r') as fr:
        content = fr.read()
        fr.close()
    return content
