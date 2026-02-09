import streamlit as st

# 1. 앱 설정 (화면을 넓게 쓰게 설정했어!)
st.set_page_config(page_title="대흥교회 찬양팀", layout="wide")

# 실시간 신호 저장용 (노트북 켜져 있는 동안 유지)
if 'message' not in st.session_state:
    st.session_state.message = "현재 대기 중..."

# 2. 역할 선택 (사이드바)
# 왼쪽 메뉴가 안 보이면 화살표 '>'를 눌러봐!
user_role = st.sidebar.radio("📢 내 역할 선택", ["인도자", "반주자/싱어"])

if user_role == "인도자":
    st.title("🎮 인도자 컨트롤 패널")
    
    # 인도자는 왼쪽엔 악보, 오른쪽엔 버튼을 배치!
    col_sheet, col_btn = st.columns([2, 1])
    
    with col_sheet:
        st.subheader("🎼 오늘 찬양 악보")
        # 여기에 악보 이미지 주소를 넣으면 돼! 일단 샘플 이미지 넣어둘게.
        st.image("https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcM9Yk%2FbtqCHvI4K5x%2FE7Hkk4KkKkGkHkKkGkHkKk%2Fimg.jpg", caption="악보 주소를 넣으면 여기에 떠!")

    with col_btn:
        st.subheader("📢 신호 보내기")
        if st.button("𝄇 후렴 다시", use_container_width=True):
            st.session_state.message = "🔄 후렴구부터 다시!"
        if st.button("🎙️ 가사 처음부터", use_container_width=True):
            st.session_state.message = "⏮️ 처음 가사로!"
        if st.button("🌉 브릿지로", use_container_width=True):
            st.session_state.message = "🌉 브릿지 파트로!"
        if st.button("🔚 엔딩 준비", use_container_width=True):
            st.session_state.message = "🔚 마지막 절 하고 끝!"
        if st.button("🛑 즉시 멈춤", type="primary", use_container_width=True):
            st.session_state.message = "🛑 즉시 멈춰주세요!"

    st.divider()
    st.info(f"전달된 메시지: {st.session_state.message}")

else:
    # 3. 반주자 모드 (악보를 화면 꽉 차게!)
    st.title("🎹 반주자용 모니터")
    
    # 인도자가 보낸 신호를 화면 맨 위에 엄청 크게!
    st.markdown(f"""
        <div style="background-color:#ff4b4b; padding:20px; border-radius:10px; text-align:center;">
            <h1 style="color:white; font-size:50px;">{st.session_state.message}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("🎼 큰 악보 보기")
    # 반주자님은 악보가 커야 하니까 이미지 출력!
    st.image("https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbcM9Yk%2FbtqCHvI4K5x%2FE7Hkk4KkKkGkHkKkGkHkKk%2Fimg.jpg")
  
   


  
