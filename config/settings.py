import os

class Settings:
    """시스템 고정 설정"""
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 메모리(로그) 경로
    LOG_DIR = os.path.join(BASE_DIR, "memory", "logs")
    JOURNAL_DIR = os.path.join(BASE_DIR, "memory", "journals")
    
    # 모델 설정
    MODEL_FAST = "gemini-3-flash-preview"
    MODEL_SMART = "gemini-3-flash-preview"

    # 🌟 [NEW] 키움 API 접속 주소 (여기에 정의)
    KIWOOM_URL_REAL = "https://api.kiwoom.com"    # 실전
    KIWOOM_URL_MOCK = "https://mockapi.kiwoom.com" # 모의(VTS)