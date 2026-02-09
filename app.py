import streamlit as st

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 찬양팀 스마트 보드", layout="wide")

# 실시간 상태 저장 (메시지, 악보, 커스텀 버튼)
if 'message' not in st.session_state:
    st.session_state.message = "현재 대기 중..."
if 'sheet_music' not in st.session_state:
    st.session_state.sheet_music = None
if 'custom_buttons' not in st.session_state:
    st.session_state.custom_buttons = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

st.title("🎵 대흥교회 찬양팀 실시간 소통 시스템")

# 2. 사이드바 역할 선택
user_role = st.sidebar.radio("📢 내 역할 선택", ["인도자", "반주자/싱어"])

if user_role == "인도자":
    st.header("🎮 인도자 컨트롤 패널")
    
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.subheader("📸 악보 업로드 (캡처본)")
        uploaded_file = st.file_uploader("악보 사진을 선택하세요", type=["jpg", "png", "jpeg"])
        if uploaded_file:
            st.session_state.sheet_music = uploaded_file
        
        if st.session_state.sheet_music:
            st.image(st.session_state.sheet_music, caption="공유 중인 악보", use_container_width=True)

    with col_right:
        st.subheader("🛠️ 신호 버튼 만들기")
        # 찬송가 6절 같은 거 대비해서 즉석에서 버튼 이름 입력!
        new_btn = st.text_input("새 버튼 이름 (예: 6절로, 전주만)", placeholder="이름 입력 후 엔터")
        if st.button("➕ 버튼 추가") and new_btn:
            if new_btn not in st.session_state.custom_buttons:
                st.session_state.custom_buttons.append(new_btn)
        
        st.divider()
        st.subheader("📢 신호 보내기 (클릭!)")
        # 생성된 버튼들을 화면에 배치
        for btn_name in st.session_state.custom_buttons:
            if st.button(btn_name, use_container_width=True):
                st.session_state.message = f"📍 {btn_name} !!"
        
        if st.button("🛑 즉시 멈춤", type="primary", use_container_width=True):
            st.session_state.message = "🛑 즉시 멈춤!!"

else:
    # --- 반주자 모드 ---
    # 신호를 화면 맨 위에 악보를 가리지 않으면서도 아주 강렬하게 표시!
    st.markdown(f"""
        <div style="background-color:#ff4b4b; padding:15px; border-radius:10px; text-align:center; position:fixed; top:50px; left:20%; width:60%; z-index:100; border: 5px solid white; box-shadow: 0px 4px 15px rgba(0,0,0,0.3);">
            <h1 style="color:white; font-size:45px; margin:0;">{st.session_state.message}</h1>
        </div>
        <div style="margin-top:120px;"></div>
    """, unsafe_allow_html=True)
    
    if st.session_state.sheet_music:
        st.subheader("🎹 반주자용 악보")
        # 인도자가 버튼을 누르면 악보 테두리가 번쩍이게 강조!
        st.image(st.session_state.sheet_music, use_container_width=True)
    else:
        st.info("인도자가 악보를 올릴 때까지 기다려주세요.")
       
   
  
