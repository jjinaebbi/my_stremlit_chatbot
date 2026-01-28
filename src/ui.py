from __future__ import annotations

from typing import Dict, List

import streamlit as st

from .llm import stream_chat_completion
from .prompts import DEFAULT_MODEL
from .utils import require_api_key, set_session


def _init_sidebar() -> None:
    with st.sidebar:
        st.header("⚙️ 설정")

        model = st.text_input(
            "모델",
            value=st.session_state.get("model", DEFAULT_MODEL),
            help="사용할 OpenAI 모델 이름입니다.",
        )
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=float(st.session_state.get("temperature", 0.7)),
            step=0.05,
        )

        st.session_state.model = model
        st.session_state.temperature = temperature

        if st.button("🧹 대화 초기화"):
            st.session_state.messages = []
            st.session_state.chat_reset = True
        else:
            st.session_state.chat_reset = False

        st.subheader("📝 시스템 프롬프트")
        system_prompt = st.text_area(
            "System Prompt",
            value=st.session_state.get("system_prompt", ""),
            height=200,
            help="모델의 기본 행동을 제어하는 시스템 메시지입니다.",
        )
        st.session_state.system_prompt = system_prompt


def _render_history(messages: List[Dict[str, str]]) -> None:
    for msg in messages:
        role = msg.get("role")
        content = msg.get("content", "")
        if role == "system":
            # 시스템 메시지는 기본적으로 표시하지 않지만,
            # 필요하다면 아래 주석을 해제하여 표시할 수 있습니다.
            # with st.chat_message("system"):
            #     st.markdown(content)
            continue
        with st.chat_message("assistant" if role == "assistant" else "user"):
            st.markdown(content)


def _build_messages_for_llm() -> List[Dict[str, str]]:
    system_prompt = st.session_state.get("system_prompt", "")
    messages: List[Dict[str, str]] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.extend(st.session_state.get("messages", []))
    return messages


def render_chat_page() -> None:
    st.title("🤖 Streamlit Web Chatbot")
    st.caption("OpenAI GPT-4o-mini 기반 스트리밍 웹 챗봇 데모")

    _init_sidebar()

    if not require_api_key():
        st.stop()

    # 기존 대화 렌더링
    messages: List[Dict[str, str]] = st.session_state.get("messages", [])
    _render_history(messages)

    # 사용자 입력
    user_input = st.chat_input("메시지를 입력하세요...")
    if user_input:
        # 사용자 메시지를 즉시 화면과 세션에 반영
        user_msg = {"role": "user", "content": user_input}
        st.session_state.messages.append(user_msg)
        with st.chat_message("user"):
            st.markdown(user_input)

        # 어시스턴트 스트리밍 응답
        with st.chat_message("assistant"):
            placeholder = st.empty()
            status = st.status("응답 생성 중입니다...", expanded=False)

            all_messages = _build_messages_for_llm()
            token_stream, error_message = stream_chat_completion(
                messages=all_messages,
                model=st.session_state.get("model", DEFAULT_MODEL),
                temperature=float(st.session_state.get("temperature", 0.7)),
            )

            if error_message:
                status.update(
                    label="오류가 발생했습니다.",
                    state="error",
                )
                placeholder.error(error_message)
                return

            full_response = ""
            for token in token_stream:
                full_response += token
                placeholder.markdown(full_response + "▌")

            placeholder.markdown(full_response)
            status.update(
                label="응답 생성 완료",
                state="complete",
            )

        # 세션에 어시스턴트 메시지 추가
        assistant_msg = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(assistant_msg)

