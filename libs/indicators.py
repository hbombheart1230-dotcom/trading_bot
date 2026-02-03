import pandas as pd
import numpy as np

class TechnicalAnalyzer:
    """
    [Calculation Layer]
    역할: DataFrame을 받아 지표(RSI, MACD, MA) 계산
    """
    
    @staticmethod
    def calc_rsi(df, period=14):
        """RSI 계산"""
        if df is None or len(df) < period: return 50.0
        
        # 데이터 전처리 (문자열 -> 숫자)
        close = df['stck_prpr'].astype(float)
        
        delta = close.diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        # 최신 값 반환
        return round(rsi.iloc[0], 2) if not pd.isna(rsi.iloc[0]) else 50.0

    @staticmethod
    def calc_ma(df, window=20):
        """이동평균선 계산"""
        if df is None or len(df) < window: return 0
        close = df['stck_prpr'].astype(float)
        ma = close.rolling(window=window).mean()
        return int(ma.iloc[0])
