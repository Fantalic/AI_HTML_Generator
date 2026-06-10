import requests
import json
from typing import Optional, List, Dict, Callable

from aigen_html.config import OLLAMA_BASE_URL, OLLAMA_DEFAULT_MODEL


def _call_ollama(endpoint: str, body: dict, timeout: int, stream: bool) -> requests.Response:
    headers = {"Content-Type": "application/json"}
    response = requests.post(
        endpoint, json=body, headers=headers, timeout=timeout, stream=stream
    )
    response.raise_for_status()
    return response


def _format_messages_as_prompt(messages: List[Dict]) -> str:
    parts = []
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        if role == "system":
            parts.append(f"System: {content}")
        elif role == "user":
            parts.append(f"User: {content}")
        elif role == "assistant":
            parts.append(f"Assistant: {content}")
    parts.append("Assistant:")
    return "\n\n".join(parts)


def ai_request(
    type: str = "chat",
    model: str = None,
    messages: Optional[List[Dict]] = None,
    prompt: Optional[str] = None,
    context: Optional[List[int]] = None,
    options: Optional[Dict] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    top_k: Optional[int] = None,
    repeat_penalty: Optional[float] = None,
    seed: Optional[int] = None,
    num_predict: Optional[int] = None,
    format: Optional[str] = None,
    stream: bool = False,
    request_timeout: int = 30,
    on_stream: Optional[Callable[[Dict], None]] = None,
) -> Dict:
    if not model:
        raise ValueError("Model is required")
    if type == "chat" and not messages:
        raise ValueError("Messages are required for chat type")
    if type == "generate" and not prompt:
        raise ValueError("Prompt is required for generate type")

    merged_options = options.copy() if options else {}
    for param in ['temperature', 'top_p', 'top_k',
                  'repeat_penalty', 'seed', 'num_predict']:
        if locals()[param] is not None:
            merged_options[param] = locals()[param]

    body = {
        "model": model,
        "stream": stream,
        "options": merged_options,
    }

    if format:
        body["format"] = format

    if type == "chat":
        body["messages"] = messages
    else:
        body["prompt"] = prompt
        if context is not None:
            body["context"] = context

    base = OLLAMA_BASE_URL.rstrip("/")
    endpoint = f"{base}/api/{type}"

    try:
        response = _call_ollama(endpoint, body, request_timeout, stream)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404 and type == "chat":
            prompt_text = _format_messages_as_prompt(messages)
            fallback_body = {k: v for k, v in body.items() if k != "messages"}
            fallback_body["prompt"] = prompt_text
            fallback_endpoint = f"{base}/api/generate"
            response = _call_ollama(fallback_endpoint, fallback_body, request_timeout, stream)
        else:
            raise RuntimeError(f"API request failed: {str(e)}") from e

    if stream:
        for line in response.iter_lines():
            if line:
                try:
                    data = json.loads(line.decode("utf-8"))
                    if on_stream:
                        on_stream(data)
                except json.JSONDecodeError:
                    continue
        return {"status": "stream completed"}

    data = response.json()

    if type == "chat":
        return data
    else:
        content = data.get("response", "")
        return {"message": {"content": content}}
