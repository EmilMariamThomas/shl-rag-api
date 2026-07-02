import streamlit as st
from agent import chat

st.set_page_config(page_title="SHL AI Agent", layout="wide")

st.title("🧠 SHL Assessment Recommendation Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []


# show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


user_input = st.chat_input("Ask about assessments...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.write(user_input)

    # call backend
    result = chat(st.session_state.messages)

    reply = result["reply"]

    # assistant output
    with st.chat_message("assistant"):
        st.write(reply)

        # recommendations
        if result.get("recommendations"):
            st.subheader("📌 Recommendations")
            for r in result["recommendations"]:
                st.markdown(f"- {r}")

        # 🔎 retrieval viewer
        if result.get("retrieved"):
            with st.expander("🔎 Retrieved Assessments (AI Brain)"):
                for r in result["retrieved"]:
                    st.markdown(f"**{r['name']}**")
                    st.caption(r["type"])
                    st.write(r["url"])
                    st.write("---")

    st.session_state.messages.append(
        {"role": "assistant", "content": reply}
    )