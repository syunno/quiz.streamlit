import streamlit as st
import json
import base64
from pathlib import Path
# ページ設定（横幅を広くして改行されにくくする）
st.set_page_config(page_title="安全専念クイズ", layout="wide")
# ========== ユーティリティ ==========
def save_quiz_data():
    try:
        with open("quiz_data.json", "w", encoding="utf-8") as f:
            json.dump(st.session_state["quiz_data"], f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"データ保存に失敗しました: {e}")
def load_quiz_data():
    if Path("quiz_data.json").exists():
        try:
            with open("quiz_data.json", "r", encoding="utf-8") as f:
                st.session_state["quiz_data"] = json.load(f)
        except Exception as e:
            st.error(f"データ読み込みに失敗しました: {e}")
def save_app_settings():
    try:
        with open("app_settings.json", "w", encoding="utf-8") as f:
            json.dump(st.session_state["app_settings"], f, ensure_ascii=False, indent=2)
    except Exception as e:
        st.warning(f"設定保存に失敗しました: {e}")
def load_app_settings():
    if Path("app_settings.json").exists():
        try:
            with open("app_settings.json", "r", encoding="utf-8") as f:
                st.session_state["app_settings"] = json.load(f)
        except Exception as e:
            st.error(f"設定読み込みに失敗しました: {e}")
def validate_quiz_data(data):
    if not isinstance(data, list):
        raise ValueError("トップレベルはリストである必要があります。")
    cleaned = []
    for i, q in enumerate(data, 1):
        if not isinstance(q, dict):
            raise ValueError(f"問題 {i} が辞書ではありません。")
        question = q.get("question")
        options = q.get("options")
        answer = q.get("answer")
        if not question:
            raise ValueError(f"問題 {i}: 'question' がありません。")
        if not isinstance(options, list) or len(options) < 2:
            raise ValueError(f"問題 {i}: 'options' は2つ以上のリストが必要です。")
        if answer not in options:
            raise ValueError(f"問題 {i}: 'answer' は 'options' に含まれている必要があります。")
        q.setdefault("explanation", "解説がまだ追加されていません")
        q.setdefault("points", 1)
        cleaned.append(q)
    return cleaned
def safe_rerun():
    # Streamlit のバージョン差異に安全に対応
    fn = getattr(st, "rerun", None)
    if callable(fn):
        fn()
    else:
        st.experimental_rerun()
def file_to_data_uri(uploaded_file) -> str:
    """UploadedFile を CSS の background-image で使える data URI に変換"""
    data = uploaded_file.getvalue()
    mime = uploaded_file.type or "image/png"
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{mime};base64,{b64}"
# ========== セッション初期化 ==========
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
                "points": 10
            }
        ]
    for q in st.session_state["quiz_data"]:
        q.setdefault("explanation", "解説がまだ追加されていません")
        q.setdefault("points", 1)
# アプリ設定（背景画像など）
if "app_settings" not in st.session_state:
    load_app_settings()
    if "app_settings" not in st.session_state:
        st.session_state["app_settings"] = {
            "bg": {
                "type": "url",  # url | preset | data_uri
                "value": "https://data.ac-illust.com/data/thumbnails/a5/a550c1129e4997ff4e4b20abcedd1391_t.jpeg"
            }
        }
for key, default in {
    "quiz_started": False,
    "score": 0,
    "current_question": 0,
    "answered": False,
    "edit_mode": False,
    "score_updated": False,
}.items():
    if key not in st.session_state:
        st.session_state[key] = default
# ========== コールバック ==========
def reset_quiz():
    st.session_state["score"] = 0
    st.session_state["current_question"] = 0
    st.session_state["answered"] = False
    st.session_state["score_updated"] = False
    st.session_state.pop("selected_option", None)
def start_quiz_callback():
    reset_quiz()
    st.session_state["quiz_started"] = True
def end_quiz_callback():
    reset_quiz()
    st.session_state["quiz_started"] = False
    st.session_state["edit_mode"] = False
def next_question_callback():
    st.session_state["current_question"] += 1
    st.session_state["answered"] = False
    st.session_state["score_updated"] = False
    st.session_state.pop("selected_option", None)
def toggle_edit_mode_callback():
    st.session_state["edit_mode"] = not st.session_state["edit_mode"]
    reset_quiz()
