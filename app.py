import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소 및 버튼 클릭 함수 (에러 방지용)
if 'message_list' not in st.session_state: st.session_state.message_list = [] 
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'my_btns' not in st.session_state: st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# 버튼 클릭 시 즉시 실행될 함수들 (이게 있어야 버튼이 씹히지 않아!)
def add_msg(msg): st.session_state.message_list.append(msg)
def add_custom_btn(btn_name): 
    if btn_name not in st.session_state.my_btns: st.session_state.my_btns.append(btn_name)
def move_page(delta):
    new_page = st.session_state.page + delta
    if 0 <= new_page < len(st.session_state.sheets): st.session_state.page = new_page

# 3. 디자인 (CSS)
st.markdown("""
    <style>
    .home-icon { position: fixed; top: 10px; right: 20px; font-size: 30px; z-index: 2000; }
    .nav-btn button { height: 80px !important; font-size: 28px !important; background-color: #f0f2f6 !important; border-radius: 12px !important; }
    .signal-box { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px; border: 4px solid white; }
    .stButton>button { width: 100%; font-weight: bold; }
    </style>
    <div class="home-icon">🏠</div>
""", unsafe_allow_html=True)

# 4. 역할 선택 및 저장 관리
user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

with st.sidebar.expander("💾 설정 저장 및 관리"):
    if st.button("현재 세팅 임시 저장"):
        st.success("현재 버튼과 악보가 세션에 저장되었습니다!")
    if st.button("🔄 전체 초기화"):
        st.session_state.message_list = []
        st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]
        st.rerun()

current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "대기 중"

# ---------------------------------------------------------
# 5. 인도자 화면 (배치: 신호 -> 버튼 -> 악보)
# ---------------------------------------------------------
if user_role == "인도자":
    st.title("🎮 인도자 센터")
    st.markdown(f'<div class="signal-box"><h2>📢 현재 신호: {current_msg}</h2></div>', unsafe_allow_html=True)

    if st.session_state.sheets:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button("◀ 이전 악보", on_click=move_page, args=(-1,))
        c2.button("다음 악보 ▶", on_click=move_page, args=(1,))
        st.markdown('</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2.5, 1.2])
    with col_left:
        files = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if files: st.session_state.sheets = files
        if st.session_state.sheets:
            st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

    with col_right:
        st.subheader("✍️ 즉시 타이핑")
        inst_msg = st.text_input("메시지 입력", key="leader_input")
        if st.button("🚀 전송") and inst_msg:
            add_msg(f"🚨 {inst_msg}")
            st.rerun()
        
        st.divider()
        st.subheader("➕ 버튼 추가")
        samples = ["1절로", "2절로", "3절로", "한 키 업", "전주만", "드럼만"]
        sc1, sc2 = st.columns(2)
        for i, s in enumerate(samples):
            target = sc1 if i % 2 == 0 else sc2
            target.button(f"➕ {s}", key=f"add_{s}", on_click=add_custom_btn, args=(s,))
            
        st.divider()
        st.subheader("📢 전송 버튼")
        for b in st.session_state.my_btns:
            st.button(f"📍 {b}", key=f"send_{b}", on_click=add_msg, args=(f"📍 {b} !!",))

# ---------------------------------------------------------
# 6. 반주자 화면 (배치: 버튼 -> 신호 -> 악보)
# ---------------------------------------------------------
else:
    if st.session_state.sheets:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns(2)
        btn_col1.button("◀ PREV (이전)", on_click=move_page, args=(-1,))
        btn_col2.button("NEXT (다음) ▶", on_click=move_page, args=(1,))
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.session_state.message_list:
            st.markdown(f'<div class="signal-box"><h1 style="font-size:60px; margin:0;">{current_msg}</h1></div>', unsafe_allow_html=True)
        
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
    else:
        st.info("인도자가 악보를 올릴 때까지 기다려주세요.")
