def read_text_file(file) -> str:
    return file.read().decode("utf-8")

def text_to_lines(text: str) -> list:
    return text.strip().splitlines()