# ========== 背景画像の現在値 ==========
bg_conf = st.session_state["app_settings"]["bg"]
bg_url = bg_conf.get("value") or "https://data.ac-illust.com/data/thumbnails/a5/a550c1129e4997ff4e4b20abcedd1391_t.jpeg"
# ========== サイドバー ==========
st.sidebar.title("メニュー")
st.sidebar.button("🔧 編集モード", key="edit_mode_button", on_click=toggle_edit_mode_callback)
st.sidebar.button("🔙 最初の画面", key="back_to_start_button", on_click=end_quiz_callback)
# データの入出力（バックアップ/インポート）
with st.sidebar.expander("📁 データの入出力"):
    json_str = json.dumps(st.session_state["quiz_data"], ensure_ascii=False, indent=2)
    st.download_button(
        "💾 クイズデータをダウンロード",
        data=json_str.encode("utf-8"),
        file_name="quiz_data.json",
        mime="application/json"
    )
    uploaded = st.file_uploader("JSON をインポート", type="json")
    if uploaded is not None:
        try:
            data_raw = json.load(uploaded)
            st.session_state["quiz_data"] = validate_quiz_data(data_raw)
            save_quiz_data()
            st.success("✅ インポートしました。")
        except Exception as e:
            st.error(f"⚠️ インポートに失敗しました: {e}")
# 背景画像設定
with st.sidebar.expander("🎨 背景画像設定"):
    # プリセット候補
    PRESETS = {
        "淡いグラデの抽象": "https://images.unsplash.com/photo-1517816743773-6e0fd518b4a6?q=80&w=1920&auto=format&fit=crop",
        "青系グラデーション": "https://images.unsplash.com/photo-1517816434065-1662653d4958?q=80&w=1920&auto=format&fit=crop",
        "シンプルテクスチャ": "https://images.unsplash.com/photo-1516637090014-cb1ab0d08fc7?q=80&w=1920&auto=format&fit=crop",
        "初期画像（イラストAC）": "https://data.ac-illust.com/data/thumbnails/a5/a550c1129e4997ff4e4b20abcedd1391_t.jpeg",
    }
    source_to_index = {"preset": 0, "url": 1, "data_uri": 2}
    current_source_idx = source_to_index.get(bg_conf.get("type", "url"), 1)
    source = st.radio("背景ソース", ["プリセット", "URL", "ファイルアップロード"], index=current_source_idx, horizontal=True)
    new_bg_type = bg_conf.get("type", "url")
    new_bg_value = bg_url
    if source == "プリセット":
        new_bg_type = "preset"
        preset_name = st.selectbox("プリセットを選択", list(PRESETS.keys()))
        new_bg_value = PRESETS[preset_name]
        st.image(new_bg_value, caption=f"プレビュー: {preset_name}", use_column_width=True)
    elif source == "URL":
        new_bg_type = "url"
        new_bg_value = st.text_input("画像URLを入力", value=bg_url)
        if new_bg_value:
            st.image(new_bg_value, caption="プレビュー", use_column_width=True)
    else:  # ファイルアップロード
        new_bg_type = "data_uri"
        img_file = st.file_uploader("画像ファイルをアップロード", type=["png", "jpg", "jpeg", "webp"])
        if img_file is not None:
            try:
                data_uri = file_to_data_uri(img_file)
                new_bg_value = data_uri
                st.image(img_file, caption="プレビュー（アップロード）", use_column_width=True)
            except Exception as e:
                st.error(f"画像の処理に失敗しました: {e}")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("適用（プレビュー）"):
            st.session_state["app_settings"]["bg"] = {"type": new_bg_type, "value": new_bg_value}
            st.success("✅ 背景を適用しました。")
    with col_b:
        if st.button("設定を保存"):
            st.session_state["app_settings"]["bg"] = {"type": new_bg_type, "value": new_bg_value}
            save_app_settings()
            st.success("💾 背景設定を保存しました。")
