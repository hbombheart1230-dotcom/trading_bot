# 🚀 Trading Bot with LangGraph & Gemini 3.0

키움증권 REST API(모의투자)와 LangGraph를 결합한 자율형 주식 매매 에이전트 프로젝트입니다.

---

## 🤖 For AI Agent (Gemini) Instructions

이 섹션은 AI 에이전트가 프로젝트의 컨텍스트를 파악하기 위한 가이드라인입니다. 파일을 읽을 때 이 규칙을 최우선으로 고려하세요.

### 📍 Current Project Status (2026-02-02)
1. **Core Infrastructure**: `.env`, `config.py`, `state.py` 3개 파일 업로드 완료.
2. **Setup**: 키움 모의투자 호스트(`mockapi.kiwoom.com`) 및 계좌 설정 완료.
3. **Current Goal**: 랭그래프의 각 노드(Observer, Analyst, Executor) 및 스킬(Skills) 구현 단계 진입 중.

### 🛠️ Architecture & Skill Standards
- **Skill-Based Design**: 모든 외부 연동(키움 API, 장 운영 시간 체크 등)은 `@tool` 데코레이터를 사용한 스킬로 구현할 것.
- **State Management**: 에이전트의 모든 판단 근거와 로그는 `state.py`의 `AgentState`에 기록할 것.
- **Cost Optimization**: 장 운영 외 시간에는 Gemini 호출을 방지하는 스케줄러 로직을 준수할 것.

### 📝 Working History
- **[2026-02-02]**: 프로젝트 초기화 및 모의투자 환경 설정 완료. (config, state, .env 기본 뼈대 구축)

---

## 📂 Project Structure
- `config.py`: 환경 변수 및 서버 설정 관리
- `state.py`: LangGraph용 TypedDict 상태 정의
- `.env`: API Key 및 개인 정보 (GitHub 업로드 금지/로컬 관리)

## 🛠️ Requirements
- python-dotenv
- requests
- langgraph
- google-generativeai
