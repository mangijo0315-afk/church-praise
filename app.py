import streamlit as st
from datetime import datetime, timedelta

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소
if 'message_list' not in st.session_state: st.session_state.message_list = [] 
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
# 곡별 '확정 저장' 저장소 (오래 감)
if 'permanent_storage' not in st.session_state: st.session_state.permanent_storage = {}
# 곡별 '임시 작업' 저장소 (3일 뒤 만료 시뮬레이션용)
if 'temp_storage' not in st.session_state: st.session_state.temp_storage = {}

default_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# 기능 함수
def add_msg(msg): st.session_state.message_list.append(msg)
def move_page(delta):
    new_page = st.session_state.page + delta
    if 0 <= new_page < len(st.session_state.sheets): st.session_state.page = new_page

# 선택한 것만 영구 저장하는 함수
def save_to_permanent(song_name):
    if song_name in st.session_state.temp_storage:
        st.session_state.permanent_storage[song_name] = {
            "btns": st.session_state.temp_storage[song_name],
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        st.success(f"✅ '{song_name}' 설정이 장기 저장소에 등록되었습니다!")

# 3. 디자인 (CSS)
st.markdown("""
    <style>
    .home-icon { position: fixed; top: 10px; right: 20px; font-size: 30px; z-index: 2000; }
    .nav-btn button { height: 75px !important; font-size: 26px !important; background-color: #f0f2f6 !important; border-radius: 12px !important; }
    .signal-box { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px; border: 4px solid white; }
    .stButton>button { width: 100%; font-weight: bold; }
    </style>
    <div class="home-icon">🏠</div>
""", unsafe_allow_html=True)

# 4. 사이드바 (장기 저장소 확인)
user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

with st.sidebar.expander("💾 장기 저장 목록 (영구)", expanded=True):
    if st.session_state.permanent_storage:
        for song, data in st.session_state.permanent_storage.items():
            st.info(f"📌 **{song}** ({data['date']})\n: {', '.join(data['btns'])}")
    else:
        st.write("오래 보관된 곡이 없습니다.")

with st.sidebar.expander("⏱️ 임시 작업 중 (3일 뒤 삭제)"):
    for song in st.session_state.temp_storage.keys():
        if song not in st.session_state.permanent_storage:
            st.caption(f"⏳ {song} (편집 중...)")

# 5. 인도자 화면
if user_role == "인도자":
    st.title("🎮 인도자 센터")
    current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "대기 중"
    st.markdown(f'<div class="signal-box"><h2>📢 현재 신호: {current_msg}</h2></div>', unsafe_allow_html=True)

    if st.session_state.sheets:
        cur_file = st.session_state.sheets[st.session_state.page]
        song_name = cur_file.name.split('.')[0]
        
        # 버튼/악보 레이아웃
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button(f"◀ 이전", on_click=move_page, args=(-1,))
        c2.button(f"다음 ▶", on_click=move_page, args=(1,))
        st.markdown('</div>', unsafe_allow_html=True)

        col_left, col_right = st.columns([2.5, 1.2])
        with col_left:
            st.subheader(f"📄 현재 곡: {song_name}")
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
                        st.session_state.temp_storage[song_name].append(s)
                        st.rerun()

            st.divider()
            st.subheader("📢 신호 전송")
            # 영구 저장된 게 있으면 그걸 쓰고, 없으면 임시 작업용 버튼 사용
            saved_custom = st.session_state.permanent_storage.get(song_name, {}).get("btns", st.session_state.temp_storage.get(song_name, []))
            song_btns = default_btns + saved_custom
            for b in song_btns:
                st.button(f"📍 {b}", key=f"send_{b}", on_click=add_msg, args=(f"📍 {b} !!",))
            
            st.divider()
            # [핵심] 사용자가 직접 눌러야만 영구 저장!
            if st.button("💾 이 곡의 설정 '영구 저장'"):
                save_to_permanent(song_name)
    else:
        uploaded = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if uploaded: st.session_state.sheets = uploaded; st.rerun()

# 6. 반주자 화면
else:
    if st.session_state.sheets:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        btn_col1, btn_col2 = st.columns(2)
        btn_col1.button("◀ PREV", on_click=move_page, args=(-1,))
        btn_col2.button("NEXT ▶", on_click=move_page, args=(1,))
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="signal-box"><h1 style="font-size:60px; margin:0;">{current_msg}</h1></div>', unsafe_allow_html=True)
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
