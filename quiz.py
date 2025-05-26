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

# セッション状態の初期化を安全に実行
for key, default in {
    "quiz_data": [],
    "score": 0,  # スコアの初期化
    "current_question": 0,
    "quiz_started": False,
    "answered": False,
    "edit_mode": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# 固定スコア表示用のHTML
score = st.session_state.get("score", 0)  # 安全にスコアを取得
st.markdown(f"""
    <div class="fixed-score">
        現在のスコア: {score}
    </div>
""", unsafe_allow_html=True)

# カスタムCSSの適用
st.markdown("""
    <style>
        .fixed-score {
            position: fixed;
            top: 10px;
            left: 20px;
            background-color: rgba(255, 255, 255, 0.8);
            padding: 10px 20px;
            border-radius: 8px;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
            font-size: 18px;
            font-weight: bold;
            z-index: 1000;
        }
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
    </style>
""", unsafe_allow_html=True)

# 最初の画面
if not st.session_state["quiz_started"] and not st.session_state["edit_mode"]:
    st.markdown('<div class="custom-title">デジタルクイズ</div>', unsafe_allow_html=True)
    st.markdown('<div class="custom-subtitle">クイズを解いてデジタル機器について学ぼう！</div>', unsafe_allow_html=True)
    st.button("▶️ クイズを開始", key="start_button", on_click=lambda: st.session_state.update({"quiz_started": True}))
# クイズ画面
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

        st.markdown(f"<p style='color:white; font-size:24px;'><strong>問題: {question['question']}</strong></p>", unsafe_allow_html=True)

        if not st.session_state["answered"]:
            for option in question["options"]:
                if st.button(option, key=f"option_{option}"):
                    st.session_state["selected_option"] = option
                    st.session_state["answered"] = True

        if st.session_state["answered"]:
            selected_option = st.session_state["selected_option"]
            if selected_option == question["answer"]:
                st.session_state["score"] += question["points"]  # 点数加算を安全に実行
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
        # クイズ終了
        total_points = sum(q["points"] for q in st.session_state["quiz_data"])  # 合計点数を計算
        st.markdown("<h1>クイズ終了！🎉</h1>", unsafe_allow_html=True)
        st.write(f"あなたのスコア: {st.session_state['score']} / {total_points}")  # スコアを正しく表示
        save_quiz_data()

# 編集モード
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
    new_points = st.number_input("点数を設定:", min_value=1, max_value=100, value=1, key="new_points")  # 点数入力欄を追加

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
        st.session_state["edit_mode"] = False  # 編集モードを解除
        st.session_state["quiz_started"] = False  # クイズ開始状態を停止
        st.rerun()
