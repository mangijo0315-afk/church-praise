import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소 (세션 상태)
if 'message_list' not in st.session_state: st.session_state.message_list = [] 
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
# 기본적으로 항상 있어야 할 버튼들
if 'my_btns' not in st.session_state: 
    st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# CSS: 반주자 패드 세로 모드 최적화 (신호창이 악보를 절대 가리지 않음)
st.markdown("""
    <style>
    .musician-header {
        position: sticky; top: 0; 
        background-color: #ff4b4b; color: white;
        padding: 10px; border-radius: 0 0 15px 15px;
        text-align: center; z-index: 1000;
        border-bottom: 5px solid white;
    }
    .msg-item { font-size: 22px; font-weight: bold; margin: 3px 0; border-bottom: 1px solid #ff7373; }
    .stButton>button { width: 100%; height: 45px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

# 3. 반주자 화면 (가림 방지 처리됨)
if user_role == "반주자/싱어":
    if st.session_state.message_list:
        st.markdown('<div class="musician-header">', unsafe_allow_html=True)
        # 최신 신호 3개까지 노출
        for m in st.session_state.message_list[-3:]:
            st.markdown(f'<div class="msg-item">{m}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.sheets:
        c1, c2 = st.columns(2)
        if c1.button("◀ 이전"): st.session_state.page = max(0, st.session_state.page - 1)
        if c2.button("다음 ▶"): st.session_state.page = min(len(st.session_state.sheets)-1, st.session_state.page + 1)
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

# 4. 인도자 화면 (샘플 복구 + 타이핑 추가)
else:
    st.title("🎮 인도자 센터")
    
    # 현재 나가는 신호 확인창
    with st.expander("📝 현재 나가는 신호 (클릭해서 삭제)"):
        if st.button("🔴 모든 신호 삭제"): 
            st.session_state.message_list = []
            st.rerun()
        for i, m in enumerate(st.session_state.message_list):
            st.write(f"{i+1}. {m}")

    col_left, col_right = st.columns([2.5, 1])
    
    with col_left:
        files = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if files: st.session_state.sheets = files
        if st.session_state.sheets:
            st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

    with col_right:
        st.subheader("✍️ 즉시 타이핑 전송")
        inst_msg = st.text_input("전달할 말 입력", key="leader_typing")
        if st.button("🚀 전송") and inst_msg:
            st.session_state.message_list.append(f"🚨 {inst_msg}")
            st.rerun()

        st.divider()
        st.subheader("➕ 샘플로 버튼 추가")
        # 네가 원했던 샘플들 다시 나열!
        samples = ["1절로", "2절로", "3절로", "4절로", "한 키 업", "전주만", "드럼만", "잔잔하게"]
        s_col1, s_col2 = st.columns(2)
        for i, s in enumerate(samples):
            target = s_col1 if i % 2 == 0 else s_col2
            if target.button(f"➕ {s}"):
                if s not in st.session_state.my_btns:
                    st.session_state.my_btns.append(s)
                st.rerun()

        st.divider()
        st.subheader("📢 신호 보내기 (클릭!)")
        # 생성된 버튼들 나열
        for b in st.session_state.my_btns:
            if st.button(f"📍 {b}"):
                st.session_state.message_list.append(f"📍 {b} !!")
                st.rerun()
