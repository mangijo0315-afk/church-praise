import streamlit as st
from datetime import datetime

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소
if 'message_list' not in st.session_state: st.session_state.message_list = [] 
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'permanent_storage' not in st.session_state: st.session_state.permanent_storage = {}
if 'temp_storage' not in st.session_state: st.session_state.temp_storage = {}

default_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# 기능 함수
def add_msg(msg): st.session_state.message_list.append(msg)
def move_page(delta):
    new_page = st.session_state.page + delta
    if 0 <= new_page < len(st.session_state.sheets): 
        st.session_state.page = new_page

# 3. 디자인 (CSS)
st.markdown("""
    <style>
    .home-icon { position: fixed; top: 10px; right: 20px; font-size: 30px; z-index: 2000; }
    /* 인도자/반주자 공통: 페이지 이동 버튼을 악보 위아래로 크게 */
    .nav-btn button { height: 70px !important; font-size: 24px !important; background-color: #f0f2f6 !important; border-radius: 12px !important; }
    .signal-box { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px; border: 4px solid white; }
    /* 악보 클릭 영역 강조 */
    .stImage { cursor: pointer; transition: 0.3s; }
    .stImage:active { opacity: 0.5; }
    </style>
    <div class="home-icon">🏠</div>
""", unsafe_allow_html=True)

user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

# 4. 사이드바 (저장 목록)
with st.sidebar.expander("💾 장기 저장 목록 (영구)", expanded=True):
    if st.session_state.permanent_storage:
        for song, data in st.session_state.permanent_storage.items():
            st.info(f"📌 **{song}**\n: {', '.join(data['btns'])}")
    else: st.write("저장된 곡이 없습니다.")

# 5. 인도자 화면
if user_role == "인도자":
    st.title("🎮 인도자 센터")
    current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "대기 중"
    st.markdown(f'<div class="signal-box"><h2>📢 현재 신호: {current_msg}</h2></div>', unsafe_allow_html=True)

    if st.session_state.sheets:
        cur_file = st.session_state.sheets[st.session_state.page]
        song_name = cur_file.name.split('.')[0]
        
        # [변경점] 악보 위에도 이동 버튼 배치 (터치하기 편하게)
        c1, c2 = st.columns(2)
        c1.button("◀ 이전 (Back)", key="top_prev", on_click=move_page, args=(-1,))
        c2.button("다음 (Next) ▶", key="top_next", on_click=move_page, args=(1,))

        col_left, col_right = st.columns([2.5, 1.2])
        with col_left:
            st.subheader(f"📄 {song_name}")
            # [핵심] 악보 자체를 버튼처럼 클릭 가능하게 만듦
            if st.button("🖼️ 악보 터치해서 다음 장으로 넘기기", key="img_click_btn"):
                move_page(1)
                st.rerun()
            st.image(cur_file, use_container_width=True)

        with col_right:
            st.subheader("➕ 버튼 추가")
            samples = ["1절로", "2절로", "3절로", "한 키 업", "전주만", "드럼만", "잔잔하게"]
            sc1, sc2 = st.columns(2)
            for i, s in enumerate(samples):
                target = sc1 if i % 2 == 0 else sc2
                if target.button(f"➕ {s}", key=f"add_{s}"):
                    if song_name not in st.session_state.temp_storage: st.session_state.temp_storage[song_name] = []
                    if s not in st.session_state.temp_storage[song_name]:
                        st.session_state.temp_storage[song_name].append(s); st.rerun()

            st.divider()
            st.subheader("📢 신호 전송")
            saved_custom = st.session_state.permanent_storage.get(song_name, {}).get("btns", st.session_state.temp_storage.get(song_name, []))
            for b in (default_btns + saved_custom):
                st.button(f"📍 {b}", key=f"send_{b}", on_click=add_msg, args=(f"📍 {b} !!",))
            
            st.divider()
            if st.button("💾 이 곡 영구 저장"):
                if song_name in st.session_state.temp_storage:
                    st.session_state.permanent_storage[song_name] = {"btns": st.session_state.temp_storage[song_name], "date": datetime.now().strftime("%Y-%m-%d")}
                    st.success("저장 완료!")
    else:
        uploaded = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if uploaded: st.session_state.sheets = uploaded; st.rerun()

# 6. 반주자 화면 (인도자가 넘기면 실시간으로 같이 넘어감)
else:
    if st.session_state.sheets:
        st.markdown(f'<div class="signal-box"><h1 style="font-size:60px; margin:0;">{current_msg}</h1></div>', unsafe_allow_html=True)
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)

