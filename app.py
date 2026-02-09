import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 찬양팀 스마트 보드", layout="wide")

# 2. 데이터 저장소
if 'message' not in st.session_state: st.session_state.message = "현재 대기 중..."
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'my_btns' not in st.session_state: st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# CSS: 신호창 디자인 및 배치
st.markdown("""
    <style>
    .fixed-header {
        position: fixed; top: 35px; left: 5%; width: 90%;
        background-color: #ff4b4b; color: white;
        padding: 10px; border-radius: 10px;
        text-align: center; z-index: 1000;
        border: 2px solid white; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    .main-content { margin-top: 100px; }
    .stButton>button { width: 100%; height: 45px; font-weight: bold; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

# 역할 선택
user_role = st.sidebar.radio("📢 역할", ["인도자", "반주자/싱어"])

# 3. 공통 신호창 (화면 최상단 고정)
st.markdown(f'<div class="fixed-header"><h1>{st.session_state.message}</h1></div>', unsafe_allow_html=True)
st.markdown('<div class="main-content">', unsafe_allow_html=True)

if user_role == "인도자":
    st.title("🎮 인도자 관제 센터")
    col_left, col_right = st.columns([2.5, 1])
    
    with col_left:
        # 악보 관리
        files = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if files: st.session_state.sheets = files
        
        if st.session_state.sheets:
            st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

    with col_right:
        # 가사 외 긴급 요청 직접 타이핑
        st.subheader("✍️ 긴급 메시지 직접 입력")
        instant_msg = st.text_input("지금 바로 전달할 말 (예: 드럼 멈춰!)", key="instant")
        if st.button("🚀 즉시 전송") and instant_msg:
            st.session_state.message = f"🚨 {instant_msg}"
            
        st.divider()
        
        # 퀵 버튼 생성 (샘플에서 클릭해서 추가)
        st.subheader("➕ 버튼 추가 아이템")
        samples = ["1절로", "2절로", "3절로", "4절로", "5절로", "6절로", "한 키 업", "전주만", "잔잔하게"]
        sc1, sc2 = st.columns(2)
        for i, s in enumerate(samples):
            target_col = sc1 if i % 2 == 0 else sc2
            if target_col.button(f"➕ {s}"):
                if s not in st.session_state.my_btns:
                    st.session_state.my_btns.append(s)
        
        st.divider()
        
        # 실시간 신호 버튼 리스트
        st.subheader("📢 저장된 신호 보내기")
        for b in st.session_state.my_btns:
            if st.button(f"📍 {b}"):
                st.session_state.message = f"📍 {b} !!"
        
        if st.button("🛑 즉시 멈춤", type="primary"):
            st.session_state.message = "🛑 즉시 멈춤!!"

else:
    # --- 반주자 모드 ---
    if st.session_state.sheets:
        # 페이지 이동 버튼
        pc1, pc2 = st.columns(2)
        with pc1:
            if st.button("◀ 이전"): st.session_state.page = max(0, st.session_state.page - 1)
        with pc2:
            if st.button("다음 ▶"): st.session_state.page = min(len(st.session_state.sheets)-1, st.session_state.page + 1)
            
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
    else:
        st.info("인도자가 올린 악보가 없습니다.")

st.markdown('</div>', unsafe_allow_html=True)
  
  
   
