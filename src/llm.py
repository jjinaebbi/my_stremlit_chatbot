from typing import Dict, Iterable, List, Tuple

from openai import OpenAI, APIConnectionError, AuthenticationError, RateLimitError, APIStatusError

from .utils import format_error_message


def get_client() -> OpenAI:
    """
    Create an OpenAI client.

    The OPENAI_API_KEY is read from the environment by the SDK.
    """
    return OpenAI()


def stream_chat_completion(
    messages: List[Dict[str, str]],
    model: str,
    temperature: float,
) -> Tuple[Iterable[str], str]:
    """
    Stream a chat completion response from OpenAI.

    Returns a tuple of (token_iterator, error_message).
    If error_message is non-empty, token_iterator will be an empty iterator.
    """
    try:
        client = get_client()
        stream = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=True,
        )

        def token_generator():
            for chunk in stream:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content

        return token_generator(), ""

    except AuthenticationError as e:
        return iter(()), format_error_message(
            "인증 오류가 발생했습니다. OPENAI_API_KEY를 확인해주세요.",
            e,
        )
    except RateLimitError as e:
        return iter(()), format_error_message(
            "요청 제한에 도달했습니다. 잠시 후 다시 시도해주세요.",
            e,
        )
    except APIConnectionError as e:
        return iter(()), format_error_message(
            "OpenAI 서버에 연결할 수 없습니다. 네트워크 상태를 확인해주세요.",
            e,
        )
    except APIStatusError as e:
        return iter(()), format_error_message(
            f"OpenAI API 오류가 발생했습니다. (status: {e.status_code})",
            e,
        )
    except Exception as e:  # noqa: BLE001
        return iter(()), format_error_message(
            "알 수 없는 오류가 발생했습니다.",
            e,
        )