# ========== CSS（背景に動的URL反映） ==========
st.markdown(f"""
    <style>
        .stApp {{
            background-image: url("{bg_url}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .block-container {{ max-width: 1200px; }}
        h1 {{
            color: #FFD700;
            font-size: clamp(28px, 4vw, 48px);
            text-align: center;
            margin-top: 20px;
        }}
        h2 {{
            color: #ADD8E6;
            font-size: clamp(18px, 3.2vw, 36px);
            text-align: center;
            margin-bottom: 20px;
        }}
        h2.subtitle {{
            white-space: nowrap;
            word-break: keep-all;
            overflow-wrap: normal;
            font-size: clamp(18px, 2.8vw, 36px);
        }}
        .quiz-end {{
            color: #90EE90;
            font-size: 36px;
            text-align: center;
        }}
        /* 画像の高さ制限（画面内に収める） */
        .stImage img {{
            max-width: 100%;
            height: auto;
            max-height: 60vh;
            object-fit: contain;
            display: block;
            margin: 0 auto;
            border-radius: 6px;
            box-shadow: 0 2px 12px rgba(0,0,0,.25);
        }}
        @media (max-width: 768px) {{
            .stImage img {{ max-height: 40vh; }}
        }}
        /* 一般ボタン（次の問題へ等） */
        .stButton > button {{
            width: 100%;
            padding: 14px 18px;
            font-size: clamp(16px, 2.2vw, 22px);
            border-radius: 10px !important;
            border: 2px solid #1E90FF;
            background: linear-gradient(180deg,#ffffff,#f6f9ff);
            color: #0b1f33;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(30,144,255,.25);
            font-weight: 600;
        }}
        /* サイドバーのボタンは控えめに */
        section[data-testid="stSidebar"] .stButton > button {{
            font-size: 16px;
            min-height: 40px;
            padding: 10px 12px;
            border-width: 2px;
            border-radius: 10px !important;
            box-shadow: 0 2px 8px rgba(30,144,255,.25);
        }}
        /* 選択肢ボタンを特大サイズに（回答前のみこのコンテナ内で使用） */
        .choices .stButton > button {{
            width: 100%;
            padding: 30px 34px;               /* さらに大きく */
            font-size: clamp(24px, 4.2vw, 44px);
            min-height: 110px;                /* 高さをしっかり確保 */
            border-radius: 18px !important;
            border: 5px solid #1E90FF;
            background: linear-gradient(180deg,#ffffff,#eef4ff);
            color: #0b1f33;
            margin-bottom: 18px;
            box-shadow: 0 8px 22px rgba(30,144,255,.30);
            font-weight: 800;
            letter-spacing: 0.03em;
        }}
    </style>
""", unsafe_allow_html=True)
# ========== 本体 ==========
if st.session_state["edit_mode"]:
    st.markdown("<h1>クイズ編集モード</h1>", unsafe_allow_html=True)
    for idx, q in enumerate(st.session_state["quiz_data"]):
        st.markdown(f"<h2>問題 {idx + 1}</h2>", unsafe_allow_html=True)
        question_text = st.text_input("問題を編集:", q["question"], key=f"question_{idx}")
        num_options = st.number_input(
            "選択肢数",
            min_value=2, max_value=8,
            value=len(q["options"]),
            step=1,
            key=f"num_options_{idx}"
        )
        options = []
        for i in range(int(num_options)):
            default = q["options"][i] if i < len(q["options"]) else ""
            options.append(st.text_input(f"選択肢 {i+1}:", default, key=f"option_{idx}_{i}"))
        default_index = options.index(q["answer"]) if q["answer"] in options else 0
        answer = st.selectbox("正解を選択:", options if options else [""], index=default_index, key=f"answer_{idx}")
        image_url = st.text_input("画像URLを編集:", q.get("image_url", ""), key=f"image_url_{idx}")
        explanation = st.text_area("解説を編集:", q.get("explanation", ""), key=f"explanation_{idx}")
        points = st.number_input("点数を設定:", min_value=1, max_value=100, value=int(q.get("points", 1)), step=1, key=f"points_{idx}")
        col_u, col_d = st.columns(2)
        with col_u:
            if st.button(f"問題 {idx + 1} を更新", key=f"update_{idx}"):
                if answer not in options:
                    st.error("⚠️ 正解は選択肢に含まれている必要があります。")
                elif any(opt.strip() == "" for opt in options):
                    st.error("⚠️ 空の選択肢があります。すべて入力してください。")
                else:
                    st.session_state["quiz_data"][idx] = {
                        "question": question_text,
                        "options": options,
                        "answer": answer,
                        "image_url": image_url,
                        "explanation": explanation,
                        "points": int(points),
                    }
                    save_quiz_data()
                    st.success(f"✅ 問題 {idx + 1} を更新しました！")
        with col_d:
            if st.button(f"🗑️ 問題 {idx + 1} を削除", key=f"delete_{idx}"):
                st.session_state["quiz_data"].pop(idx)
                save_quiz_data()
                st.success(f"🗑️ 問題 {idx + 1} を削除しました！")
                safe_rerun()
    st.markdown("### ➕ 新しい問題を追加")
    new_question = st.text_input("新しい問題:", key="new_question")
    new_num_options = st.number_input("選択肢数（2〜8）", min_value=2, max_value=8, value=4, step=1, key="new_num_options")
    new_options = [st.text_input(f"選択肢 {i + 1}:", key=f"new_option_{i}") for i in range(int(new_num_options))]
    new_answer = st.selectbox("正解:", new_options if new_options else [""], key="new_answer")
    new_image_url = st.text_input("画像URL:", key="new_image_url")
    new_explanation = st.text_area("解説:", key="new_explanation")
    new_points = st.number_input("点数を設定:", min_value=1, max_value=100, value=1, step=1, key="new_points")
    if st.button("➕ 問題を追加", key="add_question_button"):
        if new_question and all(opt.strip() for opt in new_options) and new_answer and new_explanation:
            if new_answer not in new_options:
                st.error("⚠️ 正解は選択肢に含まれている必要があります。")
            else:
                st.session_state["quiz_data"].append({
                    "question": new_question,
                    "options": new_options,
                    "answer": new_answer,
                    "image_url": new_image_url,
                    "explanation": new_explanation,
                    "points": int(new_points),
                })
                save_quiz_data()
                st.success("✅ 新しい問題を追加しました！")
        else:
            st.error("⚠️ 必須項目をすべて入力してください！")
