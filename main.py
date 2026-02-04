# main.py
import os
import sys
from config.settings import Settings
from libs.auth import KiwoomAuth
from agents.commander import Commander # 사령관 클래스 임포트

def init_system():
    print("=========================================")
    print("   Kiwoom AI Trader V6.0 (One-Shot Sniper)    ")
    print("=========================================")

    # 1. 필수 폴더 생성
    for path in [Settings.LOG_DIR, Settings.JOURNAL_DIR]:
        if not os.path.exists(path):
            os.makedirs(path)

    # 2. 인증(로그인)
    auth = KiwoomAuth()
    if not auth.login():
        print("\n❌ [System] 접속 실패. 프로그램을 종료합니다.")
        return

    # ---------------------------------------------------------
    # 3. Commander AI 가동 (여기가 추가된 부분입니다!)
    # ---------------------------------------------------------
    print("\n🚀 [System] AI 전략 사령부(Commander) 가동...")
    
    commander = Commander()
    
    # (임시) 시장 데이터가 아직 없으므로 간단한 텍스트 전달
    # 나중에 여기에 뉴스 크롤링 데이터나 전일 지수 데이터를 넣습니다.
    dummy_market_info = "현재 나스닥 선물 약보합세. 변동성 다소 확대 예상."
    
    todays_strategy = commander.analyze_market(dummy_market_info)
    
    if todays_strategy:
        print("\n📜 [System] 오늘의 매매 규칙(Rulebook)이 확정되었습니다.")
        # 여기서 확정된 전략을 파일로 저장하거나 메모리에 올립니다.
        # save_strategy(todays_strategy) -> 추후 구현
    else:
        print("\n⚠️ [System] 전략 수립 실패. 보수적 기본 규칙을 적용합니다.")

if __name__ == "__main__":
    init_system()