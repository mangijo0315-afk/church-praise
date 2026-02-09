import streamlit as st

# 앱 설정
st.set_page_config(page_title="대흥교회 실시간 소통판", layout="wide")

# 가짜 데이터베이스 (버튼 누른 상태 저장)
if 'message' not in st.session_state:
    st.session_state.message = "현재 대기 중..."

st.title("🎵 실시간 찬양팀 소통 시스템")

# 사이드바 역할 선택
user_role = st.sidebar.radio("역할", ["인도자", "반주자/싱어"])

if user_role == "인도자":
    st.header("🎮 인도자 전용 버튼 (한 번만 클릭!)")
    
    # 가사 및 구간 이동 버튼들
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("𝄇 후렴 다시", use_container_width=True):
            st.session_state.message = "🔄 후렴구부터 다시 시작하세요!"
        if st.button("🎙️ 가사 처음부터", use_container_width=True):
            st.session_state.message = "⏮️ 처음 가사로 돌아갑니다!"
            
    with col2:
        if st.button("🌉 브릿지로", use_container_width=True):
            st.session_state.message = "🌉 브릿지(Bridge) 파트 진입!"
        if st.button("🎹 전주/간주", use_container_width=True):
            st.session_state.message = "🎼 악기 연주 중 (전주/간주)"

    with col3:
        if st.button("🔚 엔딩 준비", use_container_width=True):
            st.session_state.message = "🔚 마지막 절 하고 마무리!"
        if st.button("🛑 즉시 멈춤", type="primary", use_container_width=True):
            st.session_state.message = "🛑 즉시 연주를 멈춰주세요!"

    st.divider()
    st.subheader("현재 전달된 신호:")
    st.warning(st.session_state.message)

else:
    st.header("🎹 반주자/싱어 모니터")
    # 신호를 아주 크게 보여줌
    st.markdown(f"""
        <div style="background-color:#f0f2f6; padding:50px; border-radius:10px; text-align:center;">
            <h1 style="color:#ff4b4b; font-size:60px;">{st.session_state.message}</h1>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("알림 확인 완료"):
        st.session_state.message = "대기 중..."
      import streamlit as st

# 앱 설정
st.set_page_config(page_title="대흥교회 찬양팀", layout="wide")

st.title("🎵 악보 + 실시간 소통판")

# 사이드바 역할 선택
user_role = st.sidebar.radio("역할", ["인도자", "반주자/싱어"])

# --- 악보 섹션 (여기에 악보 주소를 넣으면 돼) ---
# 예시로 구글에서 가져온 악보 이미지를 넣어둘게. 나중에 네 악보 링크로 바꿔!
sheet_music_url = "https://블로그나_인터넷에_올린_네_악보_주소.jpg" 

if user_role == "인도자":
    # 화면을 반으로 나눠서 왼쪽은 악보, 오른쪽은 버튼!
    col_left, col_right = st.columns([2, 1]) 
    
    with col_left:
        st.subheader("🎼 현재 악보")
        # 실제 악보가 있다면 아래 주석(#)을 풀고 링크를 넣으면 사진이 떠!
        # st.image("https://pds.joongang.co.kr/news/component/htmlphoto_mmdata/202304/24/49622d14-b97c-4034-8c83-7c9896582570.jpg") 
        st.write("안녕! 여기에 악보 이미지를 띄울 수 있어.")

    with col_right:
        st.subheader("🎮 컨트롤")
        if st.button("𝄇 후렴 다시"): st.success("후렴 다시!")
        if st.button("🌉 브릿지로"): st.info("브릿지 이동!")
        if st.button("🔚 엔딩 준비"): st.warning("엔딩 준비!")

else:
    # 반주자 모드: 악보를 크게 띄우고 위에 알림창을 작게!
    st.error("📢 인도자 신호: 후렴구 다시 시작!!") # 신호가 여기 뜸
    st.subheader("🎹 반주자용 큰 악보")
    # st.image("네_악보_링크")
    st.write("반주자님은 여기서 악보를 크게 보면서 상단 알림을 확인하세요!")
