import re


def _delete_new_lines(text):
    text = text.replace("\n", "")
    return text


def _delete_dialog_signs(text):
    text = re.sub(r'(^|\s)-\s', "", text)
    text = re.sub(r'\s{2,}', " ", text)
    return text


def normalize_text(text):
    text = _delete_new_lines(text)
    text = _delete_dialog_signs(text)
    return text
