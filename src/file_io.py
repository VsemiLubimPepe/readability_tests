def read_txt_file(file_path):
    with open(file_path, "r") as txt_file:
        text = txt_file.read()
    return text


def write_txt_file(file_path, text):
    with open(file_path, "w") as txt_file:
        txt_file.write(text)
    return
