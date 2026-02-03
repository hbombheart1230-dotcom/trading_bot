import google.generativeai as genai
from typing import TypedDict
from langgraph.graph import StateGraph, END
from skills.kiwoom import KiwoomSkill
import os
import json
from dotenv import load_dotenv

# 1. 환경변수 및 모델 로드
load_dotenv()
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")
MODE = os.getenv("TRADING_MODE", "MOCK")

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(MODEL_NAME)
kiwoom = KiwoomSkill(mode=MODE)

# 2. 상태 정의
class TradingState(TypedDict):
    ticker: str
    market: dict
    position: dict
    decision: str
    reason: str

# 3. 노드 정의
def analyze_node(state: TradingState):
    ticker = state['ticker']
    
    # 데이터 수집
    market = kiwoom.get_market_data(ticker)
    pos = kiwoom.get_position(ticker)
    
    if not market: return {"decision": "HOLD", "reason": "Data Fail"}

    # 프롬프트 (공격형 스캘퍼 페르소나)
    prompt = f"""
    [Asset] {ticker} | Price: {market['price']} | RSI: {market['rsi']} | Ratio: {market['power_ratio']}
    [My Pos] Qty: {pos['qty']} | ROI: {pos['roi']}% 
    
    [Rules]
    1. SELL if ROI <= -3.0% (Stop Loss)
    2. SELL if ROI >= 5.0% (Take Profit)
    3. BUY if Qty==0 AND RSI < 35 AND Ratio > 1.2
    4. Else HOLD
    
    Output JSON: {{"decision": "BUY/SELL/HOLD", "reason": "brief reason"}}
    """
    
    try:
        res = model.generate_content(prompt)
        ai = json.loads(res.text.replace("```json", "").replace("```", ""))
    except:
        ai = {"decision": "HOLD", "reason": "Error"}
        
    print(f"🤖 [Gemini] {ai['decision']} ({ai['reason']})")
    return {"decision": ai['decision'], "reason": ai['reason'], "market": market, "position": pos}

def execution_node(state: TradingState):
    decision = state['decision']
    ticker = state['ticker']
    qty = state['position']['qty']
    
    if decision == 'BUY' and qty == 0:
        # 공격형 진입: 테스트용 10주 매수
        kiwoom.send_order(ticker, "buy", 10)
        
    elif decision == 'SELL' and qty > 0:
        # 전량 청산
        kiwoom.send_order(ticker, "sell", qty)
        
    return state

# 4. 그래프 연결
workflow = StateGraph(TradingState)
workflow.add_node("Brain", analyze_node)
workflow.add_node("Hand", execution_node)
workflow.set_entry_point("Brain")
workflow.add_edge("Brain", "Hand")
workflow.add_edge("Hand", END)
app = workflow.compile()
