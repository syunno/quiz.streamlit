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
    "edit_mode": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# カスタムCSS
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
        .stButton > button {
            background-color: #0000FF;
            color: white;
            font-size: 24px;
            padding: 10px;
            border-radius: 5px;
            border: 2px solid gold;
            transition: 0.3s;
            margin-bottom: 10px;
        }
        .stButton > button:hover {
            background-color: #0000AA;
            transform: scale(1.05);
        }
        h2 {
            color: white !important;
            font-family: "Yu Mincho", "Hiragino Mincho Pro", serif;
        }
        label {
            color: white !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# タイトル
st.markdown('<div class="custom-title">デジタルクイズ</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subtitle">クイズを解いてデジタル機器について学ぼう！</div>', unsafe_allow_html=True)

# クイズ開始
if not st.session_state["quiz_started"]:
    if st.button("クイズを開始"):
        st.session_state["edit_mode"] = False
        st.session_state["quiz_started"] = True
        st.rerun()
elif not st.session_state["edit_mode"]:
    question_index = st.session_state["current_question"]
    if question_index < len(st.session_state["quiz_data"]):
        question = st.session_state["quiz_data"][question_index]
        st.image(question["image_url"], width=600)
        st.markdown(f"<p style='color:white; font-size:24px;'><strong>問題: {question['question']}</strong></p>", unsafe_allow_html=True)

        # 選択肢を白文字ボタンで表示
        if not st.session_state["answered"]:
            for option in question["options"]:
                if st.button(option, key=f"option_{option}"):
                    st.session_state["selected_option"] = option
                    st.session_state["answered"] = True

        # 回答後の処理
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
        if st.button("🔙 最初の画面に戻る"):
            st.session_state["quiz_started"] = False
            st.session_state["score"] = 0
            st.session_state["current_question"] = 0
            st.session_state["answered"] = False
            st.rerun()

# 編集モード
if st.button("🔧 クイズ編集モード"):
    st.session_state["edit_mode"] = not st.session_state["edit_mode"]
    st.rerun()

if st.session_state["edit_mode"]:
    st.markdown("<h2>クイズ編集</h2>", unsafe_allow_html=True)

    for idx, q in enumerate(st.session_state["quiz_data"]):
        st.markdown(f"### 問題 {idx + 1}")
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

        if st.button("🔙 最初の画面に戻る"):
            st.session_state["edit_mode"] = False
            st.rerun()
