import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소
if 'message_list' not in st.session_state: st.session_state.message_list = [] 
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'my_btns' not in st.session_state: st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# CSS: 신호창 -> 이동 버튼 -> 악보 순서로 배치 & 디자인
st.markdown("""
    <style>
    .home-icon { position: fixed; top: 10px; right: 20px; font-size: 30px; z-index: 2000; }
    /* 신호창: 맨 위에 왕 크게 */
    .signal-box {
        background-color: #ff4b4b; color: white;
        padding: 25px; border-radius: 15px;
        text-align: center; margin-bottom: 10px;
        border: 5px solid white; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    /* 페이지 이동 버튼: 연주 중 터치하기 쉽게 크게 */
    .nav-btn button {
        height: 70px !important; font-size: 25px !important; 
        background-color: #f0f2f6 !important; border-radius: 10px !important;
    }
    .stButton>button { width: 100%; font-weight: bold; }
    </style>
    <div class="home-icon">🏠</div>
""", unsafe_allow_html=True)

user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])
current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "대기 중"

# 3. 인도자 화면 (신호창 하단 배치로 가림 방지)
if user_role == "인도자":
    st.title("🎮 인도자 컨트롤 센터")
    st.markdown(f'<div class="signal-box"><h2 style="margin:0;">📢 현재 신호: {current_msg}</h2></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2.5, 1.2])
    with col_left:
        files = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if files: st.session_state.sheets = files
        if st.session_state.sheets:
            # 인도자용 큰 이동 버튼
            c1, c2 = st.columns(2)
            if c1.button("◀ 이전 악보", key="l_prev"): st.session_state.page = max(0, st.session_state.page - 1)
            if c2.button("다음 악보 ▶", key="l_next"): st.session_state.page = min(len(st.session_state.sheets)-1, st.session_state.page + 1)
            st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

    with col_right:
        st.subheader("✍️ 즉시 타이핑")
        inst_msg = st.text_input("메시지 입력", key="leader_input")
        if st.button("🚀 전송") and inst_msg:
            st.session_state.message_list.append(f"🚨 {inst_msg}")
            st.rerun()
        st.divider()
        st.subheader("➕ 버튼 추가")
        samples = ["1절로", "2절로", "3절로", "한 키 업", "전주만", "드럼만"]
        sc1, sc2 = st.columns(2)
        for i, s in enumerate(samples):
            target = sc1 if i % 2 == 0 else sc2
            if target.button(f"➕ {s}", key=f"add_{s}"):
                if s not in st.session_state.my_btns:
                    st.session_state.my_btns.append(s)
                    st.rerun()
        st.divider()
        st.subheader("📢 전송 버튼")
        for b in st.session_state.my_btns:
            if st.button(f"📍 {b}", key=f"send_{b}"):
                st.session_state.message_list.append(f"📍 {b} !!")
                st.rerun()

# 4. 반주자 화면 (요청하신 순서: 신호 -> 버튼 -> 악보)
else:
    # [1순위] 신호창 (맨 위)
    if st.session_state.message_list:
        st.markdown(f'<div class="signal-box"><h1 style="font-size:60px; margin:0;">{current_msg}</h1></div>', unsafe_allow_html=True)
    
    # [2순위] 이동 버튼 (신호창 바로 아래)
    if st.session_state.sheets:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        if c1.button("◀ PREV (이전)", key="p_prev"): st.session_state.page = max(0, st.session_state.page - 1)
        if c2.button("NEXT (다음) ▶", key="p_next"): st.session_state.page = min(len(st.session_state.sheets)-1, st.session_state.page + 1)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # [3순위] 악보 (맨 아래)
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
    else:
        st.info("인도자가 악보를 올릴 때까지 기다려주세요.")
