import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소 (곡별로 버튼을 저장할 딕셔너리 추가)
if 'message_list' not in st.session_state: st.session_state.message_list = [] 
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
# 곡별 저장 저장소 { "곡이름": ["추가한버튼1", "추가한버튼2"] }
if 'sheet_presets' not in st.session_state: st.session_state.sheet_presets = {}
# 기본 버튼 (이건 고정)
default_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# 버튼 클릭 함수
def add_msg(msg): st.session_state.message_list.append(msg)
def move_page(delta):
    new_page = st.session_state.page + delta
    if 0 <= new_page < len(st.session_state.sheets): st.session_state.page = new_page

# 곡별로 추가 버튼 저장하기
def save_preset(song_name, btn_list):
    # 기본 버튼을 제외한 '추가된 버튼'만 필터링해서 저장
    custom_only = [b for b in btn_list if b not in default_btns]
    st.session_state.sheet_presets[song_name] = custom_only

# 3. 디자인 (CSS)
st.markdown("""
    <style>
    .home-icon { position: fixed; top: 10px; right: 20px; font-size: 30px; z-index: 2000; }
    .nav-btn button { height: 70px !important; font-size: 24px !important; background-color: #f0f2f6 !important; border-radius: 12px !important; }
    .signal-box { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px; border: 4px solid white; }
    .stButton>button { width: 100%; font-weight: bold; }
    </style>
    <div class="home-icon">🏠</div>
""", unsafe_allow_html=True)

user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

# 4. 인도자 화면
if user_role == "인도자":
    st.title("🎮 인도자 센터")
    current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "대기 중"
    st.markdown(f'<div class="signal-box"><h2>📢 현재 신호: {current_msg}</h2></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2.5, 1.2])
    
    with col_left:
        files = st.file_uploader("악보 업로드 (여러 장 가능)", accept_multiple_files=True)
        if files: st.session_state.sheets = files
        
        if st.session_state.sheets:
            current_sheet = st.session_state.sheets[st.session_state.page]
            song_name = current_sheet.name.split('.')[0] # 파일명에서 확장자 제거
            
            # 페이지 이동 버튼
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            c1.button(f"◀ {st.session_state.page}번", on_click=move_page, args=(-1,))
            c2.button(f"{st.session_state.page + 2}번 ▶", on_click=move_page, args=(1,))
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.subheader(f"📄 현재 악보: {song_name}")
            st.image(current_sheet, use_container_width=True)

    with col_right:
        if st.session_state.sheets:
            # 해당 곡에 저장된 프리셋 불러오기
            if song_name not in st.session_state.sheet_presets:
                st.session_state.sheet_presets[song_name] = []
            
            active_btns = default_btns + st.session_state.sheet_presets[song_name]

            st.subheader("➕ 이 곡에 버튼 추가")
            samples = ["1절로", "2절로", "3절로", "한 키 업", "전주만", "드럼만", "잔잔하게"]
            sc1, sc2 = st.columns(2)
            for i, s in enumerate(samples):
                target = sc1 if i % 2 == 0 else sc2
                if target.button(f"➕ {s}", key=f"add_{s}"):
                    if s not in st.session_state.sheet_presets[song_name]:
                        st.session_state.sheet_presets[song_name].append(s)
                        st.rerun()

            st.divider()
            st.subheader("📢 전송 (현재 곡 맞춤)")
            for b in active_btns:
                st.button(f"📍 {b}", key=f"send_{b}", on_click=add_msg, args=(f"📍 {b} !!",))
            
            st.divider()
            if st.button("💾 이 곡의 설정 저장"):
                st.success(f"'{song_name}' 곡의 버튼들이 저장되었습니다!")
        else:
            st.info("먼저 악보를 업로드해주세요.")

# 5. 반주자 화면 (기존 레이아웃 유지)
else:
    if st.session_state.sheets:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns(2)
        btn_col1.button("◀ PREV", on_click=move_page, args=(-1,))
        btn_col2.button("NEXT ▶", on_click=move_page, args=(1,))
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.message_list:
            st.markdown(f'<div class="signal-box"><h1 style="font-size:60px; margin:0;">{current_msg}</h1></div>', unsafe_allow_html=True)
        
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
