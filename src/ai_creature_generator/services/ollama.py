import requests
import json
from typing import Optional, List, Dict, Callable

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
    """
    Send a request to Ollama API with support for both chat and generate endpoints

    Args:
        type: Request type - 'chat' or 'generate'
        model: Model name to use (required)
        messages: Chat history for chat requests
        prompt: Input prompt for generate requests
        context: Context from previous response (generate only)
        options: Additional model options
        temperature: Control randomness (0.0-1.0)
        top_p: Diversity control via nucleus sampling
        top_k: Diversity control via top-k sampling
        repeat_penalty: Penalize repeated tokens
        seed: Random seed
        num_predict: Max tokens to generate
        format: Response format (e.g., 'json')
        stream: Enable streaming response
        request_timeout: Request timeout in seconds
        on_stream: Callback for streaming responses

    Returns:
        Dictionary with API response

    Raises:
        ValueError: For invalid parameters
        RuntimeError: For API request failures
    """
    # Validate required parameters
    if not model:
        raise ValueError("Model is required")
    if type == "chat" and not messages:
        raise ValueError("Messages are required for chat type")
    if type == "generate" and not prompt:
        raise ValueError("Prompt is required for generate type")

    # Merge options
    merged_options = options.copy() if options else {}
    for param in ['temperature', 'top_p', 'top_k',
                 'repeat_penalty', 'seed', 'num_predict']:
        if locals()[param] is not None:
            merged_options[param] = locals()[param]

    # Build request body
    body = {
        "model": model,
        "stream": stream,
        "options": merged_options
    }

    if format:
        body["format"] = format

    if type == "chat":
        body["messages"] = messages
    else:
        body["prompt"] = prompt
        if context is not None:
            body["context"] = context

    # Prepare request
    endpoint = f"http://localhost:11434/api/{type}"
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(
            endpoint,
            json=body,
            headers=headers,
            timeout=request_timeout,
            stream=stream
        )
        response.raise_for_status()

        if stream:
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        if on_stream:
                            on_stream(data)
                    except json.JSONDecodeError:
                        continue
            return {"status": "stream completed"}

        return response.json()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API request failed: {str(e)}") from e