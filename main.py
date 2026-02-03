from agents.bot import app
import time
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

if __name__ == "__main__":
    # 타겟 설정 (삼성전자)
    TARGET = "005930"
    
    print("=========================================")
    print("🔥 Kiwoom AI Scalper V1.0 (Basic)")
    print(f"🎯 Target: {TARGET}")
    print("=========================================")
    
    try:
        while True:
            # 에이전트 실행
            app.invoke({"ticker": TARGET})
            
            # 5초 대기 (API 속도 제한 고려)
            print("💤 ...waiting 5s...")
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n🛑 시스템을 안전하게 종료합니다.")
