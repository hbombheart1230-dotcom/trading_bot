Gemini_Trading_Bot/

│

├── .env                    # [보안] API Key, 계좌 비밀번호

├── main.py                 # [실행] 프로그램의 시작점 (무한루프 X, 스케줄러 O)

│

├── config/                 # [설정] 건드리지 않는 고정 설정

│   ├── __init__.py

│   ├── settings.py         # 기본 상수 (로그 경로, 기본 모델명)

│   └── secrets.py          # .env 로드 및 검증

│

├── memory/                 # [기억] 🌟 V6 핵심: AI의 도서관 (RAG)

│   ├── __init__.py

│   ├── trade_logs/         # [Raw] 매일매일의 매매 기록 (CSV/JSON)

│   ├── journals/           # [Thought] AI가 작성한 매매 일기 & 반성문 (Txt)

│   └── knowledge_base/     # [Vector] "이런 장세엔 RSI 20이 맞더라" 패턴 DB

│

├── prompts/                # [지시] AI에게 주는 역할 정의서 (Code와 분리)

│   ├── __init__.py

│   ├── commander_prompt.py # (장전) "전략 수립해"

│   ├── sniper_prompt.py    # (장중) "살까 말까? 팔까 말까?"

│   └── reviewer_prompt.py  # (장후) "오늘 매매 반성해"

│

├── agents/                 # [두뇌] AI 에이전트 구현체 (Gemini API 호출)

│   ├── __init__.py

│   ├── commander.py        # 거시경제 + Memory 조회 -> Rule 생성

│   ├── sniper.py           # 실시간 상황 판단 -> 매매 결정

│   └── reviewer.py         # 로그 분석 -> Memory 업데이트

│

├── core/                   # [몸통] 시스템 핵심 로직 (AI X, Python O)

│   ├── __init__.py

│   ├── engine.py           # 🌟 전체 흐름 제어 (State Machine: IDLE->WATCH->COOLDOWN)

│   ├── rule_parser.py      # 🌟 AI가 준 JSON 규칙을 Python 조건문으로 변환 (할루시네이션 방지)

│   └── skill_loader.py     # 스킬 동적 로딩기

│

├── libs/                   # [인프라] 기초 공사 (변하지 않는 기능)

│   ├── __init__.py

│   ├── auth.py             # 키움 로그인/접속 관리

│   ├── network.py          # API 요청/제한/재시도 관리

│   ├── rag_manager.py      # 🌟 Memory에서 과거 데이터 검색/저장 (Vector Search)

│   └── logger.py           # 파일 기록 담당

│

└── skills/                 # [도구] AI가 꺼내 쓰는 부품들 (계속 추가됨)

    ├── __init__.py

    ├── market_watcher.py   # 시세/호가/체결강도 조회

    ├── account_manager.py  # 잔고 확인/주문 전송

    ├── chart_calculator.py # RSI, MACD 등 지표 계산 (수학)

    └── news_finder.py      # (확장) 뉴스 검색
