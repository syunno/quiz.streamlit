# 必要なライブラリをインポート
import streamlit as st
import json
from pathlib import Path

# **データ保存関数**
def save_quiz_data():
    """
    現在のクイズデータをJSONファイルに保存する関数
    """
    with open("quiz_data.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state["quiz_data"], f, ensure_ascii=False)

# **データロード関数**
def load_quiz_data():
    """
    JSONファイルからクイズデータをロードする関数。
    ファイルが存在する場合のみデータをロード。
    """
    if Path("quiz_data.json").exists():
        with open("quiz_data.json", "r", encoding="utf-8") as f:
            st.session_state["quiz_data"] = json.load(f)

# **セッション初期化**
if "quiz_data" not in st.session_state:
    load_quiz_data()
    if "quiz_data" not in st.session_state:  # ファイルがない場合の初期データ
        st.session_state["quiz_data"] = [
            {"question": "この城の名前は？", "options": ["姫路城", "松本城", "大阪城", "熊本城"], 
             "answer": "姫路城", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8c/Himeji_Castle_looking_up.jpg/800px-Himeji_Castle_looking_up.jpg",
             "explanation": "姫路城は日本三名城の一つで、別名白鷺城とも呼ばれています。"
            },
            {"question": "この花の名前は？", "options": ["梅", "桜", "牡丹", "藤"], 
             "answer": "桜", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Japanese_Sakura.JPG/800px-Japanese_Sakura.JPG",
             "explanation": "桜は日本の象徴的な花で、春の訪れを知らせる風物詩です。"
            }
        ]
    # デフォルト値を補完（explanation キーがない場合）
    for q in st.session_state["quiz_data"]:
        if "explanation" not in q:
            q["explanation"] = "解説がまだ追加されていません"

# セッション状態の管理
if "quiz_started" not in st.session_state:
    st.session_state["quiz_started"] = False
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0
if "answered" not in st.session_state:
    st.session_state["answered"] = False
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False

# **カスタムCSS**
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://tse4.mm.bing.net/th/id/OIP.Rwqvo--qeTaERBRSp579xQHaEO?cb=iwp2&rs=1&pid=ImgDetMain");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        .custom-title {
            font-size: 64px;  /* タイトル用フォントサイズ */
            font-family: "Yu Mincho", "Hiragino Mincho Pro", serif;
            text-align: center;
            color: white;
        }
        .custom-subtitle {
            font-size: 40px;  /* サブタイトル用フォントサイズ */
            color: white;
            margin-bottom: 20px;
            text-align: center;
        }
        .custom-text {
            font-size: 24px;  /* 解説用フォントサイズ */
            line-height: 1.6;
            text-align: justify;
            color: white;
        }
        .stButton > button {
            background-color: #0000FF;
            color: white;
            font-size: 30px;
            padding: 10px;
            border-radius: 5px;
            border: 2px solid gold;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #0000FF;
            transform: scale(1.05);
        }

    </style>
""", unsafe_allow_html=True)

# **タイトルセクション**
st.markdown('<div class="custom-title">デジタルクイズ</div>', unsafe_allow_html=True)
st.markdown('<div class="custom-subtitle">クイズを解いてデジタル機器について学ぼう！</div>', unsafe_allow_html=True)
# **クイズ開始ボタン**
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
        st.write(f"**問題: {question['question']}**")
        selected_option = st.radio("選択肢:", question["options"], key="selected_option")

        if st.button("回答する") and not st.session_state["answered"]:
            st.session_state["answered"] = True
            if selected_option == question["answer"]:
                st.session_state["score"] += 1
                st.markdown("<h2 class='correct'>🎉 正解！</h2>", unsafe_allow_html=True)
            else:
                st.markdown("<h2 class='wrong'>❌ 不正解！</h2>", unsafe_allow_html=True)
            
                        # 解説を表示
            st.markdown(f"<p class='custom-text'>解説: {question['explanation']}</p>", unsafe_allow_html=True)

        # 次の問題に進むボタン
        if st.session_state["answered"]:
            if st.button("次の問題へ"):
                st.session_state["current_question"] += 1
                st.session_state["answered"] = False
                st.rerun()
    else:
        # クイズ終了画面
        st.markdown("<h1>クイズ終了！🎉</h1>", unsafe_allow_html=True)
        st.write(f"あなたのスコア: {st.session_state['score']} / {len(st.session_state['quiz_data'])}")
        save_quiz_data()

        # 最初の画面に戻るボタン
        if st.button("🔙 最初の画面に戻る"):
            st.session_state["quiz_started"] = False
            st.session_state["score"] = 0
            st.session_state["current_question"] = 0
            st.session_state["answered"] = False
            st.rerun()
# **クイズ編集モード**
if st.button("🔧 クイズ編集モード"):
    st.session_state["edit_mode"] = not st.session_state["edit_mode"]
    st.rerun()

if st.session_state["edit_mode"]:
   st.markdown("""
    <style>
        /* クイズ編集タイトル */
        h2 {
            color: #FFD700;  /* ゴールド */
            font-family: "Yu Mincho", "Hiragino Mincho Pro", serif;
        }

        /* 問題タイトル */
        .stMarkdown h3 {
            color: #00CED1;  /* ターコイズブルー */
        }

        /* ラベル（問題を編集、選択肢など） */
        label {
            color: #FFFFFF !important;
            font-weight: bold;
        }

        /* テキスト入力欄の文字色 */
        .stTextInput input {
            color: #FF69B4;  /* ピンク */
        }

        /* テキストエリアの文字色 */
        .stTextArea textarea {
            color: #ADFF2F;  /* 黄緑 */
        }

        /* セレクトボックスの文字色 */
        .stSelectbox div[data-baseweb="select"] {
            color: #87CEFA;  /* ライトブルー */
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("<h2>📝 クイズ編集</h2>", unsafe_allow_html=True)
     for idx, q in enumerate(st.session_state["quiz_data"]):
        st.markdown(f"### 問題 {idx + 1}")
        question_text = st.text_input("問題を編集:", q["question"], key=f"question_{idx}")
        options = [st.text_input(f"選択肢 {i+1}:", q["options"][i], key=f"option_{idx}_{i}") for i in range(len(q["options"]))]
        answer = st.selectbox("正解を選択:", options, index=q["options"].index(q["answer"]), key=f"answer_{idx}")
        image_url = st.text_input("画像URLを編集:", q["image_url"], key=f"image_url_{idx}")
        explanation = st.text_area("解説を編集:", q.get("explanation", "解説がまだ追加されていません"), key=f"explanation_{idx}")

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

    # 新しい問題を追加
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

    # 戻るボタン
    if st.button("🔙 最初の画面に戻る"):
        st.session_state["edit_mode"] = False
        st.rerun()
