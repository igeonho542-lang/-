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

# 속성 상성표 (공격 타입 -> 방어 타입 배율)
TYPE_CHART = {
    "불꽃": {"풀": 2.0, "물": 0.5, "불꽃": 0.5, "바위": 0.5, "강철": 2.0},
    "물": {"불꽃": 2.0, "풀": 0.5, "물": 0.5, "바위": 2.0, "드래곤": 0.5},
    "풀": {"물": 2.0, "불꽃": 0.5, "풀": 0.5, "독": 0.5, "비행": 0.5, "바위": 2.0, "강철": 0.5},
    "전기": {"물": 2.0, "비행": 2.0, "전기": 0.5, "풀": 0.5, "드래곤": 0.5},
    "에스퍼": {"격투": 2.0, "독": 2.0, "에스퍼": 0.5, "악": 0.0},
    "고스트": {"에스퍼": 2.0, "고스트": 2.0, "악": 0.5, "노말": 0.0},
    "드래곤": {"드래곤": 2.0, "강철": 0.5},
    "격투": {"노말": 2.0, "바위": 2.0, "강철": 2.0, "악": 2.0, "비행": 0.5, "독": 0.5, "에스퍼": 0.5},
    "악": {"에스퍼": 2.0, "고스트": 2.0, "격투": 0.5, "악": 0.5},
    "강철": {"바위": 2.0, "불꽃": 0.5, "물": 0.5, "전기": 0.5, "강철": 0.5},
    "노말": {"바위": 0.5, "고스트": 0.0, "강철": 0.5},
}

