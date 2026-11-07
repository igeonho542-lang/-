import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="환영합니다!",
    page_icon="🎉",
    layout="centered"
)

# 검은색 배경, 핑크색 글씨 및 중앙 정렬을 위한 Custom CSS 적용
st.markdown(
    """
    <style>
    /* 전체 배경색 지정 */
    .stApp {
        background-color: #0E1117;
    }
    
    /* 기본 텍스트 및 헤더 핑크색 지정 */
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #FFB6C1 !important;
    }

    /* 버튼 스타일 커스텀: 연한 핑크색 배경(#FFC0CB), 진한 핑크색 글씨(#C71585) */
    div.stButton > button {
        background-color: #FFC0CB !important;
        color: #C71585 !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 12px 28px !important;
        font-size: 18px !important;
        width: 100% !important;
    }
    
    div.stButton > button:hover {
        background-color: #FFB6C1 !important;
        color: #8B008B !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 타이틀 안내
st.title("✨ 웹앱에 오신 것을 환영합니다")

# 빈 공간을 만들어 버튼을 중앙에 배치
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    # '들어가기' 버튼 및 폭죽 효과 구현
    clicked = st.button("들어가기")

if clicked:
    # Streamlit 내장 축하/풍선 효과
    st.balloons()
    
    # 환영 문구 출력 (중앙 정렬 효과를 위해 markdown 활용 가능)
    st.markdown("<h2 style='text-align: center;'>💖 환영합니다! 💖</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>성공적으로 입장하셨습니다.</p>", unsafe_allow_html=True)
