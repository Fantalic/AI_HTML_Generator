
def extract_html_code(text):
    start_marker = "```html"
    end_marker = "```"
    start_index = text.find(start_marker)
    if start_index == -1:
        return text
    end_index = text.find(end_marker, start_index + len(start_marker))
    if end_index == -1:
        return text
    html_code = text[start_index + len(start_marker):end_index].strip()
    return html_code


def remove_think_tags(text):
    idx = text.find("</think>")
    if idx == -1:
        return text.strip()
    result = text[idx + len("</think>"):]
    return result.strip()
