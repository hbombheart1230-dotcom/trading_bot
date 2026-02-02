import time
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from state import AgentState
from config import Config

# 1. 에이전트가 사용할 도구(Skill) 정의
def check_market_status(ticker: str):
    """현재 장 운영 시간인지 확인하는 함수 (예시 로직)"""
    return "현재 한국 정규장 운영 중입니다."

# 2. 제미나이 모델 설정 (3.0 Pro)
llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", google_api_key=Config.GEMINI_API_KEY)

def trading_agent(state: AgentState):
    # 에이전트의 사고 과정
    prompt = f"""
    당신은 전문 주식 트레이더입니다. 
    현재 종목: {state['ticker']}
    시장 상황: {check_market_status(state['ticker'])}
    
    위 상황을 분석하여 BUY, SELL, HOLD 중 하나를 결정하고 이유를 설명하세요.
    결과는 반드시 JSON 형식으로 답하세요.
    """
    response = llm.invoke(prompt)
    # 실제 운영 시에는 여기서 JSON 파싱 로직이 들어갑니다.
    return {
        "decision": "HOLD", 
        "reason": "테스트 모드: 장 운영 상태 확인 완료",
        "logs": ["에이전트가 시장 상황을 확인했습니다."]
    }

# 3. 그래프 조립
workflow = StateGraph(AgentState)
workflow.add_node("agent", trading_agent)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

app = workflow.compile()

if __name__ == "__main__":
    print("🚀 에이전트 가동...")
    inputs = {"ticker": "005930", "logs": [], "messages": []}
    result = app.invoke(inputs)
    print(f"결정: {result['decision']}")
    print(f"사유: {result['reason']}")
