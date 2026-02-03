import pandas as pd
from libs.kiwoom_client import KiwoomClient     # 통신 담당 Import
from libs.indicators import TechnicalAnalyzer   # 계산 담당 Import

class KiwoomSkill:
    """
    [Business Layer]
    역할: AI 에이전트와 통신/계산 모듈 사이의 오케스트레이터
    """
    def __init__(self, mode="MOCK"):
        # 통신 모듈 인스턴스화
        self.client = KiwoomClient(mode) 

    def get_market_context(self, ticker):
        """
        AI가 호출하는 메인 함수.
        Client로 데이터를 긁어오고 Analyzer로 분석해서 리턴.
        """
        # 1. [Client] 데이터 수집
        # 1-1. 현재가
        res_price = self.client.post('/api/dostk/stkinfo', {'stk_cd': ticker}, 'ka10001')
        price = int(res_price.json()['output']['stck_prpr']) if res_price and res_price.status_code == 200 else 0

        # 1-2. 호가
        res_book = self.client.post('/api/dostk/mrkcond', {'stk_cd': ticker}, 'ka10004')
        book = res_book.json().get('output', {}) if res_book and res_book.status_code == 200 else {}
        buy_vol = int(book.get('total_bid_r', 0))
        sell_vol = int(book.get('total_ask_r', 0))
        ratio = round(buy_vol / max(sell_vol, 1), 2)

        # 1-3. 차트 (과거 데이터)
        res_chart = self.client.post('/api/dostk/mrkcond', {'stk_cd': ticker}, 'ka10006')
        df = pd.DataFrame(res_chart.json().get('output', [])) if res_chart and res_chart.status_code == 200 else None

        # 2. [Analyzer] 지표 계산
        rsi = TechnicalAnalyzer.calc_rsi(df)
        ma20 = TechnicalAnalyzer.calc_ma(df, 20)
        
        # 3. 데이터 패키징 (AI Context)
        return {
            "ticker": ticker,
            "price": price,
            "indicators": {
                "rsi": rsi,
                "ma20": ma20,
                "trend": "UP" if price > ma20 else "DOWN"
            },
            "orderbook": {
                "power_ratio": ratio, # 매수/매도 잔량비
                "buy_vol": buy_vol,
                "sell_vol": sell_vol
            }
        }

    def send_order(self, ticker, action, qty, price=0):
        """주문 요청도 Client에게 위임"""
        trade_type = "03" if price == 0 else "00"
        data = {
            'dmst_stex_tp': 'KRX', 'stk_cd': ticker, 'ord_qty': str(qty),
            'ord_uv': str(price) if price > 0 else "", 'trde_tp': trade_type, 'cond_uv': ''
        }
        
        res = self.client.post('/api/dostk/ordr', data, 'kt10000')
        if res and res.status_code == 200:
            print(f"🚀 [Order] {action.upper()} {qty}주 전송 완료")
            return True
        return False
