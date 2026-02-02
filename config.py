import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    KIWOOM_APP_KEY = os.getenv("KIWOOM_APP_KEY")
    KIWOOM_SECRET_KEY = os.getenv("KIWOOM_SECRET_KEY")
    ACCOUNT_NO = os.getenv("KIWOOM_ACCOUNT_NO")
    
    # 모의투자 서버 설정
    BASE_URL = "https://mockapi.kiwoom.com"
    MODE = "mock"
