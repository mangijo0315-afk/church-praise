import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소 초기화 (유실 방지)
keys = {
    'message_list': [], 
    'sheets': [], 
    'page': 0, 
    'permanent_storage': {}, 
    'temp_storage': {},
}
for key, default in keys.items():
    if key not in st.session_state:
        st.session_state[key] = default

default_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# 3. 페이지 이동 함수
def move_page(delta):
    if st.session_state.sheets:
        st.session_state.page = (st.session_state.page + delta) % len(st.session_state.sheets)

# 4. 스와이프 감지 로직 (자바스크립트)
if st.session_state.sheets:
    swipe_js = """
    <script>
    var startX;
    const doc = window.parent.document;
    doc.addEventListener('touchstart', function(e) { startX = e.touches[0].clientX; }, false);
    doc.addEventListener('touchend', function(e) {
        var endX = e.changedTouches[0].clientX;
        var diffX = startX - endX;
        if (Math.abs(diffX) > 70) { 
            if (diffX > 0) window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'next'}, '*');
            else window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'prev'}, '*');
        }
    }, false);
    </script>
    """
    swipe_val = components.html(swipe_js, height=0)
    if swipe_val == 'next': move_page(1); st.rerun()
    if swipe_val == 'prev': move_page(-1); st.rerun()

# 5. 디자인 (CSS)
st.markdown("""
    <style>
    .home-icon { position: fixed; top: 10px; right: 20px; font-size: 30px; z-index: 2000; }
    .signal-box { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px; border: 4px solid white; }
    .nav-btn button { height: 80px !important; font-size: 30px !important; background-color: #f0f2f6 !important; border-radius: 15px !important; border: 2px solid #ccc !important; }
    .stButton>button { width: 100%; font-weight: bold; border-radius: 12px; }
    </style>
    <div class="home-icon">🏠</div>
""", unsafe_allow_html=True)

# 6. 사이드바 (역할 및 저장소)
user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

with st.sidebar.expander("💾 설정 저장 및 관리", expanded=True):
    st.subheader("📂 장기 저장 목록")
    if st.session_state.permanent_storage:
        for song, data in st.session_state.permanent_storage.items():
            st.info(f"📌 **{song}**\n: {', '.join(data['btns'])}")
    else:
        st.write("저장된 곡이 없습니다.")
    
    st.divider()
    if st.button("🔄 전체 데이터 초기화"):
        st.session_state.permanent_storage = {}
        st.session_state.temp_storage = {}
        st.session_state.sheets = []
        st.rerun()

# 7. 메인 화면 로직
if user_role == "인도자":
    st.title("🎮 인도자 센터")

    if st.session_state.sheets:
        cur_file = st.session_state.sheets[st.session_state.page]
        song_name = cur_file.name.split('.')[0]
        current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "대기 중"

        # [1순위: 이동 버튼]
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.button("◀ PREV", key="ind_prev", on_click=move_page, args=(-1,))
        c2.button("NEXT ▶", key="ind_next", on_click=move_page, args=(1,))
        st.markdown('</div>', unsafe_allow_html=True)

        # [2순위: 빨간 신호 배너]
        st.markdown(f'<div class="signal-box"><h2>📢 현재 신호: {current_msg}</h2></div>', unsafe_allow_html=True)

        # [3순위: 악보 및 컨트롤러]
        col_left, col_right = st.columns([2.5, 1.2])
        with col_left:
            st.subheader(f"📄 {song_name}")
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
            custom = st.session_state.permanent_storage.get(song_name, {}).get("btns", st.session_state.temp_storage.get(song_name, []))
            for b in (default_btns + custom):
                if st.button(f"📍 {b}", key=f"send_{b}"):
                    st.session_state.message_list.append(f"📍 {b} !!"); st.rerun()
            
            st.divider()
            if st.button("💾 이 곡 영구 저장"):
                btns = st.session_state.temp_storage.get(song_name, [])
                st.session_state.permanent_storage[song_name] = {"btns": btns, "date": datetime.now().strftime("%m/%d")}
                st.success("저장 완료!")
    else:
        uploaded = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if uploaded: st.session_state.sheets = uploaded; st.rerun()

# 8. 반주자 화면
else:
    st.title("🎹 반주자/싱어 화면")
    if st.session_state.sheets:
        current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "준비 중"

        # [1순위: 이동 버튼]
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        bc1, bc2 = st.columns(2)
        bc1.button("◀ PREV", key="ban_prev", on_click=move_page, args=(-1,))
        bc2.button("NEXT ▶", key="ban_next", on_click=move_page, args=(1,))
        st.markdown('</div>', unsafe_allow_html=True)

        # [2순위: 빨간 신호 배너]
        st.markdown(f'<div class="signal-box"><h1 style="font-size:60px; margin:0;">{current_msg}</h1></div>', unsafe_allow_html=True)

        # [3순위: 악보]
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
    else:
        st.info("인도자가 악보를 올릴 때까지 대기 중...")
