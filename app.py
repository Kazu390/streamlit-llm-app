# ---------------------------------
# 必要なライブラリを読み込む
# ---------------------------------
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv
load_dotenv()  # .envファイルから環境変数を読み込む

# ---------------------------------
# AI（LLM）に質問するための関数
# ---------------------------------
def ask_llm(user_input: str, expert_type: str) -> str:
    """
    ・user_input : ユーザーが入力した質問（文字）
    ・expert_type : 選択された専門家の種類（文字）
    → AIの回答（文字）を返す
    """

    # 専門家の種類によって、AIの役割を決める
    if expert_type == "ITコンサルタント":
        system_prompt = (
            "あなたは優秀なITコンサルタントです。"
            "専門的かつ分かりやすく回答してください。"
        )
    elif expert_type == "マーケティング専門家":
        system_prompt = (
            "あなたは経験豊富なマーケティング専門家です。"
            "実践的な視点で回答してください。"
        )
    else:
        # 万が一どれにも当てはまらなかった場合
        system_prompt = "あなたは有能な専門家です。"

    # AIモデルを準備する
    llm = ChatOpenAI(
        model_name="gpt-4o-mini",
        temperature=0  # 回答を安定させる
    )

    # AIに渡すメッセージを作る
    messages = [
        SystemMessage(content=system_prompt),  # AIの役割
        HumanMessage(content=user_input),       # ユーザーの質問
    ]

    # AIに質問して、結果を受け取る
    result = llm(messages)

    # AIの回答（文字）だけを返す
    return result.content


# ---------------------------------
# ここから画面（Webアプリ）の作成
# ---------------------------------

# アプリのタイトル
st.title("専門家に質問できるLLM Webアプリ")

# アプリの説明文
st.markdown("""
### このアプリについて
1. 質問を入力します  
2. 専門家の種類を選びます  
3. 送信ボタンを押すとAIが専門家になりきって答えます  
""")

# 専門家を選ぶラジオボタン
expert = st.radio(
    "専門家の種類を選択してください",
    ["ITコンサルタント", "マーケティング専門家"]
)

# 質問を入力する欄
user_text = st.text_area(
    "質問を入力してください",
    placeholder="例：新規サービスを立ち上げる際の注意点を教えてください"
)

# 「送信」ボタンが押されたときの処理
if st.button("送信"):

    # 何も入力されていなかった場合
    if user_text.strip() == "":
        st.warning("質問を入力してください。")

    # 入力がある場合
    else:
        # AIが考えている間、くるくる表示
        with st.spinner("AIが回答を考えています..."):
            answer = ask_llm(user_text, expert)

        # 結果を画面に表示
        st.subheader("回答結果")
        st.write(answer)
