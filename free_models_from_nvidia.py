import os
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor, TimeoutError, as_completed
from typing import Dict, Iterator, Union, Callable, Iterable, List, Optional, Tuple

FREE_MODELS = ['nvidia/gliner-pii',
 'nvidia/nemotron-content-safety-reasoning-4b',
 'google/gemma-2-2b-it',
 'mistralai/mistral-large-3-675b-instruct-2512',
 'meta/llama-4-maverick-17b-128e-instruct',
 'google/gemma-3n-e2b-it',
 'mistralai/mistral-nemotron',
 'google/gemma-3-27b-it',
 'moonshotai/kimi-k2-instruct-0905',
 'meta/llama-guard-4-12b',
 'nvidia/nemotron-3-content-safety',
 'nvidia/nemotron-3-nano-30b-a3b',
 'nvidia/llama-3.1-nemotron-ultra-253b-v1',
 'deepseek-ai/deepseek-v3.2',
 'google/gemma-3n-e4b-it',
 'moonshotai/kimi-k2-instruct',
 'nvidia/llama-3.1-nemotron-nano-vl-8b-v1',
 'mistralai/mistral-medium-3-instruct',
 'nvidia/nemotron-nano-12b-v2-vl',
 'moonshotai/kimi-k2-thinking',
 'mistralai/magistral-small-2506',
 'deepseek-ai/deepseek-v3.1-terminus',
 'nvidia/llama-3.3-nemotron-super-49b-v1.5',
 'z-ai/glm-5.1',
 'minimaxai/minimax-m2.7']


def call_nvidia_model(
    messages: List[Dict[str, str]],
    model: str = "z-ai/glm4.7",
    api_key: Optional[str] = None,
    base_url: str = "https://integrate.api.nvidia.com/v1",
    temperature: float = 0.2,
    max_tokens: int = 512,
    stream: bool = False,
) -> Union[str, Iterator[str]]:
    """
    Call an NVIDIA-hosted model through NVIDIA's OpenAI-compatible API.

    Args:
        messages: A list of chat messages in OpenAI format, for example:
            [{"role": "user", "content": "Hello"}]
        model: The NVIDIA model name, for example "z-ai/glm4.7".
        api_key: NVIDIA API key. If not provided, reads from NVIDIA_API_KEY.
        base_url: NVIDIA's OpenAI-compatible API base URL.
        temperature: Sampling temperature.
        max_tokens: Maximum number of output tokens.
        stream: Whether to use streaming output.

    Returns:
        If stream is False, returns the full response text as a string.
        If stream is True, returns an iterator that yields text chunks.

    Raises:
        ValueError: If no API key is provided and NVIDIA_API_KEY is not set.
    """
    api_key = api_key or os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError(
            "Missing NVIDIA API key. Pass api_key or set NVIDIA_API_KEY."
        )

    client = OpenAI(
        api_key=api_key,
        base_url=base_url,
    )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=stream,
    )

    if not stream:
        return response.choices[0].message.content or ""

    def text_stream() -> Iterator[str]:
        for chunk in response:
            if not chunk.choices:
                continue
            delta = chunk.choices[0].delta
            if delta and getattr(delta, "content", None):
                yield delta.content

    return text_stream()


def get_completion(
    prompt: str,
    model: str = "google/gemma-2-2b-it",
    api_key: Optional[str] = None,
    base_url: str = "https://integrate.api.nvidia.com/v1",
    temperature: float = 0.2,
    max_tokens: int = 512,
    stream: bool = False,
) -> str:
    """
    Get a completion from an NVIDIA-hosted model for a given prompt.

    Args:
        prompt: The input prompt string.
        model: The NVIDIA model name, for example "z-ai/glm4.7".
        api_key: NVIDIA API key. If not provided, reads from NVIDIA_API_KEY.
        base_url: NVIDIA's OpenAI-compatible API base URL.
        temperature: Sampling temperature.
        max_tokens: Maximum number of output tokens. 
    Returns:
        The completion text as a string.
    Raises:
        ValueError: If no API key is provided and NVIDIA_API_KEY is not set.
    """
    messages = [{"role": "user", "content": prompt}]
    return call_nvidia_model(
        messages=messages,
        model=model,
        api_key=api_key,
        base_url=base_url,
        temperature=temperature,
        max_tokens=max_tokens,
        stream=stream,
    )


def check_models(
    models: Iterable[str],
    get_completion: Callable[[str, str], object]=get_completion,
    prompt: str = "Just say hi",
    timeout: float = 0.5,
    max_workers: Optional[int] = None,
) -> Tuple[List[str], List[str]]:
    """
    Return (working_models, failed_models).
    """
    models = list(models)
    working_models: List[str] = []
    failed_models: List[str] = []

    def probe(model: str) -> Tuple[str, bool]:
        with ThreadPoolExecutor(max_workers=1) as single_executor:
            future = single_executor.submit(get_completion, prompt, model)
            try:
                future.result(timeout=timeout)
                return model, True
            except TimeoutError:
                return model, True
            except Exception:
                return model, False

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(probe, model) for model in models]

        for future in as_completed(futures):
            try:
                model, ok = future.result()
                if ok:
                    working_models.append(model)
                else:
                    failed_models.append(model)
            except Exception:
                pass

    return working_models, failed_models




if __name__ == "__main__":
    working_models, failed_models = check_models(
        models=FREE_MODELS,
        prompt="Just say hi",
        timeout=0.5,
        max_workers=16,
    )

    print("Working models:")
    print(working_models)
    print()
    print("Failed models:")
    print(failed_models)
