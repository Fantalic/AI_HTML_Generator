
def extract_html_code(text):
    start_marker = "```html"
    end_marker = "```"
    start_index = text.find(start_marker)
    end_index = text.find(end_marker, start_index)
    if start_index != -1 and end_index != -1:
        html_code = text[start_index + len(start_marker):end_index].strip()
        html_code.replace("```html", "")
        html_code.replace("```", "")
        return html_code
    return text


def remove_think_tags(text):
    idx = text.find("</think>")
    thinking = text[:idx]
    result = text[idx+len("</think>"):]
    return result.strip()
