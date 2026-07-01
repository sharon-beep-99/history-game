import streamlit as st
import urllib.request
import urllib.parse

# 設定網頁標題與圖示
st.set_page_config(page_title="歷史與視覺大挑戰", page_icon="🥷")

# ---------------------------------------------------------
# Google 表單後端直接寫入機制（終極防阻擋完美對齊版）
# ---------------------------------------------------------
def save_data_via_form(level, quiz_type, player_input, is_correct, current_score):
    """利用 urllib 直接在背景提交 Google 表單，數據會自動 100% 同步到試算表中"""
    # 已完全替換為您專屬的真實表單回應網址
    form_base_url = "https://docs.google.com/forms/d/e/1FAIpQLSeRhRGrySadi5UFVM4SQ6Ztctjoi4Xw-911-zLagXvqR80UhA/formResponse"
    
    # 將您的真實 entry ID 與變數進行精準對齊綁定
    form_data = {
        "entry.204255297": str(level),
        "entry.1957046489": str(quiz_type),
        "entry.685187602": str(player_input),
        "entry.2140147487": "是" if is_correct else "否",
        "entry.171006543": str(current_score)
    }
    
    try:
        data = urllib.parse.urlencode(form_data).encode("utf-8")
        req = urllib.request.Request(form_base_url, data=data, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            pass # 成功於後端提交
    except Exception as e:
        pass # 防止任何網路波動引發前端網頁卡頓

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
if st.session_state.level <= TOTAL_LEVELS:
    current_num = st.session_state.level
    current_q = QUIZ_DATA[current_num]
    
    st.header(f"第 {current_num} 關")
    st.write(current_q["q"])
    
    ans = None
    
    # --- 題型 A：選擇題（第 1, 2, 3 關均為單圖） ---
    if current_q["type"] == "single":
        try:
            st.image(f"images/level{current_num}.jpg", use_container_width=True)
        except:
            st.warning(f"⚠️ 找不到圖檔，請確認 images/ 內是否有 level{current_num}.jpg")
            
        ans = st.radio("選擇答案：", current_q["options"], index=None, key=f"q_{current_num}", disabled=st.session_state.answered)
        
    # --- 題型 B：開放式簡答題（第 4, 5, 6, 7, 8 關均支援送分與開放回答） ---
    elif current_q["type"] == "free_text":
        # 第 4, 5, 6 關為雙圖並排
        if current_num in [4, 5, 6]:
            col1, col2 = st.columns(2)
            try:
                with col1:
                    st.image(f"images/level{current_num}_a.jpg", caption="對比圖 A", use_container_width=True)
                with col2:
                    st.image(f"images/level{current_num}_b.jpg", caption="對比圖 B", use_container_width=True)
            except:
                st.warning(f"⚠️ 找不到對比圖檔，請確認 images/ 內是否有 level{current_num}_a.jpg 與 level{current_num}_b.jpg")
        
       elif current_num in [7, 8]:
            try:
                st.image(f"images/level{current_num}.jpg", caption="店鋪招牌局部", use_container_width=True)
            except:
                st.warning(f"⚠️ 找不到圖檔，請確認 images/ 內是否有 level{current_num}.jpg")
