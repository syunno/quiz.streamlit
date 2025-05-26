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
query_params = st.query_params
if "edit_mode_toggle" in query_params:
    st.session_state["edit_mode"] = not st.session_state["edit_mode"]
    st.set_query_params({})  # クエリパラメータをクリア
    st.experimental_rerun()
if "back_to_start" in query_params:
    st.session_state["quiz_started"] = False
    st.session_state["edit_mode"] = False
    st.set_query_params({})  # クエリパラメータをクリア
    st.experimental_rerun()
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
    if "start_quiz" in query_params:
        st.session_state["quiz_started"] = True
        st.set_query_params({})  # クエリパラメータをクリア
        st.experimental_rerun()
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
                st.experimental_rerun()
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
    # 一括スタイル設定セクションの追加
    st.markdown("<h2>一括スタイル設定</h2>", unsafe_allow_html=True)
    with st.form("bulk_style_form"):
        st.markdown(
            f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>問題文の色（例: #ffffff）</label>",
            unsafe_allow_html=True
        )
        bulk_question_color = st.text_input("", "#ffffff", key="bulk_question_color")
        st.markdown(
            f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>問題文のサイズ（例: 24px）</label>",
            unsafe_allow_html=True
        )
        bulk_question_size = st.text_input("", "24px", key="bulk_question_size")
        st.markdown(
            f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>解説の色（例: #ffffff）</label>",
            unsafe_allow_html=True
        )
        bulk_explanation_color = st.text_input("", "#ffffff", key="bulk_explanation_color")
        st.markdown(
            f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>解説のサイズ（例: 18px）</label>",
            unsafe_allow_html=True
        )
        bulk_explanation_size = st.text_input("", "18px", key="bulk_explanation_size")
        st.markdown(
            f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>正解メッセージの色（例: #00ff00）</label>",
            unsafe_allow_html=True
        )
        bulk_answer_color = st.text_input("", "#00ff00", key="bulk_answer_color")
        st.markdown(
            f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>正解メッセージのサイズ（例: 28px）</label>",
            unsafe_allow_html=True
        )
        bulk_answer_size = st.text_input("", "28px", key="bulk_answer_size")
        st.markdown(
            f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>不正解メッセージの色（例: #ff0000）</label>",
            unsafe_allow_html=True
        )
        bulk_wrong_color = st.text_input("", "#ff0000", key="bulk_wrong_color")
        st.markdown(
            f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>不正解メッセージのサイズ（例: 28px）</label>",
            unsafe_allow_html=True
        )
        bulk_wrong_size = st.text_input("", "28px", key="bulk_wrong_size")
        submitted = st.form_submit_button("🔄 一括適用")
    if submitted:
        bulk_styles = {}
      
        # バリデーション（任意）
        def is_valid_color(code):
            if isinstance(code, str) and code.startswith("#") and (len(code) == 7 or len(code) == 4):
                return True
            return False
        input_errors = []
        if not is_valid_color(bulk_question_color):
            input_errors.append("問題文の色が無効です。例: #ffffff")
        if not bulk_question_size.endswith("px") or not bulk_question_size[:-2].isdigit():
            input_errors.append("問題文のサイズが無効です。例: 24px")
        if not is_valid_color(bulk_explanation_color):
            input_errors.append("解説の色が無効です。例: #ffffff")
        if not bulk_explanation_size.endswith("px") or not bulk_explanation_size[:-2].isdigit():
            input_errors.append("解説のサイズが無効です。例: 18px")
        if not is_valid_color(bulk_answer_color):
            input_errors.append("正解メッセージの色が無効です。例: #00ff00")
        if not bulk_answer_size.endswith("px") or not bulk_answer_size[:-2].isdigit():
            input_errors.append("正解メッセージのサイズが無効です。例: 28px")
        if not is_valid_color(bulk_wrong_color):
            input_errors.append("不正解メッセージの色が無効です。例: #ff0000")
        if not bulk_wrong_size.endswith("px") or not bulk_wrong_size[:-2].isdigit():
            input_errors.append("不正解メッセージのサイズが無効です。例: 28px")
        if input_errors:
            for error in input_errors:
                st.error(f"⚠️ {error}")
        else:
            bulk_styles = {
                "question_color": bulk_question_color,
                "question_size": bulk_question_size,
                "explanation_color": bulk_explanation_color,
                "explanation_size": bulk_explanation_size,
                "answer_color": bulk_answer_color,
                "answer_size": bulk_answer_size,
                "wrong_color": bulk_wrong_color,
                "wrong_size": bulk_wrong_size
            }
            for q in st.session_state["quiz_data"]:
                q["style"].update(bulk_styles)
            save_quiz_data()
            st.success("✅ 一括スタイルをすべての問題に適用しました！")
            st.set_query_params({})  # クエリパラメータをクリア
            st.experimental_rerun()
    # 編集画面のスタイル設定
    with st.expander("⚙️ 編集画面のスタイル設定", expanded=False):
        label_color = st.text_input("ラベルの色（例: #ffffff）", editor_style["label_color"], key="editor_label_color")
        label_size = st.text_input("ラベルのサイズ（例: 16px）", editor_style["label_size"], key="editor_label_size")
        heading_color = st.text_input("見出しの色", editor_style["heading_color"], key="editor_heading_color")
        heading_size = st.text_input("見出しのサイズ", editor_style["heading_size"], key="editor_heading_size")
        if st.button("🎨 スタイルを更新"):
            # バリデーション（任意）
            def is_valid_color(code):
                if isinstance(code, str) and code.startswith("#") and (len(code) == 7 or len(code) == 4):
                    return True
                return False
            errors = []
            if not is_valid_color(label_color):
                errors.append("ラベルの色が無効です。例: #ffffff")
            if not label_size.endswith("px") or not label_size[:-2].isdigit():
                errors.append("ラベルのサイズが無効です。例: 16px")
            if not is_valid_color(heading_color):
                errors.append("見出しの色が無効です。例: #ffcc00")
            if not heading_size.endswith("px") or not heading_size[:-2].isdigit():
                errors.append("見出しのサイズが無効です。例: 24px")
            if errors:
                for error in errors:
                    st.error(f"⚠️ {error}")
            else:
                st.session_state["editor_style"] = {
                    "label_color": label_color,
                    "label_size": label_size,
                    "heading_color": heading_color,
                    "heading_size": heading_size
                }
                save_quiz_data()
                st.success("✅ 編集画面のスタイルを更新しました！")
                st.set_query_params({})  # クエリパラメータをクリア
                st.experimental_rerun()
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
        if st.button(f"問題 {idx + 1} を更新", key=f"update_{idx}"):
            # バリデーション（任意）
            errors = []
            if not question_text:
                errors.append(f"問題 {idx + 1}: 問題文を入力してください。")
            if not all(options):
                errors.append(f"問題 {idx + 1}: すべての選択肢を入力してください。")
            if not explanation:
                errors.append(f"問題 {idx + 1}: 解説を入力してください。")
            if not (question_color.startswith("#") and (len(question_color) == 7 or len(question_color) == 4)):
                errors.append(f"問題 {idx + 1}: 問題文の色が無効です。例: #ffffff")
            if not (question_size.endswith("px") and question_size[:-2].isdigit()):
                errors.append(f"問題 {idx + 1}: 問題文のサイズが無効です。例: 24px")
            if not (explanation_color.startswith("#") and (len(explanation_color) == 7 or len(explanation_color) == 4)):
                errors.append(f"問題 {idx + 1}: 解説の色が無効です。例: #ffffff")
            if not (explanation_size.endswith("px") and explanation_size[:-2].isdigit()):
                errors.append(f"問題 {idx + 1}: 解説のサイズが無効です。例: 18px")
            if not (answer_color.startswith("#") and (len(answer_color) == 7 or len(answer_color) == 4)):
                errors.append(f"問題 {idx + 1}: 正解メッセージの色が無効です。例: #00ff00")
            if not (answer_size.endswith("px") and answer_size[:-2].isdigit()):
                errors.append(f"問題 {idx + 1}: 正解メッセージのサイズが無効です。例: 28px")
            if not (wrong_color.startswith("#") and (len(wrong_color) == 7 or len(wrong_color) == 4)):
                errors.append(f"問題 {idx + 1}: 不正解メッセージの色が無効です。例: #ff0000")
            if not (wrong_size.endswith("px") and wrong_size[:-2].isdigit()):
                errors.append(f"問題 {idx + 1}: 不正解メッセージのサイズが無効です。例: 28px")
          
            if errors:
                for error in errors:
                    st.error(f"⚠️ {error}")
            else:
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
                st.set_query_params({})  # クエリパラメータをクリア
                st.experimental_rerun()
    # 新しい問題の追加セクション
    st.markdown(f"<h3 style='color:{editor_style['heading_color']}; font-size:{editor_style['heading_size']};'>➕ 新しい問題を追加</h3>", unsafe_allow_html=True)
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>新しい問題:</label>", unsafe_allow_html=True)
    new_question = st.text_input("", key="new_question")
    new_options = []
    for i in range(4):
        st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>選択肢 {i + 1}:</label>", unsafe_allow_html=True)
        new_options.append(st.text_input("", key=f"new_option_{i}"))
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>正解:</label>", unsafe_allow_html=True)
    new_answer = st.selectbox("", new_options, key="new_answer")
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>画像URL:</label>", unsafe_allow_html=True)
    new_image_url = st.text_input("", key="new_image_url")
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>解説:</label>", unsafe_allow_html=True)
    new_explanation = st.text_area("", key="new_explanation")
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>点数を設定:</label>", unsafe_allow_html=True)
    new_points = st.number_input("", min_value=1, max_value=100, value=1, key="new_points")
    # スタイル設定
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>問題文の色</label>", unsafe_allow_html=True)
    new_q_color = st.text_input("", "#ffffff", key="new_q_color")
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>問題文のサイズ</label>", unsafe_allow_html=True)
    new_q_size = st.text_input("", "24px", key="new_q_size")
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>解説の色</label>", unsafe_allow_html=True)
    new_e_color = st.text_input("", "#ffffff", key="new_e_color")
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>解説のサイズ</label>", unsafe_allow_html=True)
    new_e_size = st.text_input("", "18px", key="new_e_size")
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>正解メッセージの色</label>", unsafe_allow_html=True)
    new_a_color = st.text_input("", "#00ff00", key="new_a_color")
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>正解メッセージのサイズ</label>", unsafe_allow_html=True)
    new_a_size = st.text_input("", "28px", key="new_a_size")
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>不正解メッセージの色</label>", unsafe_allow_html=True)
    new_w_color = st.text_input("", "#ff0000", key="new_w_color")
    st.markdown(f"<label style='color:{editor_style['label_color']}; font-size:{editor_style['label_size']};'>不正解メッセージのサイズ</label>", unsafe_allow_html=True)
    new_w_size = st.text_input("", "28px", key="new_w_size")
    if st.button("➕ 問題を追加"):
        # バリデーション（任意）
        errors = []
        if not new_question:
            errors.append("新しい問題: 問題文を入力してください。")
        if not all(new_options):
            errors.append("新しい問題: すべての選択肢を入力してください。")
        if not new_answer:
            errors.append("新しい問題: 正解を選択してください。")
        if not new_explanation:
            errors.append("新しい問題: 解説を入力してください。")
        if not (new_q_color.startswith("#") and (len(new_q_color) == 7 or len(new_q_color) == 4)):
            errors.append("新しい問題: 問題文の色が無効です。例: #ffffff")
        if not (new_q_size.endswith("px") and new_q_size[:-2].isdigit()):
            errors.append("新しい問題: 問題文のサイズが無効です。例: 24px")
        if not (new_e_color.startswith("#") and (len(new_e_color) == 7 or len(new_e_color) == 4)):
            errors.append("新しい問題: 解説の色が無効です。例: #ffffff")
        if not (new_e_size.endswith("px") and new_e_size[:-2].isdigit()):
            errors.append("新しい問題: 解説のサイズが無効です。例: 18px")
        if not (new_a_color.startswith("#") and (len(new_a_color) == 7 or len(new_a_color) == 4)):
            errors.append("新しい問題: 正解メッセージの色が無効です。例: #00ff00")
        if not (new_a_size.endswith("px") and new_a_size[:-2].isdigit()):
            errors.append("新しい問題: 正解メッセージのサイズが無効です。例: 28px")
        if not (new_w_color.startswith("#") and (len(new_w_color) == 7 or len(new_w_color) == 4)):
            errors.append("新しい問題: 不正解メッセージの色が無効です。例: #ff0000")
        if not (new_w_size.endswith("px") and new_w_size[:-2].isdigit()):
            errors.append("新しい問題: 不正解メッセージのサイズが無効です。例: 28px")
        if errors:
            for error in errors:
                st.error(f"⚠️ {error}")
        else:
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
            st.set_query_params({})  # クエリパラメータをクリア
            st.experimental_rerun()
    # 「最初の画面に戻る」ボタン
    if st.button("🔙 最初の画面に戻る"):
        st.session_state["edit_mode"] = False
        st.session_state["quiz_started"] = False
        st.set_query_params({})  # クエリパラメータをクリア
        st.experimental_rerun()
