import streamlit as st
from st_ga import track_ga

<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-SQSJPZ9SW9"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());

  gtag('config', 'G-SQSJPZ9SW9');
</script>

# 設定網頁標題與圖示
st.set_page_config(page_title="歷史與視覺大挑戰", page_icon="🥷")

# ---------------------------------------------------------
# Google Analytics (GA4) 套件追蹤初始化
# ---------------------------------------------------------
GA_ID = "G-SQSJPZ9SW9"
track_ga(GA_ID)

# ---------------------------------------------------------
# 1. 核心設定：8 道關卡腳本與配分 (4~8關皆為開放送分題)
# ---------------------------------------------------------
QUIZ_DATA = {
    1: {"type": "single", "q": "第一關：這個旗幟可能代表甚麼？", "options": ["日本國旗", "荷蘭東印度公司旗幟", "葡萄牙國旗", "明代商船日紋旗"], "ans": "明代商船日紋旗", "points": 10},
    2: {"type": "single", "q": "第二關：畫卷末段「校閱」的場景中，可以與明代戚家軍的陣法相對應。以上圖片中所使用的武器名稱為？", "options": ["長槍", "旗幟", "大刀", "狼筅"], "ans": "狼筅", "points": 10},
    3: {"type": "single", "q": "第三關：圖片中兵士所使用的武器名稱為？", "options": ["大砲", "佛郎機砲", "長槍", "棍棒"], "ans": "長槍", "points": 10},
    4: {"type": "free_text", "q": "第四關：比較這兩張圖，你觀察到何創時本清明上河圖有哪些獨特之處呢？（送分題-有作答即有分數）", "ans": "專家觀察參考：屏風改為立軸、人物姿勢、建築樣式、傢俱配置", "points": 15},
    5: {"type": "free_text", "q": "第五關：比較這兩張圖，你觀察到何創時本清明上河圖有哪些獨特之處呢？（送分題-有作答即有分數）", "ans": "專家觀察參考：街道正中間的畫軸內容、街道人物的樣貌、衣紋的紋飾", "points": 15},
    6: {"type": "free_text", "q": "第六關：比較這兩張圖，你觀察到何創時本清明上河圖有哪些獨特之處呢？（送分題-有作答即有分數）", "ans": "專家觀察參考：掛在牆上的畫軸、建築廊柱的位置、桌案上文具的擺放方式", "points": 15},
    7: {"type": "free_text", "q": "第七關：如果是你，會為這間店鋪題寫什麼樣的招牌呢？（開放式回答-有作答即有分數）", "ans": "原本畫卷答案：灼龜", "points": 12},
    8: {"type": "free_text", "q": "第八關：如果是你，會為這間店鋪題寫什麼樣的招牌呢？（開放式回答-有作答即有分數）", "ans": "原本畫卷答案：清水綺羅錦紵", "points": 13}
}

TOTAL_LEVELS = len(QUIZ_DATA)

# 2. 初始化遊戲狀態
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'answered' not in st.session_state:
    st.session_state.answered = False

# 3. 側邊欄資訊
st.sidebar.title("🥷 歷史視覺挑戰賽")
display_level = min(st.session_state.level, TOTAL_LEVELS)
st.sidebar.write(f"目前進度：{display_level} / {TOTAL_LEVELS}")
st.sidebar.write(f"當前得分：{st.session_state.score} / 100")

# 顯示進度條
if st.session_state.level <= TOTAL_LEVELS:
    st.progress(st.session_state.level / TOTAL_LEVELS)
else:
    st.progress(1.0)

# ---------------------------------------------------------
# 遊戲關卡邏輯
# ---------------------------------------------------------
if st.session_state.level <=
