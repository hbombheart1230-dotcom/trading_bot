# agents/commander.py
import json
import google.generativeai as genai
from config.settings import Settings
from config.secrets import Secrets
from prompts.commander_prompt import SYSTEM_PROMPT

class Commander:
    """
    장 시작 전/중간에 시장 상황을 분석하고 '매매 규칙(Rule)'을 생성하는 AI
    """
    def __init__(self):
        # Gemini API 설정
        genai.configure(api_key=Secrets.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Settings.MODEL_SMART)
        
    def analyze_market(self, market_data_summary=""):
        """
        AI에게 시장 정보를 주고 전략(JSON)을 받아옴
        """
        print(f"\n👮‍♂️ [Commander] {Settings.MODEL_SMART} 모델이 전략을 수립 중입니다...")
        
        # 프롬프트 조합 (시스템 지시 + 현재 시장 상황)
        full_prompt = f"{SYSTEM_PROMPT}\n\n[현재 시장 데이터]\n{market_data_summary}\n\n오늘의 전략을 JSON으로 출력하라:"
        
        try:
            # AI 호출
            response = self.model.generate_content(full_prompt)
            response_text = response.text.strip()
            
            # JSON 파싱 (혹시 마크다운 ```json ... ``` 이 붙어있을 경우 제거)
            if response_text.startswith("```"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            
            strategy = json.loads(response_text)
            
            print(f"✅ [Commander] 전략 수립 완료: {strategy.get('strategy_name')}")
            print(f"   - 목표: {strategy.get('market_summary')}")
            print(f"   - 진입: RSI {strategy['target_buy_condition']['rsi_threshold']} 이하")
            print(f"   - 손절: {strategy['risk_management']['stop_loss_pct']}%")
            
            return strategy

        except Exception as e:
            print(f"❌ [Commander] 전략 수립 실패: {e}")
            # 비상시 기본 전략 리턴
            return {
                "strategy_name": "Emergency_Fallback",
                "target_buy_condition": {"rsi_threshold": 30, "vol_multiplier": 1.5},
                "risk_management": {"stop_loss_pct": -3.0, "take_profit_pct": 3.0}
            }