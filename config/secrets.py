import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

class Secrets:
    """환경변수 매핑 및 검증"""
    TRADING_MODE = os.getenv("TRADING_MODE", "MOCK").upper()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    KIWOOM_APP_KEY = os.getenv("KIWOOM_APP_KEY")
    KIWOOM_APP_SECRET = os.getenv("KIWOOM_APP_SECRET")
    KIWOOM_ACCOUNT_NO = os.getenv("KIWOOM_ACCOUNT_NO")

    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            print("⚠️ [Warning] GEMINI_API_KEY가 없습니다.")
        if not cls.KIWOOM_ACCOUNT_NO:
            print("⚠️ [Warning] KIWOOM_ACCOUNT_NO가 없습니다.")
