## Streamlit Web Chatbot

OpenAI GPT-4o-mini 기반의 간단한 스트리밍 웹 챗봇 데모입니다.  
`streamlit`, 최신 `openai` Python SDK, `python-dotenv` 를 사용합니다.

---

### 1. 프로젝트 구조

```text
.
├─ app.py                # Streamlit 엔트리 포인트
├─ requirements.txt      # 의존성 목록 (버전 미고정)
├─ src/
│  ├─ llm.py             # OpenAI 호출 및 스트리밍 처리
│  ├─ prompts.py         # 기본 시스템 프롬프트/모델
│  ├─ ui.py              # Streamlit 채팅 UI 렌더링
│  └─ utils.py           # 공통 유틸/로깅/에러 메시지
└─ .env (직접 생성)      # OPENAI_API_KEY 설정용
```

※ `.env.example` 대신, 직접 `.env` 파일을 만들어 사용합니다.

---

### 2. 사전 준비

1. Python 3.11+ 설치
2. 가상환경(optional) 생성 후 활성화

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
```

3. 패키지 설치

```bash
pip install -r requirements.txt
```

4. `.env` 파일 생성 (프로젝트 루트에 생성)

```bash
echo OPENAI_API_KEY=your-openai-api-key-here > .env
```

또는 텍스트 에디터로 `.env` 파일을 만들고 다음과 같이 작성합니다:

```text
OPENAI_API_KEY=your-openai-api-key-here
```

---

### 3. 실행 방법

프로젝트 루트에서 아래 명령을 실행합니다.

```bash
streamlit run app.py
```

브라우저가 자동으로 열리지 않는 경우, 터미널에 표시된 로컬 URL (예: `http://localhost:8501`) 을 직접 열면 됩니다.

---

### 4. UI 설명

- **페이지 설정**
  - 제목: `Streamlit Web Chatbot`
  - 아이콘: 🤖
  - 레이아웃: `wide`

- **사이드바**
  - **모델 입력**: 기본값은 `gpt-4o-mini`
  - **Temperature 슬라이더**: 0.0 ~ 1.0 (기본 0.7)
  - **🧹 대화 초기화 버튼**: 대화 히스토리 초기화
  - **시스템 프롬프트 textarea**: 현재 세션의 system 메시지를 확인/수정

- **메인 영역**
  - 기존 대화 히스토리(assistant/user)를 role 별로 `st.chat_message` 로 렌더링
  - `st.chat_input` 으로 사용자 입력
  - 사용자 메시지는 전송 즉시 화면/세션에 반영
  - 어시스턴트 응답은 토큰 단위로 스트리밍 표시
  - 스트리밍 중 상단에 로딩 상태(status 컴포넌트) 표시

---

### 5. LLM 동작 방식

- `st.session_state` 에 유지되는 값:
  - `messages: list[dict]` — `{ "role": "user" | "assistant", "content": str }`
  - `system_prompt: str`
  - `model: str`
  - `temperature: float`
- OpenAI 호출 시 messages 포맷:
  - 맨 앞에 시스템 프롬프트 메시지 (`role: system`)
  - 이후 user/assistant 히스토리
- 응답 성공 시:
  - 스트리밍 결과를 하나의 `assistant` 메시지로 합쳐 `messages` 에 append
- 에러 처리:
  - `OPENAI_API_KEY` 누락 시: 친절한 경고 메시지와 함께 실행 중단
  - 인증 오류/Rate limit/네트워크 오류/API 오류 등은 `llm.py` 에서 구분 처리 후 사용자 친화적 메시지로 표시

---

### 6. 배포 팁

- **Streamlit Cloud / 기타 PaaS**
  - 이 리포지토리를 그대로 배포 대상으로 지정
  - 대시보드 설정에서 환경 변수 `OPENAI_API_KEY` 를 등록
  - `requirements.txt` 를 자동으로 설치하도록 설정

- **기타**
  - 회사/팀 내 프록시 환경에서는 OpenAI 접속이 차단될 수 있으므로, 별도 네트워크 정책을 확인해야 합니다.

