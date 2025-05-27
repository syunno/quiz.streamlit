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
# クイズのリセット関数
def reset_quiz():
    st.session_state["quiz_started"] = False
    st.session_state["score"] = 0
    st.session_state["current_question"] = 0
    st.session_state["answered"] = False
# クイズの開始関数
def start_quiz():
    reset_quiz()
    st.session_state["quiz_started"] = True
# クイズ終了時のリセット関数
def end_quiz():
    reset_quiz()
# カスタムCSSの適用
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://data.ac-illust.com/data/thumbnails/a5/a550c1129e4997ff4e4b20abcedd1391_t.jpeg");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        /* タイトルとサブタイトルのスタイル */
        h1 {
            color: #FFD700; /* ゴールド */
            font-size: 48px;
            text-align: center;
            margin-top: 20px;
        }
        h2 {
            color: #ADD8E6; /* ライトブルー */
            font-size: 36px;
            text-align: center;
            margin-bottom: 20px;
        }
        /* サイドバー用ボタンのスタイル */
        .sidebar-button {
            background-color: #4444FF;
            color: white;
            font-size: 18px;
            padding: 10px 20px;
            border-radius: 8px;
            border: 2px solid gold;
            cursor: pointer;
            margin-bottom: 10px;
            width: 100%;
            text-align: center;
        }
        .sidebar-button:hover {
            background-color: #3333CC;
        }
        /* クイズ終了メッセージのスタイル */
        .quiz-end {
            color: green;
            font-size: 36px;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)
# サイドバーに固定ボタンを配置
st.sidebar.title("メニュー")
if st.sidebar.button("🔧 編集モード", key="edit_mode_button"):
    st.session_state["edit_mode"] = not st.session_state["edit_mode"]
    reset_quiz()
if st.sidebar.button("🔙 最初の画面", key="back_to_start_button"):
    reset_quiz()
# 条件分岐による表示
if st.session_state["edit_mode"]:
    st.markdown("<h1>クイズ編集モード</h1>", unsafe_allow_html=True)
    # 各問題の編集セクション
    for idx, q in enumerate(st.session_state["quiz_data"]):
        st.markdown(f"<h2>問題 {idx + 1}</h2>", unsafe_allow_html=True)
        question_text = st.text_input("問題を編集:", q["question"], key=f"question_{idx}")
        options = [st.text_input(f"選択肢 {i+1}:", q["options"][i], key=f"option_{idx}_{i}") for i in range(len(q["options"]))]
      
        # 正解が選択肢に含まれていない場合、一番最初をデフォルトに設定
        if q["answer"] in options:
            default_index = options.index(q["answer"])
        else:
            default_index = 0
        answer = st.selectbox("正解を選択:", options, index=default_index, key=f"answer_{idx}")
      
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
  
    if st.button("➕ 問題を追加", key="add_question_button"):
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
elif st.session_state["quiz_started"]:
    question_index = st.session_state["current_question"]
    if question_index < len(st.session_state["quiz_data"]):
        question = st.session_state["quiz_data"][question_index]
      
        # 画像表示（エラー対策付き）
        if question.get("image_url"):
            try:
                st.image(question["image_url"], width=600)
            except Exception:
                st.warning("画像の読み込みに失敗しました。")
      
        # 問題文の表示
        st.markdown(f"<h2>問題: {question['question']}</h2>", unsafe_allow_html=True)
      
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
          
            st.markdown(f"<p style='color:black; font-size:20px; margin-top:10px;'>解説: {question['explanation']}</p>", unsafe_allow_html=True)
      
            if st.button("次の問題へ", key="next_question_button"):
                st.session_state["current_question"] += 1
                st.session_state["answered"] = False
                st.session_state["score_updated"] = False  # フラグをリセット
                st.session_state.pop("selected_option", None)
    else:
        st.markdown("<h1 class='quiz-end'>クイズ終了！🎉</h1>", unsafe_allow_html=True)
        # スコアの表示を100点満点に変更
        st.write(f"あなたのスコア: {st.session_state['score']} / 100")
        save_quiz_data()
      
        # クイズ終了後に最初の画面に戻るボタンを表示
        if st.button("🔙 最初の画面に戻る", key="reset_button"):
            end_quiz()
else:
    # 最初の画面（タイトルとサブタイトル）
    st.markdown('<h1>デジタルクイズ</h1>', unsafe_allow_html=True)
    st.markdown('<h2>クイズを解いてデジタル機器について学ぼう！</h2>', unsafe_allow_html=True)
    if st.button("▶️ クイズを開始", key="start_quiz_button", on_click=start_quiz):
        pass  # on_click が start_quiz を呼び出すため、ここは空にします
