import pandas as pd

def bollinger_bands(f_df, ma=20, k=2):
    f_name = 'ma' + str(ma)
    f_df[f_name] = f_df['close'].rolling(window=ma, center=False).mean()
    f_df['std20'] = f_df['close'].rolling(window=ma).std(ddof=0)
    f_df['bb_high'] = f_df[f_name] + f_df['std20']*k
    f_df['bb_low'] = f_df[f_name] - f_df['std20']*k
    f_df.dropna(inplace=True)
    return f_df

def moving_average(df, ma_num):
    name = 'ma' + str(ma_num)
    df[name] = df['close'].rolling(ma_num).mean()
    return df

def disparity(df, ma_num):
    name = 'ma' + str(ma_num)
    df[name] = moving_average(df, ma_num)
    df['disparity'] = df['close'] / df[name]
    return df

def rsi(df, feature, length):
    delta = df[feature].diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    _gain = up.ewm(com=(length - 1), min_periods=length).mean()
    _loss = down.abs().ewm(com=(length - 1), min_periods=length).mean()
    RS = _gain / _loss
    df['rsi'] = 100 - (100 / (1 + RS))
    return df

def fnMACD(m_Df, featrue, m_NumFast=12, m_NumSlow=26, m_NumSignal=9):
    m_Df['EMAFast'] = m_Df[featrue].ewm( span = m_NumFast, min_periods = m_NumFast - 1).mean()
    m_Df['EMASlow'] = m_Df[featrue].ewm( span = m_NumSlow, min_periods = m_NumSlow - 1).mean()
    m_Df['MACD'] = m_Df['EMAFast'] - m_Df['EMASlow']
    m_Df['MACDSignal'] = m_Df['MACD'].ewm( span = m_NumSignal, min_periods = m_NumSignal-1).mean()
    m_Df['MACDDiff'] = m_Df['MACD'] - m_Df['MACDSignal']
    return m_Df
