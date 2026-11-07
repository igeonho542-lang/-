import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="환영합니다!",
    page_icon="🎉",
    layout="centered"
)

# 검은색 배경과 핑크색 글씨를 위한 Custom CSS 적용
st.markdown(
    """
    <style>
    /* 전체 배경색 지정 */
    .stApp {
        background-color: #0E1117;
    }
    
    /* 기본 텍스트 및 헤더 핑크색 지정 */
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #FF69B4 !important;
    }

    /* 버튼 스타일 커스텀 */
    div.stButton > button {
        background-color: #FF69B4 !important;
        color: #0E1117 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 24px !important;
        font-size: 18px !important;
    }
    
    div.stButton > button:hover {
        background-color: #FF1493 !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 타이틀 안내
st.title("✨ 웹앱에 오신 것을 환영합니다")

# '들어가기' 버튼 및 폭죽 효과 구현
if st.button("들어가기"):
    # Streamlit 내장 축하/풍선 효과 (폭죽 느낌 연출)
    st.balloons()
    
    # 환영 문구 출력
    st.header("💖 환영합니다! 💖")
    st.write("성공적으로 입장하셨습니다.")
