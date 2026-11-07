import streamlit as st
import random
import time

# -----------------------------------------------------------------------------
# 1. 페이지 설정 & CSS 스타일
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="포켓몬 가차! (Pokémon Gacha)",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Arcade & Pokemon styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Noto+Sans+KR:wght@400;700;900&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #1a1c29 0%, #0d0e15 100%);
        color: #ffffff;
        font-family: 'Noto Sans KR', sans-serif;
    }

    /* Gacha Title Header */
    .gacha-header {
        text-align: center;
        background: linear-gradient(90deg, #ff4b4b, #ff8c00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-family: 'Press Start 2P', cursive, sans-serif;
        font-size: 2.2rem;
        margin-bottom: 5px;
        text-shadow: 0px 4px 10px rgba(255, 75, 75, 0.3);
    }
    
    .sub-header {
        text-align: center;
        color: #a0aec0;
        font-size: 1rem;
        margin-bottom: 25px;
    }

    /* Currency Box */
    .currency-card {
        background: rgba(255, 255, 255, 0.05);
        border: 2px solid rgba(255, 215, 0, 0.3);
        border-radius: 16px;
        padding: 12px 20px;
        display: flex;
        align-items: center;
        justify-content: space-around;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        backdrop-filter: blur(4px);
    }

    /* Cards & Pokemon Items */
    .poke-card {
        background: #252836;
        border-radius: 16px;
        padding: 15px;
        text-align: center;
        border: 2px solid #3b3e52;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        overflow: hidden;
    }
    .poke-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
    }

    /* Rarity Badges */
    .badge-c { background-color: #9e9e9e; color: #fff; }
    .badge-r { background-color: #2196f3; color: #fff; }
    .badge-sr { background-color: #9c27b0; color: #fff; }
    .badge-ur { background-color: #ff9800; color: #fff; }
    .badge-ssr { 
        background: linear-gradient(45deg, #ff0055, #7a00ff); 
        color: #fff; 
        font-weight: bold;
        box-shadow: 0 0 10px rgba(255, 0, 85, 0.6);
    }

    .rarity-pill {
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        display: inline-block;
        margin-top: 5px;
    }

    .shiny-pill {
        background: linear-gradient(45deg, #ffd700, #fff);
        color: #000;
        font-weight: bold;
        font-size: 0.7rem;
        padding: 2px 8px;
        border-radius: 10px;
        margin-left: 4px;
    }

    /* Result Animation Card */
    .draw-result-card {
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        margin: 10px 0;
        animation: popIn 0.4s ease-out forwards;
    }

    @keyframes popIn {
        0% { transform: scale(0.5); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }

    /* Pokemon Image Container */
    .poke-img-box {
        height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .poke-img-box img {
        max-height: 110px;
        max-width: 110px;
        filter: drop-shadow(0 5px 8px rgba(0,0,0,0.5));
    }
    .poke-img-uncollected {
        filter: brightness(0) opacity(0.3) !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. 포켓몬 마스터 데이터 베이스
# -----------------------------------------------------------------------------
# 공식 아트워크 URL 베이스
ARTWORK_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork"
SHINY_URL = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny"

POKEMON_DB = [
    # C (Common) - 40% 확률
    {"id": 1, "name": "이상해씨", "rarity": "C", "type": "풀/독", "hp": 45, "atk": 49},
    {"id": 4, "name": "파이리", "rarity": "C", "type": "불꽃", "hp": 39, "atk": 52},
    {"id": 7, "name": "꼬부기", "rarity": "C", "type": "물", "hp": 44, "atk": 48},
    {"id": 10, "name": "캐터피", "rarity": "C", "type": "벌레", "hp": 45, "atk": 30},
    {"id": 16, "name": "구구", "rarity": "C", "type": "노말/비행", "hp": 40, "atk": 45},
    {"id": 19, "name": "꼬렛", "rarity": "C", "type": "노말", "hp": 30, "atk": 56},
    {"id": 133, "name": "이브이", "rarity": "C", "type": "노말", "hp": 55, "atk": 55},
    {"id": 39, "name": "푸린", "rarity": "C", "type": "노말/페어리", "hp": 115, "atk": 45},

    # R (Rare) - 35% 확률
    {"id": 25, "name": "피카츄", "rarity": "R", "type": "전기", "hp": 35, "atk": 55},
    {"id": 54, "name": "고라파덕", "rarity": "R", "type": "물", "hp": 50, "atk": 52},
    {"id": 63, "name": "캐이시", "rarity": "R", "type": "에스퍼", "hp": 25, "atk": 20},
    {"id": 143, "name": "잠만보", "rarity": "R", "type": "노말", "hp": 160, "atk": 110},
    {"id": 79, "name": "야돈", "rarity": "R", "type": "물/에스퍼", "hp": 90, "atk": 65},
    {"id": 129, "name": "잉어킹", "rarity": "R", "type": "물", "hp": 20, "atk": 10},

    # SR (Super Rare) - 15% 확률
    {"id": 6, "name": "리자몽", "rarity": "SR", "type": "불꽃/비행", "hp": 78, "atk": 84},
    {"id": 9, "name": "거북왕", "rarity": "SR", "type": "물", "hp": 79, "atk": 83},
    {"id": 3, "name": "이상해꽃", "rarity": "SR", "type": "풀/독", "hp": 80, "atk": 82},
    {"id": 94, "name": "팬텀", "rarity": "SR", "type": "고스트/독", "hp": 60, "atk": 65},
    {"id": 149, "name": "망나뇽", "rarity": "SR", "type": "드래곤/비행", "hp": 91, "atk": 134},
    {"id": 448, "name": "루카리오", "rarity": "SR", "type": "격투/강철", "hp": 70, "atk": 110},

    # UR (Ultra Rare) - 8% 확률
    {"id": 658, "name": "개굴닌자", "rarity": "UR", "type": "물/악", "hp": 72, "atk": 95},
    {"id": 130, "name": "갸라도스", "rarity": "UR", "type": "물/비행", "hp": 95, "atk": 125},
    {"id": 248, "name": "마기라스", "rarity": "UR", "type": "바위/악", "hp": 100, "atk": 134},
    {"id": 376, "name": "메타그로스", "rarity": "UR", "type": "강철/에스퍼", "hp": 80, "atk": 135},

    # SSR (Legendary/Mythic) - 2% 확률
    {"id": 150, "name": "뮤츠", "rarity": "SSR", "type": "에스퍼", "hp": 106, "atk": 110},
    {"id": 151, "name": "뮤", "rarity": "SSR", "type": "에스퍼", "hp": 100, "atk": 100},
    {"id": 384, "name": "레쿠쟈", "rarity": "SSR", "type": "드래곤/비행", "hp": 105, "atk": 150},
    {"id": 493, "name": "아르세우스", "rarity": "SSR", "type": "노말", "hp": 120, "atk": 120},
]

RARITY_PROBS = {
    "C": 0.40,
    "R": 0.35,
    "SR": 0.15,
    "UR": 0.08,
    "SSR": 0.02
}

SHINY_CHANCE = 0.05  # 이로치(Shiny) 등장 확률 5%

# -----------------------------------------------------------------------------
# 3. 세션 상태 초기화 (LocalStorage 역할)
# -----------------------------------------------------------------------------
if 'coins' not in st.session_state:
    st.session_state.coins = 1000
if 'total_draws' not in st.session_state:
    st.session_state.total_draws = 0
if 'pity_count' not in st.session_state:
    st.session_state.pity_count = 0  # 50연차 천장 시스템
if 'inventory' not in st.session_state:
    # {poke_id: {"count": 0, "shiny_count": 0, "first_caught": None}}
    st.session_state.inventory = {p["id"]: {"count": 0, "shiny_count": 0} for p in POKEMON_DB}
if 'last_draw_results' not in st.session_state:
    st.session_state.last_draw_results = []

# -----------------------------------------------------------------------------
# 4. 헬퍼 함수
# -----------------------------------------------------------------------------
def get_pokemon_by_rarity(rarity):
    return [p for p in POKEMON_DB if p["rarity"] == rarity]

def draw_single():
    """단일 가차 로직"""
    st.session_state.coins -= 100
    st.session_state.total_draws += 1
    st.session_state.pity_count += 1

    # 50연차 천장 (SSR 확정)
    if st.session_state.pity_count >= 50:
        chosen_rarity = "SSR"
        st.session_state.pity_count = 0
    else:
        # 확률 기반 등급 선택
        rarities = list(RARITY_PROBS.keys())
        weights = list(RARITY_PROBS.values())
        chosen_rarity = random.choices(rarities, weights=weights, k=1)[0]
        if chosen_rarity == "SSR":
            st.session_state.pity_count = 0

    # 해당 등급의 포켓몬 중 무작위 선택
    candidates = get_pokemon_by_rarity(chosen_rarity)
    drawn_poke = dict(random.choice(candidates))

    # 이로치 여부 판정
    is_shiny = random.random() < SHINY_CHANCE
    drawn_poke["is_shiny"] = is_shiny

    # 인벤토리 업데이트
    poke_id = drawn_poke["id"]
    if is_shiny:
        st.session_state.inventory[poke_id]["shiny_count"] += 1
    st.session_state.inventory[poke_id]["count"] += 1

    return drawn_poke

def trigger_confetti():
    """SSR 등장 시 축하 대포 효과"""
    st.components.v1.html(
        """
        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.5.1/dist/confetti.browser.min.js"></script>
        <script>
            confetti({
                particleCount: 120,
                spread: 100,
                origin: { y: 0.6 }
            });
        </script>
        """,
        height=0
    )

# -----------------------------------------------------------------------------
# 5. UI Layout - 사이드바
# -----------------------------------------------------------------------------
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/9/98/International_Pok%C3%A9mon_logo.svg", width=220)
    st.markdown("### 🎮 컨트롤 패널")

    # 충전 / 코인 리셋
    if st.button("🪙 포켓코인 1,000개 충전", use_container_width=True):
        st.session_state.coins += 1000
        st.toast("코인이 1,000개 충전되었습니다!", icon="💰")

    if st.button("🔄 데이터 초기화", use_container_width=True):
        st.session_state.coins = 1000
        st.session_state.total_draws = 0
        st.session_state.pity_count = 0
        st.session_state.inventory = {p["id"]: {"count": 0, "shiny_count": 0} for p in POKEMON_DB}
        st.session_state.last_draw_results = []
        st.toast("게임 데이터가 초기화되었습니다.", icon="🧹")

    st.markdown("---")
    st.markdown("### 📊 뽑기 확률 정보")
    st.markdown("""
    - **C (Common):** 40%
    - **R (Rare):** 35%
    - **SR (Super Rare):** 15%
    - **UR (Ultra Rare):** 8%
    - **SSR (Legendary):** 2%
    - **✨ 이로치(Shiny):** 모든 뽑기 시 5%
    """)
    st.info("💡 **천장 시스템**: 50회 동안 SSR이 나오지 않으면 50번째에 SSR이 100% 확정 등장합니다!")

# -----------------------------------------------------------------------------
# 6. 메인 UI - 상단 스탯 영역
# -----------------------------------------------------------------------------
st.markdown('<div class="gacha-header">POKÉMON GACHA</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">당신만의 전설 포켓몬을 수집해보세요!</div>', unsafe_allow_html=True)

# 통계 및 수집률 계산
total_species = len(POKEMON_DB)
collected_species = sum(1 for v in st.session_state.inventory.values() if v["count"] > 0)
completion_rate = (collected_species / total_species) * 100

st.markdown(f"""
    <div class="currency-card">
        <div>💰 <b>보유 코인:</b> <span style="color:#ffd700; font-size:1.3rem;">{st.session_state.coins:,}</span> P</div>
        <div>🔮 <b>총 뽑기 횟수:</b> {st.session_state.total_draws}회</div>
        <div>🎯 <b>SSR 천장 카운트:</b> {st.session_state.pity_count}/50</div>
        <div>📖 <b>도감 수집률:</b> {collected_species}/{total_species} ({completion_rate:.1f}%)</div>
    </div>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 7. 메인 UI - 탭 구성 (가차 화면 & 도감 화면)
# -----------------------------------------------------------------------------
tab_gacha, tab_pokedex = st.tabs(["🎰 가차 뽑기 (Gacha)", "📚 포켓몬 도감 (Pokédex)"])

# =============================================================================
# TAB 1: 가차 뽑기
# =============================================================================
with tab_gacha:
    st.write("")
    col_btn1, col_btn2 = st.columns(2)

    with col_btn1:
        btn_1x = st.button("🎁 1회 뽑기 (100 P)", use_container_width=True, type="primary")
    with col_btn2:
        btn_10x = st.button("🔥 10회 연쇄 뽑기 (1,000 P)", use_container_width=True, type="secondary")

    # 뽑기 액션 처리
    results = []
    if btn_1x:
        if st.session_state.coins >= 100:
            with st.spinner("몬스터볼을 던지는 중... ⚡"):
                time.sleep(0.5)
                results.append(draw_single())
                st.session_state.last_draw_results = results
        else:
            st.error("코인이 부족합니다! 사이드바에서 코인을 충전해주세요.")

    elif btn_10x:
        if st.session_state.coins >= 1000:
            with st.spinner("몬스터볼 10개를 잇따라 던지는 중... 🔥⚡"):
                time.sleep(0.8)
                for _ in range(10):
                    results.append(draw_single())
                st.session_state.last_draw_results = results
        else:
            st.error("코인이 부족합니다! 10회 뽑기에는 1,000 P가 필요합니다.")

    # 결과 출력
    if st.session_state.last_draw_results:
        st.markdown("### 🎉 최근 뽑기 결과")
        
        # SSR 포함 여부 확인 -> 폭죽 효과
        has_ssr = any(p["rarity"] == "SSR" for p in st.session_state.last_draw_results)
        if has_ssr:
            trigger_confetti()
            st.balloons()

        res_cols = st.columns(min(len(st.session_state.last_draw_results), 5))
        for idx, poke in enumerate(st.session_state.last_draw_results):
            col_target = res_cols[idx % 5]
            
            img_url = SHINY_URL if poke["is_shiny"] else ARTWORK_URL
            img_src = f"{img_url}/{poke['id']}.png"
            rarity_class = f"badge-{poke['rarity'].lower()}"

            with col_target:
                st.markdown(f"""
                    <div class="poke-card draw-result-card">
                        <div style="font-size: 0.8rem; color:#aaa;">No.{poke['id']:03d}</div>
                        <div class="poke-img-box">
                            <img src="{img_src}" alt="{poke['name']}">
                        </div>
                        <div style="font-weight: bold; margin-top: 8px;">{poke['name']}</div>
                        <div>
                            <span class="rarity-pill {rarity_class}">{poke['rarity']}</span>
                            {"<span class='shiny-pill'>✨ Shiny</span>" if poke["is_shiny"] else ""}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                st.write("")

# =============================================================================
# TAB 2: 포켓몬 도감 (Pokédex)
# =============================================================================
with tab_pokedex:
    st.markdown("### 📖 나만의 도감 목록")

    # 필터 옵션
    f_col1, f_col2 = st.columns([2, 2])
    with f_col1:
        filter_rarity = st.multiselect("등급 필터", ["C", "R", "SR", "UR", "SSR"], default=["C", "R", "SR", "UR", "SSR"])
    with f_col2:
        filter_status = st.radio("획득 여부", ["전체 보기", "획득한 포켓몬만", "미획득만"], horizontal=True)

    st.markdown("---")

    # 그리드 배치를 위한 컬럼 세팅
    grid_cols = st.columns(4)

    filtered_pokemon = [p for p in POKEMON_DB if p["rarity"] in filter_rarity]

    for idx, poke in enumerate(filtered_pokemon):
        inv_data = st.session_state.inventory[poke["id"]]
        is_caught = inv_data["count"] > 0
        has_shiny = inv_data["shiny_count"] > 0

        # 필터링 조건
        if filter_status == "획득한 포켓몬만" and not is_caught:
            continue
        if filter_status == "미획득만" and is_caught:
            continue

        col_target = grid_cols[idx % 4]

        # 이미지 선택 (이로치를 획득했으면 기본을 이로치로 보여주는 센스)
        img_url = SHINY_URL if has_shiny else ARTWORK_URL
        img_src = f"{img_url}/{poke['id']}.png"
        rarity_class = f"badge-{poke['rarity'].lower()}"
        img_class = "" if is_caught else "poke-img-uncollected"

        with col_target:
            st.markdown(f"""
                <div class="poke-card">
                    <div style="font-size: 0.8rem; color:#aaa;">No.{poke['id']:03d}</div>
                    <div class="poke-img-box">
                        <img src="{img_src}" class="{img_class}" alt="{poke['name']}">
                    </div>
                    <div style="font-weight: bold; margin-top: 8px; font-size:1.1rem;">
                        {poke['name'] if is_caught else "???"}
                    </div>
                    <div>
                        <span class="rarity-pill {rarity_class}">{poke['rarity']}</span>
                        {"<span class='shiny-pill'>✨ Shiny</span>" if has_shiny else ""}
                    </div>
                    <div style="font-size:0.8rem; color:#888; margin-top:6px;">
                        {f"보유 수량: <b>{inv_data['count']}</b>개" if is_caught else "미획득"}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # 상세 정보 모달 역할의 Expander
            if is_caught:
                with st.expander("상세 능력치 보기"):
                    st.write(f"**속성:** {poke['type']}")
                    st.write(f"**체력 (HP):** {poke['hp']}")
                    st.write(f"**공격력:** {poke['atk']}")
                    st.write(f"**✨ 이로치 보유:** {inv_data['shiny_count']}개")
            st.write("")
