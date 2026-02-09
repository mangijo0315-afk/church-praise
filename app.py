import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소 (곡별 프리셋 구조)
if 'message_list' not in st.session_state: st.session_state.message_list = [] 
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'sheet_presets' not in st.session_state: st.session_state.sheet_presets = {}
# 기본 버튼 (항상 노출)
default_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# 기능 함수 (on_click 연결용)
def add_msg(msg): st.session_state.message_list.append(msg)
def move_page(delta):
    new_page = st.session_state.page + delta
    if 0 <= new_page < len(st.session_state.sheets): st.session_state.page = new_page
def add_custom_to_song(song_name, btn_name):
    if song_name not in st.session_state.sheet_presets:
        st.session_state.sheet_presets[song_name] = []
    if btn_name not in st.session_state.sheet_presets[song_name]:
        st.session_state.sheet_presets[song_name].append(btn_name)

# 3. 디자인 (CSS)
st.markdown("""
    <style>
    .home-icon { position: fixed; top: 10px; right: 20px; font-size: 30px; z-index: 2000; }
    .nav-btn button { height: 75px !important; font-size: 26px !important; background-color: #f0f2f6 !important; border-radius: 12px !important; }
    .signal-box { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px; border: 4px solid white; }
    .stButton>button { width: 100%; font-weight: bold; }
    </style>
    <div class="home-icon">🏠</div>
""", unsafe_allow_html=True)

# 4. 사이드바 (역할 선택 및 저장 메뉴 복구)
user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

with st.sidebar.expander("💾 설정 저장 및 관리", expanded=True):
    if st.button("현재 모든 세팅 저장"):
        st.success("곡별 맞춤 버튼들이 시스템에 저장되었습니다!")
    
    if st.session_state.sheet_presets:
        st.write("📂 **곡별 저장된 요청사항**")
        for song, btns in st.session_state.sheet_presets.items():
            if btns: st.caption(f"🎵 {song}: {', '.join(btns)}")
            
    if st.button("🔄 전체 초기화"):
        st.session_state.message_list = []
        st.session_state.sheet_presets = {}
        st.session_state.sheets = []
        st.rerun()

current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "대기 중"

# ---------------------------------------------------------
# 5. 인도자 화면 (배치: 신호 -> 버튼 -> 악보)
# ---------------------------------------------------------
if user_role == "인도자":
    st.title("🎮 인도자 센터")
    st.markdown(f'<div class="signal-box"><h2>📢 현재 신호: {current_msg}</h2></div>', unsafe_allow_html=True)

    if st.session_state.sheets:
        cur_file = st.session_state.sheets[st.session_state.page]
        song_name = cur_file.name.split('.')[0]
        
        # [이전/다음 버튼]
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button(f"◀ {st.session_state.page}번", on_click=move_page, args=(-1,))
        c2.button(f"{st.session_state.page + 2}번 ▶", on_click=move_page, args=(1,))
        st.markdown('</div>', unsafe_allow_html=True)

        col_left, col_right = st.columns([2.5, 1.2])
        with col_left:
            st.subheader(f"📄 현재 곡: {song_name}")
            st.image(cur_file, use_container_width=True)
            files = st.file_uploader("추가 악보 업로드", accept_multiple_files=True)
            if files: st.session_state.sheets = files

        with col_right:
            st.subheader("➕ 이 곡에만 추가")
            samples = ["1절로", "2절로", "3절로", "한 키 업", "전주만", "드럼만", "잔잔하게"]
            sc1, sc2 = st.columns(2)
            for i, s in enumerate(samples):
                target = sc1 if i % 2 == 0 else sc2
                target.button(f"➕ {s}", key=f"add_{s}", on_click=add_custom_to_song, args=(song_name, s))

            st.divider()
            st.subheader("📢 신호 전송")
            # 기본 버튼 + 이 곡에 저장된 커스텀 버튼들만 노출
            song_btns = default_btns + st.session_state.sheet_presets.get(song_name, [])
            for b in song_btns:
                st.button(f"📍 {b}", key=f"send_{b}", on_click=add_msg, args=(f"📍 {b} !!",))
    else:
        st.info("먼저 악보를 업로드해주세요.")
        st.file_uploader("악보 업로드", accept_multiple_files=True, key="init_upload", on_change=lambda: st.session_state.update({"sheets": st.session_state.init_upload}))

# ---------------------------------------------------------
# 6. 반주자 화면 (배치: 버튼 -> 신호 -> 악보)
# ---------------------------------------------------------
else:
    if st.session_state.sheets:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns(2)
        btn_col1.button("◀ PREV", on_click=move_page, args=(-1,))
        btn_col2.button("NEXT ▶", on_click=move_page, args=(1,))
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div class="signal-box"><h1 style="font-size:60px; margin:0;">{current_msg}</h1></div>', unsafe_allow_html=True)
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
