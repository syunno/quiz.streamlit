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
                "points": 10,
                "style": {
                    "question_color": "#ffffff",
                    "question_size": "24px",
                    "explanation_color": "#ffffff",
                    "explanation_size": "18px",
                    "answer_color": "#00ff00",
                    "answer_size": "28px",
                    "wrong_color": "#ff0000",
                    "wrong_size": "28px"
                }
            }
        ]
    for q in st.session_state["quiz_data"]:
        if "explanation" not in q:
            q["explanation"] = "解説がまだ追加されていません"
        if "points" not in q:
            q["points"] = 1
        if "style" not in q:
            q["style"] = {
                "question_color": "#ffffff",
                "question_size": "24px",
                "explanation_color": "#ffffff",
                "explanation_size": "18px",
                "answer_color": "#00ff00",
                "answer_size": "28px",
                "wrong_color": "#ff0000",
                "wrong_size": "28px"
            }

# セッション状態の初期化
for key, default in {
    "quiz_started": False,
    "score": 0,
    "current_question": 0,
    "answered": False,
    "edit_mode": False
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# カスタムCSSと固定ボタン
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
    <div class="fixed-buttons">
        <form action="" method="get">
            <button name="edit_mode_toggle" type="submit">🔧 編集モード</button>
        </form>
        <form action="" method="get">
            <button name="back_to_start" type="submit">🔙 最初の画面</button>
        </form>
    </div>
""", unsafe_allow_html=True)

# 編集モード切り替え処理
if "edit_mode_toggle" in st.query_params:
    st.session_state["edit_mode"] = not st.session_state["edit_mode"]
    st.query_params.clear()
    st.rerun()
if "back_to_start" in st.query_params:
    st.session_state["quiz_started"] = False
    st.session_state["edit_mode"] = False
    st.query_params.clear()
    st.rerun()
# 最初の画面
if not st.session_state["quiz_started"] and not st.session_state["edit_mode"]:
    st.markdown('<div class="custom-title">デジタルクイズ</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">クイズを解いてデジタル機器について学ぼう！</div>', unsafe_allow_html=True)
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
        st.query_params.clear()
        st.rerun()

# クイズ画面
if st.session_state["quiz_started"] and not st.session_state["edit_mode"]:
    question_index = st.session_state["current_question"]
    if question_index < len(st.session_state["quiz_data"]):
        question = st.session_state["quiz_data"][question_index]
        style = question.get("style", {})

        if question.get("image_url"):
            try:
                st.image(question["image_url"], width=600)
            except Exception:
                st.warning("画像の読み込みに失敗しました。")

        st.markdown(
            f"<p style='color:{style.get('question_color', '#ffffff')}; font-size:{style.get('question_size', '24px')};'><strong>問題: {question['question']}</strong></p>",
            unsafe_allow_html=True
        )

        if not st.session_state["answered"]:
            for option in question["options"]:
                if st.button(option, key=f"option_{option}_{question_index}"):
                    st.session_state["selected_option"] = option
                    st.session_state["answered"] = True

        if st.session_state["answered"]:
            selected_option = st.session_state["selected_option"]
            if selected_option == question["answer"]:
                if "score_updated" not in st.session_state or not st.session_state["score_updated"]:
                    st.session_state["score"] += question["points"]
                    st.session_state["score_updated"] = True
                st.markdown(
                    f"<h2 style='color:{style.get('answer_color', '#00ff00')}; font-size:{style.get('answer_size', '28px')};'>🎉 正解！</h2>",
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<h2 style='color:{style.get('wrong_color', '#ff0000')}; font-size:{style.get('wrong_size', '28px')};'>❌ 不正解！</h2>",
                    unsafe_allow_html=True
                )

            st.markdown(
                f"<p style='color:{style.get('explanation_color', '#ffffff')}; font-size:{style.get('explanation_size', '18px')};'>解説: {question['explanation']}</p>",
                unsafe_allow_html=True
            )

            if st.button("次の問題へ"):
                st.session_state["current_question"] += 1
                st.session_state["answered"] = False
                st.session_state["score_updated"] = False
                st.session_state.pop("selected_option", None)
                st.rerun()
    else:
        total_points = sum(q["points"] for q in st.session_state["quiz_data"])
        st.markdown("<h1>クイズ終了！🎉</h1>", unsafe_allow_html=True)
        st.write(f"あなたのスコア: {st.session_state['score']} / {total_points}")
        save_quiz_data()

# 編集モード
elif st.session_state["edit_mode"]:
    st.markdown("<h2>クイズ編集モード</h2>", unsafe_allow_html=True)

    for idx, q in enumerate(st.session_state["quiz_data"]):
        st.markdown(f"<h3>問題 {idx + 1}</h3>", unsafe_allow_html=True)
        question_text = st.text_input("問題を編集:", q["question"], key=f"question_{idx}")
        options = [st.text_input(f"選択肢 {i+1}:", q["options"][i], key=f"option_{idx}_{i}") for i in range(len(q["options"]))]
        answer = st.selectbox("正解を選択:", options, index=q["options"].index(q["answer"]), key=f"answer_{idx}")
        image_url = st.text_input("画像URLを編集:", q["image_url"], key=f"image_url_{idx}")
        explanation = st.text_area("解説を編集:", q.get("explanation", ""), key=f"explanation_{idx}")
        points = st.number_input("点数を設定:", min_value=1, max_value=100, value=q["points"], key=f"points_{idx}")

        style = q.get("style", {})
        question_color = st.text_input("問題文の色（例: #ffffff）", style.get("question_color", "#ffffff"), key=f"q_color_{idx}")
        question_size = st.text_input("問題文のサイズ（例: 24px）", style.get("question_size", "24px"), key=f"q_size_{idx}")
        explanation_color = st.text_input("解説の色", style.get("explanation_color", "#ffffff"), key=f"e_color_{idx}")
        explanation_size = st.text_input("解説のサイズ", style.get("explanation_size", "18px"), key=f"e_size_{idx}")
        answer_color = st.text_input("正解メッセージの色", style.get("answer_color", "#00ff00"), key=f"a_color_{idx}")
        answer_size = st.text_input("正解メッセージのサイズ", style.get("answer_size", "28px"), key=f"a_size_{idx}")
        wrong_color = st.text_input("不正解メッセージの色", style.get("wrong_color", "#ff0000"), key=f"w_color_{idx}")
        wrong_size = st.text_input("不正解メッセージのサイズ", style.get("wrong_size", "28px"), key=f"w_size_{idx}")

        if st.button(f"問題 {idx + 1} を更新", key=f"update_{idx}"):
            st.session_state["quiz_data"][idx] = {
                "question": question_text,
                "options": options,
                "answer": answer,
                "image_url": image_url,
                "explanation": explanation,
                "points": points,
                "style": {
                    "question_color": question_color,
                    "question_size": question_size,
                    "explanation_color": explanation_color,
                    "explanation_size": explanation_size,
                    "answer_color": answer_color,
                    "answer_size": answer_size,
                    "wrong_color": wrong_color,
                    "wrong_size": wrong_size
                }
            }
            save_quiz_data()
            st.success(f"✅ 問題 {idx + 1} を更新しました！")
