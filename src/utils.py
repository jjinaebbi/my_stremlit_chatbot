from __future__ import annotations

import logging
import traceback
from typing import Any, Optional

import streamlit as st


LOGGER_NAME = "streamlit_web_chatbot"


def get_logger() -> logging.Logger:
    logger = logging.getLogger(LOGGER_NAME)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def format_error_message(user_message: str, exc: Optional[BaseException] = None) -> str:
    """
    Format a friendly error message for end users and log debug details.
    """
    logger = get_logger()
    if exc is not None:
        logger.error("%s: %s", user_message, repr(exc))
        logger.debug("Traceback:\n%s", traceback.format_exc())
    return user_message


def show_error(message: str) -> None:
    st.error(message)


def show_info(message: str) -> None:
    st.info(message)


def show_success(message: str) -> None:
    st.success(message)


def require_api_key() -> bool:
    """
    Check if OPENAI_API_KEY is set and show a warning if not.
    Returns True if available, False otherwise.
    """
    import os

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.warning(
            "환경 변수 `OPENAI_API_KEY` 가 설정되지 않았습니다. "
            "`.env` 파일 또는 시스템 환경 변수에 OpenAI API 키를 설정해주세요."
        )
        return False
    return True


def get_session(key: str, default: Any) -> Any:
    return st.session_state.get(key, default)


def set_session(key: str, value: Any) -> None:
    st.session_state[key] = value

