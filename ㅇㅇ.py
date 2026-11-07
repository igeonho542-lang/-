import random
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="포켓몬 가위바위보 게임",
    page_icon="✨",
    layout="centered"
)

# 흰색 배경, 핑크색 텍스트 및 핑크색 버튼 Custom CSS
st.markdown(
    """
    <style>
    /* 전체 배경색: 흰색 */
    .stApp {
        background-color: #FFFFFF;
    }
    
    /* 기본 텍스트 및 헤더: 핑크색 */
    h1, h2, h3, h4, h5, h6, p, div, span {
        color: #FF69B4 !important;
    }

    /* 가위, 바위, 보 버튼 스타일: 핑크색 배경, 흰색 글씨 */
    div.stButton > button {
        background-color: #FF69B4 !important;
        color: #FFFFFF !important;
        font-weight: bold !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 20px !important;
        font-size: 20px !important;
        width: 100% !important;
        box-shadow: 0 4px 6px rgba(255, 105, 180, 0.2);
    }
    
    /* 버튼 마우스 호버 효과 */
    div.stButton > button:hover {
        background-color: #FF1493 !important;
        color: #FFFFFF !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 타이틀 및 안내 문구
st.markdown("<h1 style='text-align: center;'>✨ 포켓몬 가위바위보 게임 ✨</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; margin-bottom: 30px;'>하나를 선택하세요</h3>", unsafe_allow_html=True)

# 컴퓨터 선택 미리 지정
options = ["가위 ✌️", "바위 ✊", "보 🖐️"]
computer_choice = random.choice(options)

# 버튼 3개를 1줄에 중앙 배치
col1, col2, col3 = st.columns(3)

user_choice = None

with col1:
    if st.button("가위 ✌️"):
        user_choice = "가위 ✌️"

with col2:
    if st.button("바위 ✊"):
        user_choice = "바위 ✊"

with col3:
    if st.button("보 🖐️"):
        user_choice = "보 🖐️"

# 결과 판정
if user_choice:
    st.write("---")
    st.markdown(f"<h4 style='text-align: center;'>나: {user_choice} VS 컴퓨터: {computer_choice}</h4>", unsafe_allow_html=True)
    
    if user_choice == computer_choice:
        st.markdown("<h2 style='text-align: center; color: #FFA500 !important;'>비겼습니다! 🤝</h2>", unsafe_allow_html=True)
    elif (
        (user_choice == "가위 ✌️" and computer_choice == "보 🖐️") or
        (user_choice == "바위 ✊" and computer_choice == "가위 ✌️") or
        (user_choice == "보 🖐️" and computer_choice == "바위 ✊")
    ):
        # 승리 시 32분의 1 확률 (약 3.125%)로 이로치 판정 (1부터 32 사이의 숫자를 뽑아 1이 나올 경우)
        is_shiny = random.randint(1, 32) == 1
        
        if is_shiny:
            st.balloons()
            st.markdown("<h2 style='text-align: center; color: #9400D3 !important;'>🌟 대박! 극희귀 ★이로치★ 포켓몬이 등장했다! 🌟</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center; font-weight: bold;'>축하합니다! 32분의 1의 확률을 뚫었습니다!</p>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='text-align: center;'>🎉 이겼습니다! 🎉</h2>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>야생의 포켓몬을 만났지만... 일반 색상이네요!</p>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #DC143C !important;'>졌습니다! 😢</h2>", unsafe_allow_html=True)
