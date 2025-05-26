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
    if "editor_style" not in st.session_state:
        st.session_state["editor_style"] = {
            "label_color": "#ffffff",
            "label_size": "16px",
            "heading_color": "#ffcc00",
            "heading_size": "24px"
        }

    editor_style = st.session_state["editor_style"]

    st.markdown("<h2>クイズ編集モード</h2>", unsafe_allow_html=True)

    with st.expander("⚙️ 編集画面のスタイル設定", expanded=False):
        label_color = st.text_input("ラベルの色（例: #ffffff）", editor_style["label_color"], key="editor_label_color")
        label_size = st.text_input("ラベルのサイズ（例: 16px）", editor_style["label_size"], key="editor_label_size")
        heading_color = st.text_input("見出しの色", editor_style["heading_color"], key="editor_heading_color")
        heading_size = st.text_input("見出しのサイズ", editor_style["heading_size"], key="editor_heading_size")

        if st.button("🎨 スタイルを更新"):
            st.session_state["editor_style"] = {
                "label_color": label_color,
                "label_size": label_size,
                "heading_color": heading_color,
                "heading_size": heading_size
            }
            st.success("✅ 編集画面のスタイルを更新しました！")
            st.rerun()

    def styled_label(text):
        return f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>{text}</label>"

    for idx, q in enumerate(st.session_state["quiz_data"]):
        st.markdown(
            f"<h3 style='color:{editor_style['heading_color']}; font-size:{editor_style['heading_size']};'>問題 {idx + 1}</h3>",
            unsafe_allow_html=True
        )

        st.markdown(styled_label("問題を編集:"), unsafe_allow_html=True)
        question_text = st.text_input("", q["question"], key=f"question_{idx}")

        options = []
        for i in range(len(q["options"])):
            st.markdown(styled_label(f"選択肢 {i+1}:"), unsafe_allow_html=True)
            options.append(st.text_input("", q["options"][i], key=f"option_{idx}_{i}"))

        st.markdown(styled_label("正解を選択:"), unsafe_allow_html=True)
        answer = st.selectbox("", options, index=q["options"].index(q["answer"]), key=f"answer_{idx}")

        st.markdown(styled_label("画像URLを編集:"), unsafe_allow_html=True)
        image_url = st.text_input("", q["image_url"], key=f"image_url_{idx}")

        st.markdown(styled_label("解説を編集:"), unsafe_allow_html=True)
        explanation = st.text_area("", q.get("explanation", ""), key=f"explanation_{idx}")

        st.markdown(styled_label("点数を設定:"), unsafe_allow_html=True)
        points = st.number_input("", min_value=1, max_value=100, value=q["points"], key=f"points_{idx}")

        style = q.get("style", {})
        st.markdown(styled_label("問題文の色（例: #ffffff）"), unsafe_allow_html=True)
        question_color = st.text_input("", style.get("question_color", "#ffffff"), key=f"q_color_{idx}")

        st.markdown(styled_label("問題文のサイズ（例: 24px）"), unsafe_allow_html=True)
        question_size = st.text_input("", style.get("question_size", "24px"), key=f"q_size_{idx}")

        st.markdown(styled_label("解説の色"), unsafe_allow_html=True)
        explanation_color = st.text_input("", style.get("explanation_color", "#ffffff"), key=f"e_color_{idx}")

        st.markdown(styled_label("解説のサイズ"), unsafe_allow_html=True)
        explanation_size = st.text_input("", style.get("explanation_size", "18px"), key=f"e_size_{idx}")

        st.markdown(styled_label("正解メッセージの色"), unsafe_allow_html=True)
        answer_color = st.text_input("", style.get("answer_color", "#00ff00"), key=f"a_color_{idx}")

        st.markdown(styled_label("正解メッセージのサイズ"), unsafe_allow_html=True)
        answer_size = st.text_input("", style.get("answer_size", "28px"), key=f"a_size_{idx}")

        st.markdown(styled_label("不正解メッセージの色"), unsafe_allow_html=True)
        wrong_color = st.text_input("", style.get("wrong_color", "#ff0000"), key=f"w_color_{idx}")

        st.markdown(styled_label("不正解メッセージのサイズ"), unsafe_allow_html=True)
        wrong_size = st.text_input("", style.get("wrong_size", "28px"), key=f"w_size_{idx}")
            # 新しい問題の追加セクション
    st.markdown(
        f"<h3 style='color:{editor_style['heading_color']}; font-size:{editor_style['heading_size']};'>➕ 新しい問題を追加</h3>",
        unsafe_allow_html=True
    )

    st.markdown(styled_label("新しい問題:"), unsafe_allow_html=True)
    new_question = st.text_input("", key="new_question")

    new_options = []
    for i in range(4):
        st.markdown(styled_label(f"選択肢 {i + 1}:"), unsafe_allow_html=True)
        new_options.append(st.text_input("", key=f"new_option_{i}"))

    st.markdown(styled_label("正解:"), unsafe_allow_html=True)
    new_answer = st.selectbox("", new_options, key="new_answer")

    st.markdown(styled_label("画像URL:"), unsafe_allow_html=True)
    new_image_url = st.text_input("", key="new_image_url")

    st.markdown(styled_label("解説:"), unsafe_allow_html=True)
    new_explanation = st.text_area("", key="new_explanation")

    st.markdown(styled_label("点数を設定:"), unsafe_allow_html=True)
    new_points = st.number_input("", min_value=1, max_value=100, value=1, key="new_points")

    # スタイル設定
    st.markdown(styled_label("問題文の色"), unsafe_allow_html=True)
    new_q_color = st.text_input("", "#ffffff", key="new_q_color")

    st.markdown(styled_label("問題文のサイズ"), unsafe_allow_html=True)
    new_q_size = st.text_input("", "24px", key="new_q_size")

    st.markdown(styled_label("解説の色"), unsafe_allow_html=True)
    new_e_color = st.text_input("", "#ffffff", key="new_e_color")

    st.markdown(styled_label("解説のサイズ"), unsafe_allow_html=True)
    new_e_size = st.text_input("", "18px", key="new_e_size")

    st.markdown(styled_label("正解メッセージの色"), unsafe_allow_html=True)
    new_a_color = st.text_input("", "#00ff00", key="new_a_color")

    st.markdown(styled_label("正解メッセージのサイズ"), unsafe_allow_html=True)
    new_a_size = st.text_input("", "28px", key="new_a_size")

    st.markdown(styled_label("不正解メッセージの色"), unsafe_allow_html=True)
    new_w_color = st.text_input("", "#ff0000", key="new_w_color")

    st.markdown(styled_label("不正解メッセージのサイズ"), unsafe_allow_html=True)
    new_w_size = st.text_input("", "28px", key="new_w_size")

    if st.button("➕ 問題を追加"):
        if new_question and all(new_options) and new_answer and new_explanation:
            st.session_state["quiz_data"].append({
                "question": new_question,
                "options": new_options,
                "answer": new_answer,
                "image_url": new_image_url,
                "explanation": new_explanation,
                "points": new_points,
                "style": {
                    "question_color": new_q_color,
                    "question_size": new_q_size,
                    "explanation_color": new_e_color,
                    "explanation_size": new_e_size,
                    "answer_color": new_a_color,
                    "answer_size": new_a_size,
                    "wrong_color": new_w_color,
                    "wrong_size": new_w_size
                }
            })
            save_quiz_data()
            st.success("✅ 新しい問題を追加しました！")
        else:
            st.error("⚠️ 必須項目をすべて入力してください！")


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

    if st.button("🔙 最初の画面に戻る"):
        st.session_state["edit_mode"] = False
        st.session_state["quiz_started"] = False
        st.rerun()
