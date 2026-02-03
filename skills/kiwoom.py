import requests
import pandas as pd
import os
import time

class KiwoomSkill:
    def __init__(self, mode="MOCK"):
        # 환경변수에 따라 호스트 주소 자동 결정
        if mode == "MOCK":
            self.host = 'https://mockapi.kiwoom.com'
            print("🛠️ [Kiwoom] 모의투자 모드(MOCK)로 연결합니다.")
        else:
            self.host = 'https://api.kiwoom.com'
            print("💰 [Kiwoom] 실전투자 모드(REAL)로 연결합니다. 주의하세요!")

        self.app_key = os.getenv("KIWOOM_APP_KEY")
        self.app_secret = os.getenv("KIWOOM_APP_SECRET")
        self.token = None
        
        # Rate Limit: API 호출 간격 조절 (안전장치)
        self.last_req_time = 0
        self.MIN_INTERVAL = 0.35 

    def _wait(self):
        """API 과부하 방지 대기"""
        elapsed = time.time() - self.last_req_time
        if elapsed < self.MIN_INTERVAL:
            time.sleep(self.MIN_INTERVAL - elapsed)
        self.last_req_time = time.time()

    def _header(self, api_id):
        if not self.token: self.auth()
        return {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'api-id': api_id
        }

    def auth(self):
        """토큰 발급"""
        self._wait()
        url = f"{self.host}/oauth2/token"
        data = { "grant_type": "client_credentials", "appkey": self.app_key, "appsecret": self.app_secret }
        try:
            res = requests.post(url, headers={'Content-Type': 'application/json;charset=UTF-8'}, json=data)
            if res.status_code == 200:
                self.token = res.json().get("access_token")
                return True
            print(f"❌ 인증 실패: {res.text}")
            return False
        except Exception as e:
            print(f"❌ 연결 오류: {e}")
            return False

    def get_market_data(self, ticker):
        """현재가, 호가, RSI 계산"""
        self._wait()
        # 1. 현재가
        res = requests.post(f"{self.host}/api/dostk/stkinfo", headers=self._header('ka10001'), json={'stk_cd': ticker})
        if res.status_code != 200: return None
        price = int(res.json().get('output', {}).get('stck_prpr', 0))

        # 2. 호가 (매수/매도 강도)
        self._wait()
        res_book = requests.post(f"{self.host}/api/dostk/mrkcond", headers=self._header('ka10004'), json={'stk_cd': ticker})
        book = res_book.json().get('output', {})
        buy_r = int(book.get('total_bid_r', 0))
        sell_r = int(book.get('total_ask_r', 0))

        # 3. RSI 계산 (최근 20개 캔들)
        rsi = 50.0
        self._wait()
        res_chart = requests.post(f"{self.host}/api/dostk/mrkcond", headers=self._header('ka10006'), json={'stk_cd': ticker})
        charts = res_chart.json().get('output', [])
        
        if charts:
            df = pd.DataFrame(charts)
            df['close'] = df['stck_prpr'].astype(float)
            delta = df['close'].diff(1)
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            df['RSI'] = 100 - (100 / (1 + rs))
            if not pd.isna(df['RSI'].iloc[0]): rsi = round(df['RSI'].iloc[0], 2)

        return {
            "ticker": ticker, "price": price, "rsi": rsi,
            "power_ratio": round(buy_r / max(sell_r, 1), 2)
        }

    def get_position(self, ticker):
        """내 잔고 확인"""
        self._wait()
        # 모의투자는 body가 비어있음
        res = requests.post(f"{self.host}/api/dostk/acnt", headers=self._header('ka00001'), json={})
        
        pos = {"qty": 0, "pnl": 0, "roi": 0.0}
        if res.status_code == 200:
            data = res.json().get('output', [])
            for item in data:
                if item.get('stk_cd') == ticker:
                    pos['qty'] = int(item.get('hldg_qty', 0))
                    pos['pnl'] = int(item.get('eval_pnl', 0))
                    pos['roi'] = float(item.get('profit_rate', 0.0))
                    break
        return pos

    def send_order(self, ticker, action, qty, price=0):
        """주문 전송"""
        self._wait()
        trade_type = "03" if price == 0 else "00" # 03:시장가
        
        data = {
            'dmst_stex_tp': 'KRX', 'stk_cd': ticker, 'ord_qty': str(qty),
            'ord_uv': str(price) if price > 0 else "", 'trde_tp': trade_type, 'cond_uv': ''
        }
        
        res = requests.post(f"{self.host}/api/dostk/ordr", headers=self._header('kt10000'), json=data)
        if res.status_code == 200:
            print(f"🚀 [주문성공] {action.upper()} {qty}주")
            return True
        print(f"❌ 주문실패: {res.text}")
        return False
