import streamlit as st
import streamlit.components.v1 as components

# 設定網頁標題與圖示
st.set_page_config(page_title="歷史與視覺大挑戰", page_icon="★")

# ---------------------------------------------------------
# Google Analytics (GA4) 數據追蹤設定
# ---------------------------------------------------------
GA_ID = "G-SQSJPZ9SW9" 

# 注入 GA4 基礎追蹤碼
ga_base_code = f"""
<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
    window.parent.dataLayer = window.parent.dataLayer || [];
    function gtag(){{window.parent.dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', '{GA_ID}');
</script>
"""
components.html(ga_base_code, height=0, width=0)

# 輔助函式：發送自訂數據與答案到 GA 後台
def track_ga_event(event_name, params):
    param_str = ", ".join([f"'{k}': '{v}'" for k, v in params.items()])
    js_code = f"""
    <script>
        window.parent.gtag('event', '{event_name}', {{{param_str}}});
    </script>
    """
    components.html(js_code, height=0, width=0)

# ---------------------------------------------------------
# 1. 核心設定：8 道關卡腳本與配分 (4~8關皆為開放送分題)
# ---------------------------------------------------------
QUIZ_DATA = {
    1: {"type": "single", "q": "第一關：這個旗幟可能代表甚麼？", "options": ["日本國旗", "荷蘭東印度公司旗幟", "葡萄牙國旗", "明代商船日紋旗"], "ans": "明代商船日紋旗", "points": 10},
    2: {"type": "single", "q": "第二關：畫卷末段「校閱」的場景中，人物排列的陣法與明代戚家軍陣法對應。以上圖片中所使用的武器名稱為？", "options": ["長槍", "旗幟", "大刀", "狼筅"], "ans": "狼筅", "points": 10},
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
        
        # 第 7, 8 關為單圖招牌題
        elif current_num in [7, 8]:
            try:
                st.image(f"images/level{current_num}.jpg", caption="店鋪招牌局部", use_container_width=True)
            except:
                st.warning(f"⚠️ 找不到圖檔，請確認 images/ 內是否有 level{current_num}.jpg")
            
        user_input = st.text_input("請輸入您的觀察或答案：", key=f"txt_{current_num}", disabled=st.session_state.answered)
        ans = user_input.strip()

    st.divider()

    # 檢查答案邏輯
    if not st.session_state.answered:
        if st.button("檢查答案"):
            if ans is None or ans == "":
                st.warning("請先輸入答案再提交喔！")
            else:
                st.session_state.answered = True
                
                # 開放式回答皆為送分題
                is_correct = True
                if current_q["type"] == "single":
                    is_correct = (ans == current_q["ans"])
                
                if is_correct:
                    st.session_state.score += current_q["points"]
                
                # 發送事件到 GA 後台
                track_ga_event(
                    event_name="player_submit_answer",
                    params={
                        "level": str(current_num),
                        "quiz_type": current_q["type"],
                        "player_input": str(ans).replace("'", "\\'"),
                        "is_correct": str(is_correct),
                        "current_total_score": str(st.session_state.score)
                    }
                )
                st.rerun()
    else:
        # 顯示對錯提示與參考解析
        if current_q["type"] == "single":
            if ans == current_q["ans"]:
                st.success(f"🎉 太厲害了！答案確實是【{current_q['ans']}】！")
            else:
                st.error(f"❌ 可惜錯囉！正確答案是【{current_q['ans']}】。")
        else:
            # 簡答送分題的回饋畫面
            st.success(f"🎉 感謝您的分享！這是一題精彩的開放觀察題。")
            st.info(f"💡 【{current_q['ans']}】")
            
        # 5秒自動換關計時器
        st.markdown(
            """
            <div style="padding:10px; background-color:#f1f3f4; border-radius:5px; margin:10px 0;">
                ⏳ <span id="countdown">5</span> 秒後自動前往下一關...
            </div>
            <script>
            var count = 5;
            var counter = setInterval(timer, 1000);
            function timer() {
                count = count - 1;
                if (count <= 0) {
                    clearInterval(counter);
                    const buttons = window.parent.document.querySelectorAll('button');
                    for (const button of buttons) {
                        if (button.textContent.includes('自動下一關')) {
                            button.click();
                            break;
                        }
                    }
                    return;
                }
                window.parent.document.getElementById("countdown").innerHTML = count;
            }
            </script>
            """,
            unsafe_allow_html=True
        )

        if st.button("自動下一關（若未跳轉請點此）", key="auto_next_btn"):
            st.session_state.answered = False
            st.session_state.level += 1
            st.rerun()

# ---------------------------------------------------------
# 結算畫面
# ---------------------------------------------------------
else:
    if st.session_state.score >= 60:
        st.balloons()
    else:
        st.snow()
        
    st.header("🎊 挑戰完成！")
    st.write(f"你在這場歷史與視覺探索中獲得了 **{st.session_state.score}** 分（總分 100）。")
    
    track_ga_event(
        event_name="game_finished",
        params={
            "final_score": str(st.session_state.score)
        }
    )
    
    if st.session_state.score >= 80:
        st.success("太神了！你簡直是歷史與鑑定大師，觀察力驚人！")
    elif st.session_state.score >= 60:
        st.info("很棒的表現！你對歷史圖像與史實細節有很強的直覺。")
    else:
        st.warning("這些題目相當考驗眼力與史實功底，分數拿這樣已經不容易了，再接再厲！")
    
    if st.button("重新開始挑戰"):
        st.session_state.level = 1
        st.session_state.score = 0
        st.session_state.answered = False
        st.rerun()
