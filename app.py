import streamlit as st

st.set_page_config(page_title="대흥교회 찬양팀 스마트 보드", layout="wide")

# 1. 상태 저장 (메시지, 여러 장의 악보, 현재 페이지 번호)
if 'message' not in st.session_state: st.session_state.message = "현재 대기 중..."
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'custom_buttons' not in st.session_state: st.session_state.custom_buttons = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# CSS로 신호창을 화면 상단에 박제 (스크롤 해도 따라옴)
st.markdown("""
    <style>
    .fixed-header {
        position: fixed;
        top: 50px; left: 10%; width: 80%;
        background-color: #ff4b4b; color: white;
        padding: 15px; border-radius: 15px;
        text-align: center; z-index: 999;
        border: 4px solid white; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .content-area { margin-top: 130px; }
    </style>
""", unsafe_allow_html=True)

# 역할 선택
user_role = st.sidebar.radio("📢 내 역할", ["인도자", "반주자/싱어"])

if user_role == "인도자":
    st.header("🎮 인도자 컨트롤 패널")
    col1, col2 = st.columns([1.5, 1])
    
    with col1:
        st.subheader("📸 악보 여러 장 올리기")
        files = st.file_uploader("악보들을 선택하세요 (한번에 여러 장 가능)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
        if files: st.session_state.sheets = files
        
        if st.session_state.sheets:
            st.info(f"현재 총 {len(st.session_state.sheets)}장의 악보가 올라와 있습니다.")

    with col2:
        st.subheader("🛠️ 버튼 추가 & 신호")
        new_btn = st.text_input("새 버튼 이름")
        if st.button("➕ 추가") and new_btn:
            st.session_state.custom_buttons.append(new_btn)
        
        st.divider()
        for btn in st.session_state.custom_buttons:
            if st.button(btn, use_container_width=True):
                st.session_state.message = f"📍 {btn} !!"

else:
    # --- 반주자 모드 (스크롤 고정 신호창 포함) ---
    st.markdown(f'<div class="fixed-header"><h1>{st.session_state.message}</h1></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="content-area">', unsafe_allow_html=True)
    if st.session_state.sheets:
        # 악보 넘기기 버튼
        col_prev, col_page, col_next = st.columns([1, 2, 1])
        with col_prev:
            if st.button("◀ 이전 악보"): st.session_state.page = max(0, st.session_state.page - 1)
        with col_page:
            st.write(f"📄 {st.session_state.page + 1} / {len(st.session_state.sheets)} 페이지")
        with col_next:
            if st.button("다음 악보 ▶"): st.session_state.page = min(len(st.session_state.sheets) - 1, st.session_state.page + 1)
        
        # 현재 페이지 악보 크게 보기
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
    else:
        st.warning("인도자가 악보를 올릴 때까지 기다려주세요.")
    st.markdown('</div>', unsafe_allow_html=True)
    
   
   
