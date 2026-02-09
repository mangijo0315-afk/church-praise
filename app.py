import streamlit as st

# 1. 앱 설정 (반응형 레이아웃)
st.set_page_config(page_title="대흥교회 찬양팀 스마트 보드", layout="wide")

# 2. 데이터 저장 (세션 상태 - 나중에 진짜 DB 연결하면 영구 저장돼!)
if 'message' not in st.session_state: st.session_state.message = "현재 대기 중..."
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'custom_buttons' not in st.session_state: 
    st.session_state.custom_buttons = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩", "6절로", "한 키 업!", "드럼 작게"]

# CSS: 신호창 상단 고정 및 디자인
st.markdown("""
    <style>
    .fixed-header {
        position: fixed; top: 40px; left: 5%; width: 90%;
        background-color: #ff4b4b; color: white;
        padding: 10px; border-radius: 10px;
        text-align: center; z-index: 1000;
        border: 3px solid white; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .main-content { margin-top: 100px; }
    .stButton>button { width: 100%; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# 사이드바 역할 선택
user_role = st.sidebar.radio("📢 역할", ["인도자", "반주자/싱어"])

# 공통 신호창 (화면 맨 위 박제)
st.markdown(f'<div class="fixed-header"><h1>{st.session_state.message}</h1></div>', unsafe_allow_html=True)

st.markdown('<div class="main-content">', unsafe_allow_html=True)

# 인도자 & 반주자 공통 레이아웃 (악보 크게 + 버튼 오른쪽)
col_score, col_ctrl = st.columns([3, 1])

with col_score:
    if user_role == "인도자":
        st.subheader("📸 악보 관리")
        files = st.file_uploader("악보 업로드 (캡처본 가능)", accept_multiple_files=True)
        if files: st.session_state.sheets = files
    
    if st.session_state.sheets:
        # 페이지 넘기기
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1: 
            if st.button("◀ 이전"): st.session_state.page = max(0, st.session_state.page - 1)
        with c2: st.write(f"📄 {st.session_state.page + 1} / {len(st.session_state.sheets)}")
        with c3:
            if st.button("다음 ▶"): st.session_state.page = min(len(st.session_state.sheets)-1, st.session_state.page + 1)
        
        # 악보 출력
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
    else:
        st.info("올려진 악보가 없습니다.")

with col_ctrl:
    st.subheader("🎮 퀵 컨트롤")
    
    # 1. 긴급 요청 샘플 (타이핑 없이 바로 클릭!)
    st.write("🆘 긴급 요청")
    samples = ["한 키 업!", "드럼 작게", "볼륨 업!", "처음부터", "간주 점프"]
    for s in samples:
        if st.button(f"🆘 {s}"): st.session_state.message = f"🚨 {s} !!"
    
    st.divider()
    
    # 2. 인도자 전용 버튼 생성 및 신호
    st.write("📢 구간 이동")
    for btn in st.session_state.custom_buttons:
        if st.button(btn):
            st.session_state.message = f"📍 {btn} !!"
            
    if user_role == "인도자":
        with st.expander("➕ 버튼/메모 추가"):
            new_btn = st.text_input("이름 입력")
            if st.button("등록") and new_btn:
                st.session_state.custom_buttons.append(new_btn)
                st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

    
       