POKEMON_DB = [
    # C (Common) - 40% 확률
    {"id": 1, "name": "이상해씨", "rarity": "C", "type": "풀", "hp": 120, "atk": 49, "skills": ["몸통박치기", "덩굴채찍"]},
    {"id": 4, "name": "파이리", "rarity": "C", "type": "불꽃", "hp": 110, "atk": 52, "skills": ["할퀴기", "불꽃세례"]},
    {"id": 7, "name": "꼬부기", "rarity": "C", "type": "물", "hp": 125, "atk": 48, "skills": ["몸통박치기", "물대포"]},
    {"id": 10, "name": "캐터피", "rarity": "C", "type": "벌레", "hp": 100, "atk": 35, "skills": ["몸통박치기", "벌레먹기"]},
    {"id": 16, "name": "구구", "rarity": "C", "type": "노말", "hp": 115, "atk": 45, "skills": ["몸통박치기", "바람일으키기"]},
    {"id": 19, "name": "꼬렛", "rarity": "C", "type": "노말", "hp": 95, "atk": 56, "skills": ["전광석화", "몸통박치기"]},
    {"id": 133, "name": "이브이", "rarity": "C", "type": "노말", "hp": 130, "atk": 55, "skills": ["몸통박치기", "전광석화"]},
    {"id": 39, "name": "푸린", "rarity": "C", "type": "노말", "hp": 180, "atk": 45, "skills": ["막치기", "보이스"]},

    # R (Rare) - 35% 확률
    {"id": 25, "name": "피카츄", "rarity": "R", "type": "전기", "hp": 120, "atk": 65, "skills": ["전광석화", "10만볼트"]},
    {"id": 54, "name": "고라파덕", "rarity": "R", "type": "물", "hp": 140, "atk": 55, "skills": ["할퀴기", "염동력"]},
    {"id": 63, "name": "캐이시", "rarity": "R", "type": "에스퍼", "hp": 90, "atk": 70, "skills": ["염동력", "환상빔"]},
    {"id": 143, "name": "잠만보", "rarity": "R", "type": "노말", "hp": 240, "atk": 110, "skills": ["누르기", "기가임팩트"]},
    {"id": 79, "name": "야돈", "rarity": "R", "type": "물", "hp": 170, "atk": 65, "skills": ["몸통박치기", "수포"]},
    {"id": 129, "name": "잉어킹", "rarity": "R", "type": "물", "hp": 70, "atk": 25, "skills": ["튀어오르기", "몸통박치기"]},

    # SR (Super Rare) - 15% 확률
    {"id": 6, "name": "리자몽", "rarity": "SR", "type": "불꽃", "hp": 180, "atk": 115, "skills": ["화염방사", "화염자동차"]},
    {"id": 9, "name": "거북왕", "rarity": "SR", "type": "물", "hp": 190, "atk": 105, "skills": ["하이드로펌프", "하이드로캐논"]},
    {"id": 3, "name": "이상해꽃", "rarity": "SR", "type": "풀", "hp": 195, "atk": 102, "skills": ["솔라빔", "하드플랜트"]},
    {"id": 94, "name": "팬텀", "rarity": "SR", "type": "고스트", "hp": 150, "atk": 120, "skills": ["섀도볼", "병상첨병"]},
    {"id": 149, "name": "망나뇽", "rarity": "SR", "type": "드래곤", "hp": 210, "atk": 134, "skills": ["드래곤크로", "파괴광선"]},
    {"id": 448, "name": "루카리오", "rarity": "SR", "type": "격투", "hp": 160, "atk": 125, "skills": ["파동탄", "인파이트"]},

    # UR (Ultra Rare) - 8% 확률
    {"id": 658, "name": "개굴닌자", "rarity": "UR", "type": "물", "hp": 175, "atk": 130, "skills": ["물수리검", "깜짝베기"]},
    {"id": 130, "name": "갸라도스", "rarity": "UR", "type": "물", "hp": 220, "atk": 135, "skills": ["폭포오르기", "용의파동"]},
    {"id": 248, "name": "마기라스", "rarity": "UR", "type": "악", "hp": 230, "atk": 140, "skills": ["악의파동", "스톤샤워"]},
    {"id": 376, "name": "메타그로스", "rarity": "UR", "type": "강철", "hp": 200, "atk": 145, "skills": ["코멧펀치", "사코키네시스"]},

    # SSR (Legendary/Mythic) - 2% 확률
    {"id": 150, "name": "뮤츠", "rarity": "SSR", "type": "에스퍼", "hp": 240, "atk": 165, "skills": ["사이코브레이크", "파괴광선"]},
    {"id": 151, "name": "뮤", "rarity": "SSR", "type": "에스퍼", "hp": 220, "atk": 140, "skills": ["미러코트", "사이코키네시스"]},
    {"id": 384, "name": "레쿠쟈", "rarity": "SSR", "type": "드래곤", "hp": 250, "atk": 175, "skills": ["화룡점정", "용의파동"]},
    {"id": 493, "name": "아르세우스", "rarity": "SSR", "type": "노말", "hp": 270, "atk": 170, "skills": ["심판의뭉치", "파괴광선"]},
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

# 배틀용 세션 상태 추가
if 'battle_team' not in st.session_state:
    st.session_state.battle_team = []  # 최대 3마리 포켓몬 ID 리스트
if 'battle_state' not in st.session_state:
    st.session_state.battle_state = None  # 배틀 진행 데이터 (player_team, ai_team, turn, logs 등)

# -----------------------------------------------------------------------------
# 4. 헬퍼 함수
# -----------------------------------------------------------------------------
def get_pokemon_by_id(poke_id):
    for p in POKEMON_DB:
        if p["id"] == poke_id:
            return p
    return None

def calc_type_multiplier(atk_type, def_type):
    return TYPE_CHART.get(atk_type, {}).get(def_type, 1.0)

def init_battle(player_ids, difficulty="normal"):
    """배틀 세션 생성"""
    player_instances = []
    for pid in player_ids:
        base = get_pokemon_by_id(pid)
        inv = st.session_state.inventory[pid]
        is_shiny = inv["shiny_count"] > 0
        stat_bonus = 1.2 if is_shiny else 1.0
        
        player_instances.append({
            "id": base["id"],
            "name": base["name"],
            "type": base["type"],
            "max_hp": int(base["hp"] * stat_bonus),
            "hp": int(base["hp"] * stat_bonus),
            "atk": int(base["atk"] * stat_bonus),
            "skills": base["skills"],
            "is_shiny": is_shiny,
            "rarity": base["rarity"]
        })

    # AI 팀 구성 (난이도에 따라 랜덤 3마리)
    ai_instances = []
    if difficulty == "easy":
        pool = [p for p in POKEMON_DB if p["rarity"] in ["C", "R"]]
    elif difficulty == "hard":
        pool = [p for p in POKEMON_DB if p["rarity"] in ["SR", "UR", "SSR"]]
    else:
        pool = POKEMON_DB

    ai_choices = random.sample(pool, 3)
    for base in ai_choices:
        ai_instances.append({
            "id": base["id"],
            "name": base["name"],
            "type": base["type"],
            "max_hp": base["hp"],
            "hp": base["hp"],
            "atk": base["atk"],
            "skills": base["skills"],
            "is_shiny": random.random() < 0.1,
            "rarity": base["rarity"]
        })

    st.session_state.battle_state = {
        "player_team": player_instances,
        "player_active": 0,
        "ai_team": ai_instances,
        "ai_active": 0,
        "logs": ["⚔️ 배틀이 시작되었습니다!"],
        "is_finished": False,
        "winner": None
    }

# 4. 헬퍼 함수
# -----------------------------------------------------------------------------
# 7. 메인 UI - 탭 구성 (가차 화면 & 도감 화면 & 배틀 화면)
# -----------------------------------------------------------------------------
tab_gacha, tab_pokedex, tab_battle = st.tabs(["🎰 가차 뽑기 (Gacha)", "📚 포켓몬 도감 (Pokédex)", "⚔️ AI 배틀 (Battle)"])

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
# =============================================================================
# TAB 3: AI 배틀 (Battle)
# =============================================================================
with tab_battle:
    st.markdown("### ⚔️ AI 포켓몬 배틀 아레나")
    
    # 보유한 포켓몬 목록 가져오기
    caught_ids = [pid for pid, data in st.session_state.inventory.items() if data["count"] > 0]
    
    if len(caught_ids) == 0:
        st.warning("⚠️ 아직 포켓몬을 뽑지 않았습니다! [가차 뽑기] 탭에서 먼저 포켓몬을 수집하세요.")
    else:
        col_setup, col_arena = st.columns([1, 2])
        
        # 1. 팀 엔트리 구성 화면
        with col_setup:
            st.markdown("#### 🛡️ 나의 배틀 엔트리 (최대 3마리)")
            
            # Selectbox 옵션 준비
            poke_options = {pid: f"No.{pid:03d} {get_pokemon_by_id(pid)['name']} [{get_pokemon_by_id(pid)['rarity']}]" for pid in caught_ids}
            
            selected_team = st.multiselect(
                "배틀에 참가할 포켓몬을 선택하세요:",
                options=list(poke_options.keys()),
                format_func=lambda x: poke_options[x],
                max_selections=3,
                default=st.session_state.battle_team if all(p in caught_ids for p in st.session_state.battle_team) else []
            )
            
            st.session_state.battle_team = selected_team
            difficulty = st.selectbox("난이도 선택", ["easy", "normal", "hard"], index=1)
            
            if st.button("🚀 배틀 시작하기!", type="primary", use_container_width=True):
                if len(selected_team) == 0:
                    st.error("최소 1마리 이상의 포켓몬을 선택해야 합니다.")
                else:
                    init_battle(selected_team, difficulty)
                    st.rerun()

        # 2. 배틀 진행 화면
        with col_arena:
            bs = st.session_state.battle_state
            if bs is None:
                st.info("👈 왼쪽에서 배틀 엔트리를 설정하고 '배틀 시작하기' 버튼을 눌러주세요!")
            else:
                player_poke = bs["player_team"][bs["player_active"]]
                ai_poke = bs["ai_team"][bs["ai_active"]]
                
                # HP 비율 계산 및 바 스타일링
                p_hp_pct = max(0, int((player_poke["hp"] / player_poke["max_hp"]) * 100))
                ai_hp_pct = max(0, int((ai_poke["hp"] / ai_poke["max_hp"]) * 100))
                
                p_img = f"{SHINY_URL if player_poke['is_shiny'] else ARTWORK_URL}/{player_poke['id']}.png"
                ai_img = f"{SHINY_URL if ai_poke['is_shiny'] else ARTWORK_URL}/{ai_poke['id']}.png"

                # 전장 대치 레이아웃
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    st.markdown(f"#### 🔵 나의 포켓몬: {player_poke['name']}")
                    st.image(p_img, width=140)
                    st.progress(p_hp_pct / 100)
                    st.caption(f"HP: {player_poke['hp']}/{player_poke['max_hp']} | 타입: {player_poke['type']}")
                    
                with b_col2:
                    st.markdown(f"#### 🔴 상대 AI: {ai_poke['name']}")
                    st.image(ai_img, width=140)
                    st.progress(ai_hp_pct / 100)
                    st.caption(f"HP: {ai_poke['hp']}/{ai_poke['max_hp']} | 타입: {ai_poke['type']}")

                st.markdown("---")

                # 배틀 조작 및 턴 진행
                if not bs["is_finished"]:
                    st.markdown("#### 🗡️ 스킬을 선택하여 공격하세요:")
                    act_cols = st.columns(len(player_poke["skills"]) + 1)
                    
                    # 스킬 공격 실행 로직
                    for s_idx, skill in enumerate(player_poke["skills"]):
                        with act_cols[s_idx]:
                            if st.button(f"💥 {skill}", key=f"skill_{s_idx}", use_container_width=True):
                                # 1) 플레이어 공격
                                mult = calc_type_multiplier(player_poke["type"], ai_poke["type"])
                                dmg = int((player_poke["atk"] * random.uniform(0.8, 1.2)) * mult)
                                ai_poke["hp"] = max(0, ai_poke["hp"] - dmg)
                                
                                effect_msg = " 효과가 뛰어났다!" if mult > 1.0 else (" 효과가 별로인 듯하다..." if mult < 1.0 else "")
                                bs["logs"].append(f"🔵 **{player_poke['name']}**의 {skill}! 상대 {ai_poke['name']}에게 {dmg} 대미지!{effect_msg}")
                                
                                # AI 사망 체크
                                if ai_poke["hp"] <= 0:
                                    bs["logs"].append(f"💀 상대 **{ai_poke['name']}**이(가) 쓰러졌습니다!")
                                    if bs["ai_active"] + 1 < len(bs["ai_team"]):
                                        bs["ai_active"] += 1
                                        next_ai = bs["ai_team"][bs["ai_active"]]
                                        bs["logs"].append(f"🔴 상대가 **{next_ai['name']}**을(를) 내보냈습니다!")
                                    else:
                                        bs["is_finished"] = True
                                        bs["winner"] = "player"
                                        st.session_state.coins += 500  # 승리 보상
                                        bs["logs"].append("🎉 **배틀 승리!** 보상으로 500 코인을 획득했습니다!")
                                
                                # 2) AI 반격 (AI 포켓몬이 생존하고 배틀이 계속될 경우)
                                if not bs["is_finished"] and ai_poke["hp"] > 0:
                                    ai_skill = random.choice(ai_poke["skills"])
                                    ai_mult = calc_type_multiplier(ai_poke["type"], player_poke["type"])
                                    ai_dmg = int((ai_poke["atk"] * random.uniform(0.8, 1.2)) * ai_mult)
                                    player_poke["hp"] = max(0, player_poke["hp"] - ai_dmg)
                                    
                                    ai_effect_msg = " 효과가 뛰어났다!" if ai_mult > 1.0 else (" 효과가 별로인 듯하다..." if ai_mult < 1.0 else "")
                                    bs["logs"].append(f"🔴 상대 **{ai_poke['name']}**의 {ai_skill}! {player_poke['name']}에게 {ai_dmg} 대미지!{ai_effect_msg}")
                                    
                                    if player_poke["hp"] <= 0:
                                        bs["logs"].append(f"💀 나의 **{player_poke['name']}**이(가) 쓰러졌습니다!")
                                        # 다음 살아있는 포켓몬 교체
                                        next_player_idx = next((i for i, p in enumerate(bs["player_team"]) if p["hp"] > 0), None)
                                        if next_player_idx is not None:
                                            bs["player_active"] = next_player_idx
                                            bs["logs"].append(f"🔵 **{bs['player_team'][next_player_idx]['name']}**을(를) 내보냈습니다!")
                                        else:
                                            bs["is_finished"] = True
                                            bs["winner"] = "ai"
                                            bs["logs"].append("😭 모든 포켓몬이 쓰러져 **배틀에서 패배**했습니다.")

                                st.rerun()

                    # 교체 버튼
                    with act_cols[-1]:
                        if st.button("🔄 포켓몬 교체", use_container_width=True):
                            alive_indices = [i for i, p in enumerate(bs["player_team"]) if p["hp"] > 0 and i != bs["player_active"]]
                            if alive_indices:
                                bs["player_active"] = alive_indices[0]
                                bs["logs"].append(f"🔵 **{bs['player_team'][bs['player_active']]['name']}**으로 교체했습니다!")
                                st.rerun()
                            else:
                                st.warning("교체 가능한 생존 포켓몬이 없습니다.")

                else:
                    if bs["winner"] == "player":
                        st.success("🏆 승리하였습니다! 승리 보상: 500 P 획득")
                    else:
                        st.error("💀 패배하였습니다. 팀을 재정비하고 다시 도전해보세요!")

                # 배틀 로그 뷰어
                with st.expander("📜 배틀 로그 (Battle Log)", expanded=True):
                    for log in reversed(bs["logs"]):
                        st.markdown(log)
