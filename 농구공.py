import streamlit as st
import folium
from streamlit_folium import st_folium

# 1. 페이지 설정
st.set_page_config(
    page_title="슬램스팟 (SlamSpot) - 농구장 실시간 지도",
    page_icon="🏀",
    layout="wide"
)

# 커스텀 CSS (헤더 및 팝업 디자인)
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #E65100;
        margin-bottom: 5px;
    }
    .sub-title {
        text-align: center;
        color: #555;
        font-size: 1.1rem;
        margin-bottom: 25px;
    }
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 0.85rem;
    }
    .badge-large { background-color: #FFEBEE; color: #C62828; }
    .badge-medium { background-color: #FFF8E1; color: #F57F17; }
    .badge-small { background-color: #E8F5E9; color: #2E7D32; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🏀 슬램스팟 (SlamSpot)</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>실시간 농구장 혼잡도 지도 & 코트 상태 정보</p>", unsafe_allow_html=True)

# 2. 샘플 농구장 데이터베이스 (혼잡도: 대/중/소)
if 'courts_data' not in st.session_state:
    st.session_state.courts_data = [
        {
            "id": 1,
            "name": "올림픽공원 농구장",
            "lat": 37.516,
            "lng": 127.122,
            "crowd_level": "대",  # 대: 사람이 많음 (대형 농구공)
            "crowd_text": "🔴 혼잡 (웨이팅 있음)",
            "icon_size": 48,
            "travel_time": "대중교통 15분 / 도보 20분",
            "parking": "🚗 가능 (공영주차장 이용)",
            "court_count": "3개 코트",
            "floor_condition": "우레탄 (상태 양호, 일부 낡음)",
            "net_condition": "정품 그물 2개, 링 1개",
            "lighting": "야간 조명 22:00까지 점등",
            "image": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 2,
            "name": "반포한강공원 농구장",
            "lat": 37.510,
            "lng": 126.996,
            "crowd_level": "중",  # 중: 적당함 (중형 농구공)
            "crowd_text": "🟡 적당함 (바로 게임 가능)",
            "icon_size": 36,
            "travel_time": "대중교통 25분 / 차량 10분",
            "parking": "🚗 가능 (한강공원 주차장)",
            "court_count": "2개 코트",
            "floor_condition": "우레탄 (모래 약간 있음)",
            "net_condition": "철골 그물망 (튼튼함)",
            "lighting": "가로등 (약간 어두움)",
            "image": "https://images.unsplash.com/photo-1519766304817-4f37bda74a29?auto=format&fit=crop&w=800&q=80"
        },
        {
            "id": 3,
            "name": "성내유수지 체육공원 농구장",
            "lat": 37.528,
            "lng": 127.132,
            "crowd_level": "소",  # 소: 적음 (소형 농구공)
            "crowd_text": "🟢 여유 (한적함)",
            "icon_size": 24,
            "travel_time": "도보 8분",
            "parking": "❌ 불가 (주변 골목 주차 필요)",
            "court_count": "1개 코트",
            "floor_condition": "우레탄 (깔끔함)",
            "net_condition": "새 그물 교체 완료",
            "lighting": "자동 센서 조명 작동",
            "image": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?auto=format&fit=crop&w=800&q=80"
        }
    ]

# 3. 레이아웃 배치 (좌측: 지도 메인, 우측: 클릭한 농구장 상세정보)
col_map, col_detail = st.columns([1.8, 1.2])

# 농구공 아이콘 URL (투명 PNG)
BASKETBALL_ICON_URL = "https://cdn-icons-png.flaticon.com/512/889/889455.png"

with col_map:
    st.subheader("🗺️ 실시간 농구장 혼잡도 지도")
    st.caption("농구공 크기: 🔴 **대** (사람 많음) | 🟡 **중** (적당함) | 🟢 **소** (여유)")
    
    # 서울 중심 기준 지도의 초기 위치 생성
    m = folium.Map(location=[37.518, 127.0
