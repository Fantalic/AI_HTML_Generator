
import urllib
def extract_html_code(text):
    # Define the start and end markers
    start_marker = "```html"
    end_marker = "```"

    # Find the start and end positions of the markers
    start_index = text.find(start_marker)
    end_index = text.find(end_marker, start_index)

    # Check if both markers were found
    if start_index != -1 and end_index != -1:
        # Extract the HTML code
        html_code = text[start_index + len(start_marker):end_index].strip()
        html_code.replace("```html", "")
        html_code.replace("```", "")

        return html_code

    return text


def remove_think_tags(text):
    # Remove all substrings enclosed by <think>...</think> tags (including tags)
    idx = text.find("</think>")
    # return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
    thinking = text[:idx]
    # print("============THIKNKING ============")
    # print(thinking)
    # print("=================================")
    result = text[idx+len("</think>"):]
    return result.strip()


def simple_parse_qs(qs_bytes: str) -> dict[str, list[str]]:
    """
    Einfacher Parser für URL-kodierte Query-Strings.
    Gibt ein Dict zurück, bei dem jeder Schlüssel eine Liste von Werten enthält.
    Beispiel:
      "a=1&b=2&b=3" -> {'a': ['1'], 'b': ['2', '3']}
    """
    result = {}
    qs = qs_bytes.decode('utf-8')
    if not qs:
        return result

    # Aufteilen nach '&'
    pairs = qs.split('&')
    for pair in pairs:
        if not pair:
            continue
        # Aufteilen nach '=' in key und value
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            key, value = pair, ''

        # URL-dekodieren von key und value
        key = urllib.parse.unquote_plus(key)
        value = urllib.parse.unquote_plus(value)
        result[key] = value

    return result