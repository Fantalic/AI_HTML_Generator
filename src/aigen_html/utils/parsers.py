
import urllib

def simple_parse_qs(qs_bytes: str) -> dict[str, list[str]]:
    result = {}
    qs = qs_bytes.decode('utf-8')
    if not qs:
        return result
    pairs = qs.split('&')
    for pair in pairs:
        if not pair:
            continue
        if '=' in pair:
            key, value = pair.split('=', 1)
        else:
            key, value = pair, ''
        key = urllib.parse.unquote_plus(key)
        value = urllib.parse.unquote_plus(value)
        result[key] = value
    return result
