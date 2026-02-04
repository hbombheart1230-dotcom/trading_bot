import requests
import json
from config.secrets import Secrets
from config.settings import Settings

class KiwoomAuth:
    """
    키움증권 REST API 인증 관리자
    [공식 문서 au10001 + 실전 로그 기반 수정]
    """
    def __init__(self):
        self.is_connected = False
        self.mode = Secrets.TRADING_MODE.upper()
        self.account = Secrets.KIWOOM_ACCOUNT_NO
        self.access_token = None
        
        # 도메인 설정
        if self.mode == "REAL":
            self.base_url = Settings.KIWOOM_URL_REAL
        else:
            self.base_url = Settings.KIWOOM_URL_MOCK
            print("🧪 [Auth] 모의 투자(mockapi) 서버로 설정되었습니다.")

    def login(self):
        print(f"🔑 [Auth] 서버 접속 시도... (Mode: {self.mode})")
        Secrets.validate()
        return self._issue_token()

    def _issue_token(self):
        """
        토큰 발급 (au10001)
        """
        endpoint = "/oauth2/token"
        url = f"{self.base_url}{endpoint}"
        
        headers = {
            "Content-Type": "application/json;charset=UTF-8"
        }
        
        data = {
            "grant_type": "client_credentials",
            "appkey": Secrets.KIWOOM_APP_KEY,
            "secretkey": Secrets.KIWOOM_APP_SECRET
        }

        try:
            print(f"📡 [Network] 토큰 요청 중... ({url})")
            
            response = requests.post(url, headers=headers, data=json.dumps(data))
            
            print(f"   - Status Code: {response.status_code}")

            if response.status_code == 200:
                res_data = response.json()
                
                # 🌟 [수정 포인트] 응답 키가 'access_token'이 아니라 'token'임!
                self.access_token = res_data.get('access_token') or res_data.get('token')
                
                if self.access_token:
                    print(f"✅ [Auth] 접속 성공!")
                    # 보안상 앞 10자리만 출력
                    print(f"   - 토큰: {self.access_token[:10]}... (발급됨)")
                    
                    # 만료 시간 확인 (expires_in 또는 expires_dt)
                    expires = res_data.get('expires_in') or res_data.get('expires_dt')
                    print(f"   - 유효기간: {expires}")
                    
                    self.is_connected = True
                    return True
                else:
                    print("❌ [Auth] 토큰 키를 찾을 수 없습니다.")
                    print(f"   - 응답 데이터: {res_data}")
                    return False
            else:
                print(f"❌ [Auth] 접속 실패")
                print(f"   - 응답: {response.text}")
                return False

        except Exception as e:
            print(f"❌ [Auth] 연결 오류: {e}")
            return False

    def get_token(self):
        return self.access_token