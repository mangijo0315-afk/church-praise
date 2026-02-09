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
      
