import pandas as pd
import streamlit as st

hanshin = pd.read_pickle("hanshin.pickle")
ouka = pd.read_pickle("ouka.pickle")
satuki = pd.read_pickle("satuki.pickle")
nakayama = pd.read_pickle("nakayama.pickle")
tenharu = pd.read_pickle("tenharu.pickle")
tokyo = pd.read_pickle("tokyo.pickle")
oaks = pd.read_pickle("oaks.pickle")

#G1レース加工関数
@st.cache
def treatment(data):
    df = data.copy()
    df.drop(['着差', '調教師'], axis=1, inplace=True)
    df = df[~(df['着順'].astype(str).str.contains('\D'))]
    df['着順'] = df['着順'].astype(int)

    return df

#レース場データ加工関数
@st.cache
def processing(results):
    df = results.copy()
    # 着順の数字以外の文字列を取り除く
    df = df[~(df['着順'].astype(str).str.contains('\D'))]
    df['着順'] = df['着順'].astype(int)

    # 性と年齢に分割
    df['性'] = df['性齢'].map(lambda x: str(x)[0])
    df['年齢'] = df['性齢'].map(lambda x: str(x)[1:]).astype(int)

    # 馬体重と体重増減に分割
    df['馬体重'] = df['馬体重(増減)'].str.split('(', expand=True)[0].astype(int)
    df['体重増減'] = df['馬体重(増減)'].str.split('(', expand=True)[1].str[:-1].astype(int)

    # 不要な列を削除
    df.drop(['性齢', '馬体重(増減)', '着差', '後3F', 'コーナー通過順', '厩舎'], axis=1, inplace=True)

    return df

#競馬場関数

def job(name, datas):
    st.title(f"{name}　レース結果　2021年")
    test = processing(datas)
    top_3 = test[test['着順'] < 4]
    top = test[test['着順'] < 2]

    option = st.selectbox(
        f'{name}の上位3着の各情報',
        ('人気', '騎手', '枠番', '体重増減', '馬番')
    )
    if option == '人気':
        f"""上位3着の{option} """
        st.table(top_3['人気'].value_counts().head(8))
    elif option == '騎手':
        f"""上位3着の{option} """
        st.table(top_3['騎手'].value_counts().head(8))
    elif option == '枠番':
        f"""上位3着の{option} """
        st.table(top_3['枠'].value_counts().head(8))
    elif option == '体重増減':
        f"""上位3着の{option} """
        st.table(top_3['体重増減'].value_counts().head(8))
    elif option == '馬番':
        f"""上位3着の{option} """
        st.table(top_3['馬番'].value_counts().head(8))

    option = st.selectbox(
        f'{name}の1着の各情報',
        ('人気', '騎手', '枠番', '体重増減','馬番')
    )
    if option == '人気':
        f"""1着の{option} """
        st.table(top['人気'].value_counts().head(8))
    elif option == '騎手':
        f"""1着の{option} """
        st.table(top['騎手'].value_counts().head(8))
    elif option == '枠番':
        f"""1着の{option} """
        st.table(top['枠'].value_counts().head(8))
    elif option == '体重増減':
        f"""1着の{option} """
        st.table(top['体重増減'].value_counts().head(8))
    elif option == '馬番':
        f"""1着の{option} """
        st.table(top['馬番'].value_counts().head(8))

#Ｇ1レース関数

def g_one(name, data):
    df = treatment(data)
    rank3 = df[df['着順'] < 4]
    rank = df[df['着順'] < 2]

    options = st.selectbox(
        f'{name}の上位3着の傾向',
        ('人気','騎手','枠番','タイム','馬番')
    )
    if options == '人気':
        f""" ### 上位3着の{options}"""
        st.table(rank3['人気'].value_counts().head(10))
    elif options == '騎手':
        f""" ### 上位3着の{options}"""
        st.table(rank3['騎手'].value_counts().head(10))
    elif options == '枠番':
        f""" ### 上位3着の{options}"""
        st.table(rank3['枠番'].value_counts().head(10))
    elif options == 'タイム':
        f""" ### 上位3着の{options}"""
        st.table(rank3['タイム'].value_counts().head(10))
    elif options == '馬番':
        f""" ### 上位3着の{options}"""
        st.table(rank3['馬番'].value_counts().head(10))

    options = st.selectbox(
        f'{name}の1着の傾向',
        ('人気', '騎手', '枠番','タイム','馬番')
    )
    if options == '人気':
        f""" ### 1着の{options}"""
        st.table(rank['人気'].value_counts().head(10))
    elif options == '騎手':
        f""" ### 1着の{options}"""
        st.table(rank['騎手'].value_counts().head(10))
    elif options == '枠番':
        f""" ### 1着の{options}"""
        st.table(rank['枠番'].value_counts().head(10))
    elif options == 'タイム':
        f""" ### 1着の{options}"""
        st.table(rank['タイム'].value_counts().head(10))
    elif options == '馬番':
        f""" ### 1着の{options}"""
        st.table(rank['馬番'].value_counts().head(10))

# 画面出力
"""
# 過去のデータから上位3着の特徴を分析！
"""
st.sidebar.write("""
    # 競馬分析アプリ
    ## ・以下のオプションからデータを指定できます
    ### 競馬場
""")

#東京競馬場
if st.sidebar.checkbox("東京"):
    job("東京競馬場", tokyo)

#阪神競馬場
if st.sidebar.checkbox("阪神"):
    job("阪神競馬場",hanshin)

#中山競馬場
if st.sidebar.checkbox('中山'):
    job('中山競馬場',nakayama)

st.sidebar.write('### G1レース')

#桜花賞
if st.sidebar.checkbox('桜花賞'):
    g_one('桜花賞', ouka)

#皐月賞
if st.sidebar.checkbox('皐月賞'):
    g_one('皐月賞', satuki)

#天春
if st.sidebar.checkbox('天皇賞（春）'):
    g_one('天皇賞（春）', tenharu)

#優駿牝馬
if st.sidebar.checkbox('優駿牝馬(オークス)'):
    g_one('優駿牝馬(オークス)', oaks)
