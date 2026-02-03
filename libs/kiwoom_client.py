import requests
import time
import os

class KiwoomClient:
    """
    [Transport Layer]
    역할: 인증(Auth), 토큰 관리, API 호출(Request), 속도 제한(Rate Limit)
    """
    def __init__(self, mode="MOCK"):
        if mode == "MOCK":
            self.host = 'https://mockapi.kiwoom.com'
            print("🛠️ [Client] 모의투자 서버 연결 설정")
        else:
            self.host = 'https://api.kiwoom.com'
            print("💰 [Client] 실전투자 서버 연결 설정")

        self.app_key = os.getenv("KIWOOM_APP_KEY")
        self.app_secret = os.getenv("KIWOOM_APP_SECRET")
        self.token = None
        
        # Rate Limit 설정
        self.last_req_time = 0
        self.MIN_INTERVAL = 0.35 # 초당 약 3회

    def _wait_rate_limit(self):
        """API 과부하 방지 (자동 대기)"""
        elapsed = time.time() - self.last_req_time
        if elapsed < self.MIN_INTERVAL:
            time.sleep(self.MIN_INTERVAL - elapsed)
        self.last_req_time = time.time()

    def _auth(self):
        """토큰 발급/갱신"""
        self._wait_rate_limit()
        url = f"{self.host}/oauth2/token"
        data = { 
            "grant_type": "client_credentials", 
            "appkey": self.app_key, 
            "appsecret": self.app_secret 
        }
        try:
            res = requests.post(url, headers={'Content-Type': 'application/json;charset=UTF-8'}, json=data)
            if res.status_code == 200:
                self.token = res.json().get("access_token")
                return True
            print(f"❌ [Auth Fail] {res.text}")
            return False
        except Exception as e:
            print(f"❌ [Network Error] {e}")
            return False

    def post(self, endpoint, data, api_id):
        """
        [공통 요청 함수]
        모든 API 요청은 이 함수를 통과함. 
        토큰이 없으면 알아서 받고, 헤더도 알아서 붙여줌.
        """
        if not self.token:
            if not self._auth(): return None

        self._wait_rate_limit()
        url = f"{self.host}{endpoint}"
        headers = {
            'Content-Type': 'application/json;charset=UTF-8',
            'authorization': f'Bearer {self.token}',
            'api-id': api_id
        }

        try:
            res = requests.post(url, headers=headers, json=data)
            # 토큰 만료시(401) 재발급 로직 추가 가능
            if res.status_code == 401:
                print("🔄 토큰 만료, 재발급 시도...")
                self._auth()
                headers['authorization'] = f'Bearer {self.token}'
                res = requests.post(url, headers=headers, json=data)
                
            return res
        except Exception as e:
            print(f"⚠️ API Request Error: {e}")
            return None
