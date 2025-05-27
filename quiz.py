import streamlit as st
import json
from pathlib import Path
# データ保存関数
def save_quiz_data():
    with open("quiz_data.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state["quiz_data"], f, ensure_ascii=False)
# データロード関数
def load_quiz_data():
    if Path("quiz_data.json").exists():
        with open("quiz_data.json", "r", encoding="utf-8") as f:
            st.session_state["quiz_data"] = json.load(f)
# セッション初期化
if "quiz_data" not in st.session_state:
    load_quiz_data()
    if "quiz_data" not in st.session_state:
        st.session_state["quiz_data"] = [
            {
                "question": "この城の名前は？",
                "options": ["姫路城", "松本城", "大阪城", "熊本城"],
                "answer": "姫路城",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Himeji_Castle_looking_up.jpg/800px-Himeji_Castle_looking_up.jpg",
                "explanation": "姫路城は日本三名城の一つで、別名白鷺城とも呼ばれています。",
                "points": 10  # 新しい点数フィールド
            }
        ]
    for q in st.session_state["quiz_data"]:
        if "explanation" not in q:
            q["explanation"] = "解説がまだ追加されていません"
        if "points" not in q:
            q["points"] = 1  # デフォルト点数を設定
# セッション状態の初期化
for key, default in {
    "quiz_started": False,
    "score": 0,
    "current_question": 0,
    "answered": False,
    "edit_mode": False  # 編集モード
}.items():
    if key not in st.session_state:
        st.session_state[key] = default
# カスタムCSSの適用（色の変更は行いません）
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://tse2.mm.bing.net/th/id/OIP.sVqIT6owUt2ssL-TQ_iOvQHaEo?cb=iwp2&rs=1&pid=ImgDetMain");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .custom-title {
            font-size: 64px;
            font-family: "Yu Mincho", "Hiragino Mincho Pro", serif;
            text-align: center;
            color: white;
        }
        .custom-subtitle {
            font-size: 40px;
            color: white;
            margin-bottom: 20px;
            text-align: center;
        }
        .fixed-buttons {
            position: fixed;
            top: 70px;
            right: 20px;
            z-index: 1000;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        .fixed-buttons button {
            background-color: #4444FF;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 8px;
            border: 2px solid gold;
            cursor: pointer;
        }
        .fixed-buttons button:hover {
            background-color: #3333CC;
        }
    </style>
""", unsafe_allow_html=True)
# ボタンのコールバック関数
def toggle_edit_mode():
    st.session_state["edit_mode"] = not st.session_state["edit_mode"]
    st.rerun()
def back_to_start():
    st.session_state["edit_mode"] = False
    st.session_state["quiz_started"] = False
    st.rerun()
def start_quiz():
    st.session_state["quiz_started"] = True
    st.rerun()
# 固定ボタンの表示
st.markdown("""
    <div class="fixed-buttons">
        <button onClick="toggle_edit_mode()">🔧 編集モード</button>
        <button onClick="back_to_start()">🔙 最初の画面</button>
    </div>
    <script>
        function toggle_edit_mode() {
            Streamlit.setComponentValue("toggle_edit_mode");
        }
        function back_to_start() {
            Streamlit.setComponentValue("back_to_start");
        }
    </script>
""", unsafe_allow_html=True)
# Streamlitのイベントハンドラを設定
if "toggle_edit_mode" in st.session_state:
    toggle_edit_mode()
    st.session_state.pop("toggle_edit_mode")
if "back_to_start" in st.session_state:
    back_to_start()
    st.session_state.pop("back_to_start")
# 最初の画面
if not st.session_state["quiz_started"] and not st.session_state["edit_mode"]:
    st.markdown('<div class="custom-title">デジタルクイズ</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">クイズを解いてデジタル機器について学ぼう！</div>', unsafe_allow_html=True)
    if st.button("▶️ クイズを開始"):
        start_quiz()
# クイズのページ
if st.session_state["quiz_started"] and not st.session_state["edit_mode"]:
    question_index = st.session_state["current_question"]
    if question_index < len(st.session_state["quiz_data"]):
        question = st.session_state["quiz_data"][question_index]
        # 画像表示（エラー対策付き）
        if question.get("image_url"):
            try:
                st.image(question["image_url"], width=600)
            except Exception:
                st.warning("画像の読み込みに失敗しました。")
        # 問題文の表示（色は変更しません）
        st.markdown(f"<p style='color:white; font-size:24px;'><strong>問題: {question['question']}</strong></p>", unsafe_allow_html=True)
        if not st.session_state["answered"]:
            for option in question["options"]:
                if st.button(option, key=f"option_{option}"):
                    st.session_state["selected_option"] = option
                    st.session_state["answered"] = True
        if st.session_state["answered"]:
            selected_option = st.session_state["selected_option"]
            if selected_option == question["answer"]:
                # スコア加算は一回のみ確実に実行
                if "score_updated" not in st.session_state or not st.session_state["score_updated"]:
                    st.session_state["score"] += question["points"]  # 正解時にのみ加算
                    st.session_state["score_updated"] = True  # 加算済みフラグを設定
                st.markdown("<h2 style='color:green;'>🎉 正解！</h2>", unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='color:red;'>❌ 不正解！</h2>", unsafe_allow_html=True)
          
            st.markdown(f"<p style='color:white; font-size:20px; margin-top:10px;'>解説: {question['explanation']}</p>", unsafe_allow_html=True)
            if st.button("次の問題へ"):
                st.session_state["current_question"] += 1
                st.session_state["answered"] = False
                st.session_state["score_updated"] = False  # フラグをリセット
                st.session_state.pop("selected_option", None)
                st.rerun()
    else:
        total_questions = len(st.session_state["quiz_data"])  # 全問題数を取得
        st.markdown("<h1>クイズ終了！🎉</h1>", unsafe_allow_html=True)
        total_points = sum(q["points"] for q in st.session_state["quiz_data"])  # 合計点数の計算を追加
        # スコアの表示を100点満点に変更
        st.write(f"あなたのスコア: {st.session_state['score']} / 100")
        save_quiz_data()
# 編集モードページ
elif st.session_state["edit_mode"]:
    st.markdown("<h2>クイズ編集モード</h2>", unsafe_allow_html=True)
    # 各問題の編集セクション
    for idx, q in enumerate(st.session_state["quiz_data"]):
        st.markdown(f"<h3>問題 {idx + 1}</h3>", unsafe_allow_html=True)
        question_text = st.text_input("問題を編集:", q["question"], key=f"question_{idx}")
        options = [st.text_input(f"選択肢 {i+1}:", q["options"][i], key=f"option_{idx}_{i}") for i in range(len(q["options"]))]
        answer = st.selectbox("正解を選択:", options, index=q["options"].index(q["answer"]), key=f"answer_{idx}")
        image_url = st.text_input("画像URLを編集:", q["image_url"], key=f"image_url_{idx}")
        explanation = st.text_area("解説を編集:", q.get("explanation", ""), key=f"explanation_{idx}")
        points = st.number_input("点数を設定:", min_value=1, max_value=100, value=q["points"], key=f"points_{idx}")  # 点数入力欄を追加
        if st.button(f"問題 {idx + 1} を更新", key=f"update_{idx}"):
            st.session_state["quiz_data"][idx] = {
                "question": question_text,
                "options": options,
                "answer": answer,
                "image_url": image_url,
                "explanation": explanation,
                "points": points,  # 点数を保存
            }
            save_quiz_data()
            st.success(f"✅ 問題 {idx + 1} を更新しました！")
    # 新しい問題の追加セクション
    st.markdown("### ➕ 新しい問題を追加")
    new_question = st.text_input("新しい問題:", key="new_question")
    new_options = [st.text_input(f"選択肢 {i + 1}:", key=f"new_option_{i}") for i in range(4)]
    new_answer = st.selectbox("正解:", new_options, key="new_answer")
    new_image_url = st.text_input("画像URL:", key="new_image_url")
    new_explanation = st.text_area("解説:", key="new_explanation")
    new_points = st.number_input("点数を設定:", min_value=1, max_value=100, value=1, key="new_points")  # 新しい問題の点数
    if st.button("➕ 問題を追加"):
        if new_question and all(new_options) and new_answer and new_explanation:
            st.session_state["quiz_data"].append({
                "question": new_question,
                "options": new_options,
                "answer": new_answer,
                "image_url": new_image_url,
                "explanation": new_explanation,
                "points": new_points,  # 点数を保存
            })
            save_quiz_data()
            st.success("✅ 新しい問題を追加しました！")
        else:
            st.error("⚠️ 必須項目をすべて入力してください！")
    # 最初の画面に戻るボタン
    if st.button("🔙 最初の画面に戻る"):
        back_to_start()
