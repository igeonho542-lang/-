import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="자시안 등장!",
    page_icon="⚔️",
    layout="centered"
)

# 흰색 배경, 핑크색 글씨, 흰색 버튼을 위한 Custom CSS 적용
st.markdown(
    """
    <style>
    /* 전체 배경색 지정: 흰색 */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 기본 텍스트 및 헤더 핑크색 지정 */
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #FF69B4 !important;
    }

    /* 버튼 스타일 커스텀: 하얀색 배경, 핑크색 글씨, 깔끔한 테두리 */
    div.stButton > button {
        background-color: #FFFFFF !important;
        color: #FF69B4 !important;
        font-weight: bold !important;
        border: 2px solid #FF69B4 !important;
        border-radius: 10px !important;
        padding: 12px 28px !important;
        font-size: 18px !important;
        width: 100% !important;
        box-shadow: 0px 2px 5px rgba(0,0,0,0.05);
    }
    
    /* 버튼에 마우스 올렸을 때 효과 */
    div.stButton > button:hover {
        background-color: #FFF0F5 !important;
        color: #FF1493 !important;
        border-color: #FF1493 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 타이틀 안내
st.title("✨ 웹앱에 오신 것을 환영합니다")

# 버튼 중앙 배치를 위한 컬럼 구성
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    clicked = st.button("들어가기")

if clicked:
    # 폭죽 애니메이션 연출
    st.balloons()
    
    # 이벤트 문구 출력
    st.markdown("<h2 style='text-align: center; margin-top: 30px;'>⚔️ 야생에 자시안이 등장했다! ⚔️</h2>", unsafe_allow_html=True)
