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
                "explanation": "姫路城は日本三名城の一つで、別名白鷺城とも呼ばれています。"
            }
        ]
    for q in st.session_state["quiz_data"]:
        if "explanation" not in q:
            q["explanation"] = "解説がまだ追加されていません"

# その他のセッション状態
for key, default in {
    "quiz_started": False,
    "score": 0,
    "current_question": 0,
    "answered": False,
    "edit_mode": False,
    "start_quiz_clicked": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# カスタムCSSと右上固定ボタン
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
        .custom-text {
            font-size: 24px;
            line-height: 1.6;
            text-align: justify;
            color: white;
        }
        h2 {
            color: white !important;
            font-family: "Yu Mincho", "Hiragino Mincho Pro", serif;
        }
        label {
            color: white !important;
            font-weight: bold;
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
    <div class="fixed-buttons">
        <form action="" method="get">
            <button name="edit_mode_toggle" type="submit">🔧 クイズ編集モード</button>
        </form>
        <form action="" method="get">
            <button name="back_to_start" type="submit">🔙 最初の画面に戻る</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# ボタン処理
if "edit_mode_toggle" in st.query_params:
    st.session_state["edit_mode"] = not st.session_state["edit_mode"]
    st.query_params.clear()
    st.rerun()

if "back_to_start" in st.query_params:
    st.session_state.clear()  # ← ここで完全リセット
    st.query_params.clear()
    st.rerun()

# タイトル
st.markdown('<div class="custom-title">デジタルクイズ</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subtitle">クイズを解いてデジタル機器について学ぼう！</div>', unsafe_allow_html=True)

# クイズ開始ボタン（最初の画面にだけ表示）
if not st.session_state["quiz_started"] and not st.session_state["edit_mode"]:
    st.markdown("""
        <form action="" method="get" style="text-align:center; margin-top: 50px;">
            <button type="submit" name="start_quiz" style="
                font-size: 36px;
                padding: 20px 60px;
                background-color: #28a745;
                color: white;
                border: 4px solid gold;
                border-radius: 12px;
                cursor: pointer;
            ">
                ▶️ クイズを開始
            </button>
        </form>
    """, unsafe_allow_html=True)

if "start_quiz" in st.query_params:
    st.session_state["quiz_started"] = True
    st.session_state["edit_mode"] = False
    st.query_params.clear()
    st.rerun()
elif not st.session_state["edit_mode"]:
    question_index = st.session_state["current_question"]
    if question_index < len(st.session_state["quiz_data"]):
        question = st.session_state["quiz_data"][question_index]

        # 画像表示（エラー対策付き）
        if question.get("image_url"):
            try:
                st.image(question["image_url"], width=600)
            except Exception:
                st.warning("画像の読み込みに失敗しました。")

        st.markdown(f"<p style='color:white; font-size:24px;'><strong>問題: {question['question']}</strong></p>", unsafe_allow_html=True)

        if not st.session_state["answered"]:
            for option in question["options"]:
                if st.button(option, key=f"option_{option}"):
                    st.session_state["selected_option"] = option
                    st.session_state["answered"] = True

        if st.session_state["answered"]:
            selected_option = st.session_state["selected_option"]
            if selected_option == question["answer"]:
                st.session_state["score"] += 1
                st.markdown("<h2 class='correct'>🎉 正解！</h2>", unsafe_allow_html=True)
            else:
                st.markdown("<h2 class='wrong'>❌ 不正解！</h2>", unsafe_allow_html=True)

            st.markdown(f"<p class='custom-text'>解説: {question['explanation']}</p>", unsafe_allow_html=True)

            if st.button("次の問題へ"):
                st.session_state["current_question"] += 1
                st.session_state["answered"] = False
                st.session_state.pop("selected_option", None)
                st.rerun()
    else:
        st.markdown("<h1>クイズ終了！🎉</h1>", unsafe_allow_html=True)
        st.write(f"あなたのスコア: {st.session_state['score']} / {len(st.session_state['quiz_data'])}")
        save_quiz_data()

# 編集モード画面
if st.session_state["edit_mode"]:
    st.markdown("<h2>クイズ編集</h2>", unsafe_allow_html=True)

    for idx, q in enumerate(st.session_state["quiz_data"]):
        st.markdown(f"<h3>問題 {idx + 1}</h3>", unsafe_allow_html=True)
        question_text = st.text_input("問題を編集:", q["question"], key=f"question_{idx}")
        options = [st.text_input(f"選択肢 {i+1}:", q["options"][i], key=f"option_{idx}_{i}") for i in range(len(q["options"]))]
        answer = st.selectbox("正解を選択:", options, index=q["options"].index(q["answer"]), key=f"answer_{idx}")
        image_url = st.text_input("画像URLを編集:", q["image_url"], key=f"image_url_{idx}")
        explanation = st.text_area("解説を編集:", q.get("explanation", ""), key=f"explanation_{idx}")

        if st.button(f"問題 {idx+1} を更新", key=f"update_{idx}"):
            st.session_state["quiz_data"][idx] = {
                "question": question_text,
                "options": options,
                "answer": answer,
                "image_url": image_url,
                "explanation": explanation
            }
            save_quiz_data()
            st.success(f"✅ 問題 {idx+1} を更新しました！")

    st.markdown("### ➕ 新しい問題を追加")
    new_question = st.text_input("新しい問題:", "", key="new_question")
    new_options = [st.text_input(f"新しい選択肢 {i+1}:", "", key=f"new_option_{i}") for i in range(4)]
    new_answer = st.selectbox("新しい正解:", new_options, key="new_answer")
    new_image_url = st.text_input("新しい画像URL:", "", key="new_image_url")
    new_explanation = st.text_area("新しい解説:", "", key="new_explanation")

    if st.button("➕ 問題を追加"):
        if new_question and all(new_options) and new_answer and new_explanation:
            st.session_state["quiz_data"].append({
                "question": new_question,
                "options": new_options,
                "answer": new_answer,
                "image_url": new_image_url,
                "explanation": new_explanation
            })
            save_quiz_data()
            st.success("✅ 新しい問題を追加しました！")
        else:
            st.error("⚠️ 問題・選択肢・解説をすべて入力してください。")

    if st.button("🔙 最初の画面に戻る（編集モード内）"):
        st.session_state.clear()
        st.rerun()
