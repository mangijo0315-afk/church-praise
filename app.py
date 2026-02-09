import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소
if 'message_list' not in st.session_state: st.session_state.message_list = [] 
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'my_btns' not in st.session_state: st.session_state.my_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# CSS: 신호창을 아까처럼 '왕 크게' 만들고 악보를 밀어내게 설정
st.markdown("""
    <style>
    .big-signal-box {
        background-color: #ff4b4b; color: white;
        padding: 20px; border-radius: 15px;
        text-align: center; margin-bottom: 10px;
        border: 5px solid white; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
    }
    .sub-signal-box {
        background-color: #ff7373; color: white;
        padding: 5px; border-radius: 8px;
        text-align: center; margin-bottom: 5px; opacity: 0.8;
    }
    .stButton>button { width: 100%; height: 55px; font-size: 18px !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

# 3. 반주자 화면 (신호창 왕 크게!)
if user_role == "반주자/싱어":
    if st.session_state.message_list:
        # 가장 최신 메시지 (왕 크게)
        st.markdown(f'<div class="big-signal-box"><h1 style="font-size:55px; margin:0;">{st.session_state.message_list[-1]}</h1></div>', unsafe_allow_html=True)
        # 그 이전 메시지들 (작게)
        if len(st.session_state.message_list) > 1:
            for m in st.session_state.message_list[-3:-1]:
                st.markdown(f'<div class="sub-signal-box">{m}</div>', unsafe_allow_html=True)
    
    if st.session_state.sheets:
        c1, c2 = st.columns(2)
        if c1.button("◀ 이전"): st.session_state.page = max(0, st.session_state.page - 1)
        if c2.button("다음 ▶"): st.session_state.page = min(len(st.session_state.sheets)-1, st.session_state.page + 1)
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

# 4. 인도자 화면 (버튼 클릭 에러 수정)
else:
    st.title("🎮 인도자 컨트롤 센터")
    
    # 상단 신호창 (인도자도 크게 확인)
    if st.session_state.message_list:
        st.error(f"현재 전송 중: {st.session_state.message_list[-1]}")
        if st.button("🔴 모든 신호 삭제 (초기화)"):
            st.session_state.message_list = []
            st.rerun()

    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        files = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if files: st.session_state.sheets = files
        if st.session_state.sheets:
            st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

    with col_right:
        st.subheader("✍️ 즉시 타이핑")
        inst_msg = st.text_input("전달할 말", key="typing_box")
        if st.button("🚀 전송하기") and inst_msg:
            st.session_state.message_list.append(f"🚨 {inst_msg}")
            st.rerun()

        st.divider()
        st.subheader("➕ 버튼 추가 (클릭!)")
        samples = ["1절로", "2절로", "3절로", "한 키 업", "전주만", "드럼만"]
        sc1, sc2 = st.columns(2)
        for i, s in enumerate(samples):
            target = sc1 if i % 2 == 0 else sc2
            # [수정] 버튼 클릭 시 상태가 즉시 반영되도록 rerun 추가
            if target.button(f"➕ {s}", key=f"sample_{s}"):
                if s not in st.session_state.my_btns:
                    st.session_state.my_btns.append(s)
                st.rerun()

        st.divider()
        st.subheader("📢 전송 버튼")
        for b in st.session_state.my_btns:
            if st.button(f"📍 {b}", key=f"send_{b}"):
                st.session_state.message_list.append(f"📍 {b} !!")
                st.rerun()
