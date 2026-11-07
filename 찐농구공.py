import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

# ---------------------------------------------------------
# 1. 페이지 및 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="울트라슈퍼레전드김윤후농구장",
    page_icon="🏀",
    layout="wide"
)

st.title("🏀 울트라슈퍼레전드김윤후농구장")
st.caption("내 주변 농구장 찾기 및 실시간 코트 혼잡도/상태 정보")

# ---------------------------------------------------------
# 2. 더미 데이터 (실제 서비스 개발 시 DB 연동 부분)
# ---------------------------------------------------------
# 농구공 혼잡도 크기 정의 (대/중/소 픽셀 크기)
CROWD_SIZES = {
    "대 (혼잡)": {"size": 45, "color": "#d9534f", "label": "🔥 많음"},
    "중 (보통)": {"size": 32, "color": "#f0ad4e", "label": "👌 보통"},
    "소 (여유)": {"size": 20, "color": "#5cb85c", "label": "🍃 적음"}
}

COURT_DATA = [
    {
        "id": 1,
        "name": "반포 한강공원 농구장",
        "lat": 37.5090,
        "lng": 127.0010,
        "distance": "0.8km",
        "crowd": "대 (혼잡)",
        "court_count": 3,
        "floor_status": "우레탄 (양호)",
        "net_status": "그물망 있음 🕸️",
        "parking": "가능 (한강공원 주차장 이용)",
        "travel_time": "도보 10분 / 차로 3분",
        "img_url": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=600&q=80"
    },
    {
        "id": 2,
        "name": "보라매공원 농구장",
        "lat": 37.4935,
        "lng": 126.9190,
        "distance": "1.5km",
        "crowd": "중 (보통)",
        "court_count": 2,
        "floor_status": "아스팔트 (약간 훼손)",
        "net_status": "그물망 없음 ❌",
        "parking": "불가 (공영주차장 도보 5분)",
        "travel_time": "도보 18분 / 차로 5분",
        "img_url": "https://images.unsplash.com/photo-1519861531473-9200262188bf?w=600&q=80"
    },
    {
        "id": 3,
        "name": "여의도공원 농구코트",
        "lat": 37.5270,
        "lng": 126.9170,
        "distance": "1.9km",
        "crowd": "소 (여유)",
        "court_count": 4,
        "floor_status": "고급 아크릴 코트 (최상)",
        "net_status": "철망 그물망 완료 🏀",
        "parking": "가능 (여의도공원 주차장)",
        "travel_time": "도보 22분 / 차로 7분",
        "img_url": "https://images.unsplash.com/photo-1574629810360-7efbbe195018?w=600&q=80"
    }
]

df_courts = pd.DataFrame(COURT_DATA)

# ---------------------------------------------------------
# 3. 사이드바 - 지역 검색 및 반경 필터
# ---------------------------------------------------------
st.sidebar.header("📍 내 위치 설정 및 필터")
region = st.sidebar.selectbox("사는 지역 선택", ["서울특별시 서초구", "서울특별시 동작구", "서울특별시 영등포구"])
radius = st.sidebar.radio("검색 반경 선택", ["1km 이내", "2km 이내"], index=1)

st.sidebar.markdown("---")
st.sidebar.subheader("🏀 혼잡도 범주")
for level, info in CROWD_SIZES.items():
    st.sidebar.write(f"**{level}**: 농구공 마커 크기 {info['size']}px ({info['label']})")

# ---------------------------------------------------------
# 4. 지도 렌더링 (시작 화면)
# ---------------------------------------------------------
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🗺️ 실시간 농구장 지도")
    st.info("💡 농구공 아이콘 크기: **대 (혼잡)** | **중 (보통)** | **소 (여유)** — 마커를 누르면 상세정보가 뜹니다!")

    # 서울 중심 기준 지도
    m = folium.Map(location=[37.5120, 126.9400], zoom_start=13, tiles="OpenStreetMap")

    # 농구장 마커 추가 (농구공 커스텀 아이콘 적용)
    for _, court in df_courts.iterrows():
        crowd_info = CROWD_SIZES[court["crowd"]]
        icon_size = crowd_info["size"]

        # 농구공 SVG/PNG 이미지 마커
        icon = folium.CustomIcon(
            icon_image="https://cdn-icons-png.flaticon.com/512/889/889455.png",
            icon_size=(icon_size, icon_size)
        )

        # 팝업 HTML 작성
        popup_html = f"""
        <div style="width:160px;">
            <b>{court['name']}</b><br>
            혼잡도: {court['crowd']}<br>
            코트 개수: {court['court_count']}개
        </div>
        """

        folium.Marker(
            location=[court["lat"], court["lng"]],
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"{court['name']} ({court['crowd']})",
            icon=icon
        ).add_to(m)

    # 지도 출력 및 클릭 이벤트 수신
    map_data = st_folium(m, width="100%", height=500)

# ---------------------------------------------------------
# 5. 농구장 선택 시 상세 정보 표시
# ---------------------------------------------------------
with col2:
    st.subheader("📋 농구장 상세 정보")
