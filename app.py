import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. [저장 기능] 세션 상태 설정 (나중에 DB 한 줄만 연결하면 영구 저장돼!)
if 'message_list' not in st.session_state: st.session_state.message_list = [] # 여러 신호 저장
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'my_btns' not in st.session_state: 
    st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# CSS: 반주자 패드 세로 모드 최적화 (악보를 절대 가리지 않음)
st.markdown("""
    <style>
    /* 신호창: 화면 상단에 고정되지만, 아래 콘텐츠를 밀어냄 */
    .musician-header {
        position: sticky; top: 0; 
        background-color: #ff4b4b; color: white;
        padding: 10px; border-radius: 0 0 15px 15px;
        text-align: center; z-index: 1000;
        border-bottom: 5px solid white;
    }
    .msg-item { font-size: 20px; font-weight: bold; margin: 2px 0; border-bottom: 1px solid #ff7373; }
    .stButton>button { width: 100%; height: 45px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

user_role = st.sidebar.radio("📢 역할", ["인도자", "반주자/싱어"])

# 3. 반주자 화면 (신호창이 악보 위에 '떠 있지' 않고 '위에 붙어' 있음)
if user_role == "반주자/싱어":
    # 여러 개의 신호를 리스트로 보여줌
    if st.session_state.message_list:
        with st.container():
            st.markdown('<div class="musician-header">', unsafe_allow_html=True)
            for m in st.session_state.message_list[-3:]: # 최신 신호 3개만 표시
                st.markdown(f'<div class="msg-item">{m}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # 악보 표시 (신호창 바로 아래부터 시작되어 절대 안 가림)
    if st.session_state.sheets:
        c1, c2 = st.columns(2)
        if c1.button("◀ 이전"): st.session_state.page = max(0, st.session_state.page - 1)
        if c2.button("다음 ▶"): st.session_state.page = min(len(st.session_state.sheets)-1, st.session_state.page + 1)
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

# 4. 인도자 화면
else:
    st.title("🎮 인도자 센터")
    
    # 현재 전송된 신호들 확인 및 삭제
    with st.expander("📝 현재 전송 중인 신호 리스트"):
        for i, m in enumerate(st.session_state.message_list):
            st.write(f"{i+1}. {m}")
        if st.button("신호 전체 삭제"): 
            st.session_state.message_list = []
            st.rerun()

    col_left, col_right = st.columns([2.5, 1])
    
    with col_left:
        files = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if files: st.session_state.sheets = files
        if st.session_state.sheets:
            st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

    with col_right:
        st.subheader("🚀 신호 여러 개 보내기")
        inst_msg = st.text_input("직접 입력", key="inst_final")
        if st.button("🚀 즉시 추가") and inst_msg:
            st.session_state.message_list.append(f"🚨 {inst_msg}")
            st.rerun()

        st.divider()
        st.write("➕ 버튼 클릭 시 리스트에 추가됨")
        # 샘플 및 커스텀 버튼들
        for b in st.session_state.my_btns:
            if st.button(f"📍 {b}"):
                st.session_state.message_list.append(f"📍 {b} !!")
                st.rerun()
  
     
