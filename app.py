import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소
if 'message' not in st.session_state: st.session_state.message = "대기 중"
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'my_btns' not in st.session_state: st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# CSS: 인도자와 반주자 스타일 분리
st.markdown("""
    <style>
    /* 반주자용: 스크롤해도 상단에 고정되는 빨간 신호창 */
    .musician-header {
        position: fixed; top: 35px; left: 5%; width: 90%;
        background-color: #ff4b4b; color: white;
        padding: 10px; border-radius: 10px;
        text-align: center; z-index: 1000;
        border: 2px solid white; box-shadow: 0px 4px 10px rgba(0,0,0,0.2);
    }
    /* 인도자용: 악보를 가리지 않는 깔끔한 알림바 */
    .leader-msg-bar {
        background-color: #f0f2f6;
        padding: 15px; border-radius: 10px;
        border-left: 10px solid #ff4b4b;
        margin-bottom: 20px; font-weight: bold;
    }
    .stButton>button { width: 100%; height: 40px; margin-bottom: 5px; }
    </style>
""", unsafe_allow_html=True)

user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

# 3. 인도자 화면 (가림 방지 레이아웃)
if user_role == "인동자" or user_role == "인도자":
    st.title("🎮 인도자 센터")
    
    # [중요] 인도자 화면에서는 신호창을 '상단 고정'하지 않고 일반 칸에 배치!
    st.markdown(f'<div class="leader-msg-bar">📢 현재 전송 중인 신호: <span style="font-size:25px; color:#ff4b4b;">{st.session_state.message}</span></div>', unsafe_allow_html=True)

    col_score, col_ctrl = st.columns([2.5, 1])
    
    with col_score:
        # 악보 업로드 및 보기
        files = st.file_uploader("파일 업로드", accept_multiple_files=True, label_visibility="collapsed")
        if files: st.session_state.sheets = files
        
        if st.session_state.sheets:
            # 악보 출력 (고정창이 없으므로 맨 위부터 다 보임)
            st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
        else:
            st.info("악보를 올려주세요.")

    with col_ctrl:
        # 긴급 메시지
        st.write("✍️ 즉시 타이핑")
        inst_msg = st.text_input("전달할 내용", key="inst_leader")
        if st.button("🚀 전송") and inst_msg:
            st.session_state.message = f"🚨 {inst_msg}"
            st.rerun()

        st.divider()
        # 버튼 공장
        st.write("➕ 버튼 추가")
        samples = ["1절로", "2절로", "3절로", "한 키 업", "전주만", "잔잔하게"]
        sc1, sc2 = st.columns(2)
        for i, s in enumerate(samples):
            target = sc1 if i % 2 == 0 else sc2
            if target.button(f"➕{s}"):
                if s not in st.session_state.my_btns: st.session_state.my_btns.append(s)
                st.rerun()

        st.divider()
        # 신호 버튼 리스트
        for b in st.session_state.my_btns:
            if st.button(f"📍 {b}"):
                st.session_state.message = f"📍 {b} !!"

# 4. 반주자 화면 (패드 최적화: 신호창 상단 고정)
else:
    st.markdown(f'<div class="musician-header"><h1>{st.session_state.message}</h1></div>', unsafe_allow_html=True)
    st.write("##") # 신호창 자리를 위한 공백
    st.write("##")
    
    if st.session_state.sheets:
        # 반주자용 페이지 이동
        c1, c2 = st.columns(2)
        if c1.button("◀ 이전"): st.session_state.page = max(0, st.session_state.page - 1)
        if c2.button("다음 ▶"): st.session_state.page = min(len(st.session_state.sheets)-1, st.session_state.page + 1)
        
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

  
     
