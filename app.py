import streamlit as st
from datetime import datetime
import streamlit.components.v1 as components

# 1. 앱 설정
st.set_page_config(page_title="대흥교회 스마트 보드", layout="wide")

# 2. 데이터 저장소
if 'message_list' not in st.session_state: st.session_state.message_list = [] 
if 'sheets' not in st.session_state: st.session_state.sheets = []
if 'page' not in st.session_state: st.session_state.page = 0
if 'permanent_storage' not in st.session_state: st.session_state.permanent_storage = {}
if 'temp_storage' not in st.session_state: st.session_state.temp_storage = {}

default_btns = ["𝄇 후렴", "🌉 브릿지", "🔚 엔딩"]

# 페이지 이동 함수
def move_page(delta):
    if st.session_state.sheets:
        st.session_state.page = (st.session_state.page + delta) % len(st.session_state.sheets)

# 3. 스와이프(Swipe) 감지 자바스크립트
# 악보 영역에서 손가락을 왼쪽/오른쪽으로 밀면 페이지가 넘어가도록 설정
components.html(
    f"""
    <script>
    var startX;
    const doc = window.parent.document;
    doc.addEventListener('touchstart', function(e) {{
        startX = e.touches[0].clientX;
    }}, false);

    doc.addEventListener('touchend', function(e) {{
        var endX = e.changedTouches[0].clientX;
        var diffX = startX - endX;

        if (Math.abs(diffX) > 100) {{ // 100픽셀 이상 밀었을 때 작동
            if (diffX > 0) {{
                // 왼쪽으로 밀기 -> 다음 장
                window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'next'}}, '*');
            }} else {{
                // 오른쪽으로 밀기 -> 이전 장
                window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'prev'}}, '*');
            }}
        }}
    }}, false);
    </script>
    """,
    height=0,
)

# 4. 디자인 (CSS)
st.markdown("""
    <style>
    .home-icon { position: fixed; top: 10px; right: 20px; font-size: 30px; z-index: 2000; }
    .signal-box { background-color: #ff4b4b; color: white; padding: 20px; border-radius: 15px; text-align: center; margin-bottom: 15px; border: 4px solid white; }
    .stButton>button { width: 100%; font-weight: bold; height: 60px; border-radius: 12px; }
    /* 악보 영역 강조 */
    .sheet-container { border: 2px solid #eee; border-radius: 20px; padding: 10px; background: white; }
    </style>
    <div class="home-icon">🏠</div>
""", unsafe_allow_html=True)

user_role = st.sidebar.radio("📢 역할 선택", ["인도자", "반주자/싱어"])

# 5. 인도자 화면
if user_role == "인도자":
    st.title("🎮 인도자 센터")
    current_msg = st.session_state.message_list[-1] if st.session_state.message_list else "대기 중"
    st.markdown(f'<div class="signal-box"><h2>📢 현재 신호: {current_msg}</h2></div>', unsafe_allow_html=True)

    if st.session_state.sheets:
        cur_file = st.session_state.sheets[st.session_state.page]
        song_name = cur_file.name.split('.')[0]
        
        col_left, col_right = st.columns([2.5, 1.2])
        with col_left:
            st.subheader(f"📄 {song_name} ({st.session_state.page + 1}/{len(st.session_state.sheets)})")
            st.caption("👈 왼쪽/오른쪽으로 밀어서(Swipe) 악보를 넘기세요")
            with st.container():
                st.image(cur_file, use_container_width=True)

        with col_right:
            st.subheader("➕ 버튼 추가 (터치)")
            samples = ["1절로", "2절로", "3절로", "한 키 업", "전주만", "드럼만", "잔잔하게"]
            sc1, sc2 = st.columns(2)
            for i, s in enumerate(samples):
                target = sc1 if i % 2 == 0 else sc2
                if target.button(f"➕ {s}", key=f"add_{s}"):
                    if song_name not in st.session_state.temp_storage: st.session_state.temp_storage[song_name] = []
                    if s not in st.session_state.temp_storage[song_name]:
                        st.session_state.temp_storage[song_name].append(s); st.rerun()

            st.divider()
            st.subheader("📢 신호 전송 (터치)")
            saved_custom = st.session_state.permanent_storage.get(song_name, {}).get("btns", st.session_state.temp_storage.get(song_name, []))
            for b in (default_btns + saved_custom):
                if st.button(f"📍 {b}", key=f"send_{b}"):
                    st.session_state.message_list.append(f"📍 {b} !!")
                    st.rerun()
            
            st.divider()
            if st.button("💾 이 곡 영구 저장"):
                btns = st.session_state.temp_storage.get(song_name, [])
                st.session_state.permanent_storage[song_name] = {"btns": btns, "date": datetime.now().strftime("%m/%d")}
                st.success("저장 완료!")
    else:
        uploaded = st.file_uploader("악보 업로드", accept_multiple_files=True)
        if uploaded: st.session_state.sheets = uploaded; st.rerun()

# 6. 반주자 화면
else:
    if st.session_state.sheets:
        st.markdown(f'<div class="signal-box"><h1 style="font-size:60px; margin:0;">{current_msg}</h1></div>', unsafe_allow_html=True)
        st.image(st.session_state.sheets[st.session_state.page], use_container_width=True)
