import streamlit as st

# 1. 앱 설정 (최대한 넓게)
st.set_page_config(page_title="대흥교회 찬양팀 스마트 보드", layout="wide")

# 2. 데이터 저장소 (세션 상태)
if 'message' not in st.session_state: st.session_state.message = "현재 대기 중..."
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
# 인도자가 직접 만든 버튼들이 저장되는 곳
if 'my_btns' not in st.session_state: st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# CSS: 반주자 모드에서 신호창을 더 작고 스마트하게 상단 고정
st.markdown("""
    <style>
    .fixed-header {
        position: fixed; top: 35px; left: 5%; width: 90%;
        background-color: #ff4b4b; color: white;
        padding: 10px; border-radius: 10px;
        text-align: center; z-index: 1000;
        border: 2px solid white; box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
    }
    .musician-content { margin-top: 100px; width: 100% !important; }
    .stButton>button { width: 100%; height: 45px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 역할 선택 (사이드바)
user_role = st.sidebar.radio("📢 역할", ["인도자", "반주자/싱어"])

# 3. 인도자 화면
if user_role == "인도자":
    st.title("🎮 인도자 관제 센터")
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("🎼 악보 및 파일 관리")
        files = st.file_uploader("악보 업로드 (여러 장 가능)", accept_multiple_files=True)
        if files: st.session_state.sheets = files
        
        if st.session_state.sheets:
            c1, c2, c3 = st.columns([1, 2, 1])
            with c1: 
                if st.button("◀ 이전"): st.session_state.page = max(0, st.session_state.page - 1)
            with col_left: # 악보 크게 보기
                st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
    
    with col_right:
        st.subheader("⚡ 퀵 버튼 생성")
        # 샘플 단어들 (클릭하면 바로 아래 버튼 리스트에 추가됨)
        st.write("아이템 클릭 시 버튼 자동 생성:")
        samples = ["1절로", "2절로", "3절로", "4절로", "5절로", "6절로", "한 키 업", "드럼만", "전주만", "잔잔하게"]
        
        # 샘플들을 한 줄에 2개씩 배치
        sc1, sc2 = st.columns(2)
        for i, s in enumerate(samples):
            target_col = sc1 if i % 2 == 0 else sc2
            if target_col.button(f"➕ {s}"):
                if s not in st.session_state.my_btns:
                    st.session_state.my_btns.append(s)
        
        st.divider()
        st.subheader("📢 실시간 신호 전송")
        # 생성된 버튼들 나열
        for b in st.session_state.my_btns:
            if st.button(f"📍 {b}", key=f"send_{b}"):
                st.session_state.message = f"📍 {b} !!"
        
        if st.button("🛑 즉시 멈춤", type="primary"):
            st.session_state.message = "🛑 즉시 멈춤!!"
        
        if st.button("🗑️ 버튼 초기화"):
            st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]
            st.rerun()

# 4. 반주자 화면 (버튼 없이 악보만 꽉 차게!)
else:
    st.markdown(f'<div class="fixed-header"><h1>{st.session_state.message}</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="musician-content">', unsafe_allow_html=True)
    
    if st.session_state.sheets:
        # 악보 페이지 이동용 투명 버튼 (최상단)
        pc1, pc2 = st.columns(2)
        with pc1:
            if st.button("◀ 이전 페이지"): st.session_state.page = max(0, st.session_state.page - 1)
        with pc2:
            if st.button("다음 페이지 ▶"): st.session_state.page = min(len(st.session_state.sheets)-1, st.session_state.page + 1)
            
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
    else:
        st.info("인도자가 올린 악보가 없습니다.")
    st.markdown('</div>', unsafe_allow_html=True)
  
    
   
  