elif st.session_state["quiz_started"]:
    question_index = st.session_state["current_question"]
    if question_index < len(st.session_state["quiz_data"]):
        question = st.session_state["quiz_data"][question_index]
        # 画像表示（CSSで高さ制限）
        if question.get("image_url"):
            try:
                st.image(question["image_url"], use_column_width=True)
            except Exception:
                st.warning("画像の読み込みに失敗しました。")
        # 進捗と点数の表示
        total_questions = len(st.session_state["quiz_data"])
        st.caption(f"問題 {question_index + 1} / {total_questions} | この問題の点数: {question.get('points', 1)} 点")
        st.progress((question_index) / total_questions if total_questions else 0)
        # 問題文
        st.markdown(f"<h2>問題: {question['question']}</h2>", unsafe_allow_html=True)
        # 2列の選択肢ボタン（未回答時のみ表示＝回答後は一切表示しない）
        if not st.session_state["answered"]:
            cols = st.columns(2)
            for i, option in enumerate(question["options"]):
                with cols[i % 2]:
                    st.markdown("<div class='choices'>", unsafe_allow_html=True)
                    if st.button(option, key=f"option_{question_index}_{i}"):
                        st.session_state["selected_option"] = option
                        st.session_state["answered"] = True
                    st.markdown("</div>", unsafe_allow_html=True)
        # 回答後の表示（ボタンは出さない）
        if st.session_state["answered"]:
            selected_option = st.session_state["selected_option"]
            is_correct = (selected_option == question["answer"])
            if not st.session_state.get("score_updated", False) and is_correct:
                st.session_state["score"] += int(question.get("points", 1))
                st.session_state["score_updated"] = True
            # 結果テキストのみ表示
            if is_correct:
                st.markdown("<h2 style='color:green;'>🎉 正解！</h2>", unsafe_allow_html=True)
            else:
                st.markdown("<h2 style='color:red;'>❌ 不正解！</h2>", unsafe_allow_html=True)
                st.write(f"あなたの選択: {selected_option}")
                st.write(f"正解: {question['answer']}")
            # 解説
            st.markdown(
                f"<p style='color:black; font-size:20px; margin-top:10px;'>解説: {question['explanation']}</p>",
                unsafe_allow_html=True
            )
            st.button("次の問題へ", key="next_question_button", on_click=next_question_callback)
    else:
        total_points = sum(q.get("points", 1) for q in st.session_state["quiz_data"])
        score = st.session_state["score"]
        percent = (score / total_points * 100) if total_points else 0
        st.markdown("<h1 class='quiz-end'>クイズ終了！🎉</h1>", unsafe_allow_html=True)
        st.write(f"あなたのスコア: {score} / {total_points}（{percent:.1f}%）")
        save_quiz_data()
        st.button("🔙 最初の画面に戻る", key="reset_button", on_click=end_quiz_callback)
else:
    st.markdown('<h1>安全専念クイズ</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subtitle">クイズを解いて安全知識を身に付けよう！</h2>', unsafe_allow_html=True)
    st.button("▶️ クイズを開始", key="start_quiz_button", on_click=start_quiz_callback)
