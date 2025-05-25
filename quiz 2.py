import streamlit as st

#streamlit run main.py

# **和風デザインのカスタムCSS**
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://www.transparenttextures.com/patterns/washi.png");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }
        h1, h2, h3 {
            font-size: 48px;
            font-family: "Yu Mincho", "Hiragino Mincho Pro", serif;
        }
        p {
            font-size: 28px;
        }
        .correct, .wrong {
            font-size: 32px;
            font-weight: bold;
        }
        .quiz-container {
            font-family: "Yu Mincho", "Hiragino Mincho Pro", serif;
            background: rgba(255, 255, 255, 0.85);
            padding: 20px;
            border-radius: 10px;
            border: 3px solid #a52a2a;
            text-align: center;
            box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
            margin: auto;
            width: 50%;
        }
        .stButton > button {
            background-color: #a52a2a;
            color: white;
            font-size: 24px;
            padding: 10px;
            border-radius: 5px;
            border: 2px solid gold;
            transition: 0.3s;
        }
        .stButton > button:hover {
            background-color: #800000;
            transform: scale(1.05);
        }
    </style>
""", unsafe_allow_html=True)

# **クイズタイトル**
st.markdown("<h1>🖌 墨書風クイズゲーム 🎌</h1>", unsafe_allow_html=True)

# **クイズデータ**
quiz_data = [
    {"question": "この城の名前は？", "options": ["姫路城", "松本城", "大阪城", "熊本城"], 
     "answer": "姫路城", "image_url": r"C:\Users\81802\OneDrive\デスクトップ\絵\oriba.jpg"},
    {"question": "この花の名前は？", "options": ["梅", "桜", "牡丹", "藤"], 
     "answer": "桜", "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3f/Japanese_Sakura.JPG/800px-Japanese_Sakura.JPG"}
]

# **セッション状態の管理**
if "quiz_started" not in st.session_state:
    st.session_state["quiz_started"] = False
if "score" not in st.session_state:
    st.session_state["score"] = 0
if "current_question" not in st.session_state:
    st.session_state["current_question"] = 0
if "answered" not in st.session_state:
    st.session_state["answered"] = False

# **クイズ開始ボタン**
if not st.session_state["quiz_started"]:
    if st.button("クイズを開始"):
        st.session_state["quiz_started"] = True
        st.rerun()
else:
    question_index = st.session_state["current_question"]
    if question_index < len(quiz_data):
        question = quiz_data[question_index]

        # **画像を表示（金枠付き）**
        st.image(question["image_url"], width=600)

        st.write(f"**問題: {question['question']}**")

        # **選択肢を表示（クイズ開始前は表示しない）**
        if st.session_state["quiz_started"]:
            selected_option = st.radio("選択肢:", question["options"], key="selected_option")

            # **「回答する」ボタン**
            if st.button("回答する") and not st.session_state["answered"]:
                st.session_state["answered"] = True
                if selected_option == question["answer"]:
                    st.session_state["score"] += 1
                    st.markdown("<h2 class='correct'>🎉 正解！</h2>", unsafe_allow_html=True)
                else:
                    st.markdown("<h2 class='wrong'>❌ 不正解！</h2>", unsafe_allow_html=True)

        # **「次の問題へ」ボタン**
        if st.session_state["answered"]:
            if st.button("次の問題へ"):
                st.session_state["current_question"] += 1
                st.session_state["answered"] = False
                st.rerun()
    else:
        # **クイズ終了時の枠を追加（「クイズ終了！」を枠内に配置）**
        st.markdown("""
            <div class='quiz-container'>
                <h1>クイズ終了！🎉</h1>
                <p>あなたのスコア: {}</p>
            </div>
        """.format(st.session_state["score"]), unsafe_allow_html=True)


