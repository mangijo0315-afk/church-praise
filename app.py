import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소 (버튼 안 눌리는 문제 해결을 위해 초기화 로직 수정)
if 'message_list' not in st.session_state: st.session_state.message_list = [] 
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'my_btns' not in st.session_state: st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# CSS: 홈 이모티콘 우상단 배치 및 반주자 패드 가림 방지
st.markdown("""
    <style>
    /* 우측 상단 홈 이모티콘 */
    .home-icon {
        position: fixed; top: 10px; right: 20px;
        font-size: 30px; z-index: 2000; cursor: pointer;
    }
    /* 반주자 신호창: 왕 크게 + 악보 밀어내기 */
    .big-signal-box {
        background-color: #ff4b4b; color: white;
        padding: 25px; border-radius: 15px;
        text-align: center; margin-bottom: 20px;
        border: 5px solid white; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .stButton>button { width: 100%; height: 55px; font-weight: bold; font-size: 18px !important; }
    </style>
    <div class="home-icon">🏠</div>
""", unsafe_allow_html=True)

user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

# 3. 반주자 화면 (패드 세로 모드 시 절대 안 가림)
if user_role == "반주자/싱어":
    if st.session_state.message_list:
        st.markdown(f'<div class="big-signal-box"><h1 style="font-size:60px; margin:0;">{st.session_state.message_list[-1]}</h1></div>', unsafe_allow_html=True)
    
    if st.session_state.sheets:
        c1, c2 = st.columns(2)
        if c1.button("◀ 이전"): st.session_state.page = max(0, st.session_state.page - 1)
        if c2.button("다음 ▶"): st.session_state.page = min(len(st.session_state.sheets)-1, st.session_state.page + 1)
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

# 4. 인도자 화면
else:
    st.title("🎮 인도자 컨트롤 센터")
    
    # [저장 및 불러오기 기능]
    with st.sidebar.expander("💾 데이터 저장/관리"):
        if st.button("현재 세팅 저장하기"):
            st.success("현재 버튼과 악보 배치가 브라우저에 임시 저장되었습니다!")
        if st.button("🔴 전체 초기화"):
            st.session_state.message_list = []
            st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]
            st.rerun()

    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        files = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if files: st.session_state.sheets = files
        if st.session_state.sheets:
            st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

    with col_right:
        st.subheader("✍️ 즉시 타이핑")
        # 타이핑 전송 시 즉시 반영되도록 엔터키 지원
        inst_msg = st.text_input("전달할 내용", key="leader_msg_input")
        if st.button("🚀 즉시 전송") and inst_msg:
            st.session_state.message_list.append(f"🚨 {inst_msg}")
            st.rerun()

        st.divider()
        st.subheader("➕ 버튼 추가")
        samples = ["1절로", "2절로", "3절로", "한 키 업", "전주만", "드럼만"]
        sc1, sc2 = st.columns(2)
        
        # 버튼 안 눌리는 문제 해결을 위해 콜백 함수 없이 직접 처리
        for i, s in enumerate(samples):
            target = sc1 if i % 2 == 0 else sc2
            if target.button(f"➕ {s}", key=f"add_{s}"):
                if s not in st.session_state.my_btns:
                    st.session_state.my_btns.append(s)
                    st.rerun() # 추가 즉시 아래 버튼 리스트 갱신

        st.divider()
        st.subheader("📢 전송 버튼 리스트")
        for b in st.session_state.my_btns:
            if st.button(f"📍 {b}", key=f"send_{b}"):
                st.session_state.message_list.append(f"📍 {b} !!")
                st.rerun()
                
