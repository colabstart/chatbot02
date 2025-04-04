import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 TOTO의 제주도 여행 가이드 서비스")
st.write(
    "TOTO의 제주도 여행 가이드 서비스는 OpenAI의 GPT-3.5 모델을 활용하여, 여러분의 여행을 더욱 즐겁고 편리하게 만들어주는 스마트 챗봇입니다."
    "간단히 OpenAI API 키만 입력하면 바로 이용하실 수 있어요."
)

# 🔑 사용자로부터 OpenAI API 키 입력 받기
openai_api_key = st.text_input("🔐 OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("API 키를 입력하시면 챗봇을 이용하실 수 있어요.", icon="🗝️")
else:

    # OpenAI 클라이언트 생성
    client = OpenAI(api_key=openai_api_key)

    # 시스템 역할 메시지 정의
    system_message = {
        "role": "system",
        "content": (
            "당신은 제주도 여행에 대한 정보를 제공하는 친절하고 전문적인 가이드입니다. "
            "맛집, 관광지, 교통, 날씨, 계절별 추천 등 여행자들이 궁금해할 내용을 쉽게 설명해 주세요. "
            "친절하고 대화하듯 자연스럽게 대답하세요."
        )
    }
    
    # 세션 상태에 메시지가 없으면 초기화 및 환영 인사 추가
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": (
                "안녕하세요! 😊 저는 **TOTO의 제주도 여행 가이드 챗봇**입니다.\n\n"
                "제주도 맛집, 관광지, 교통편, 날씨 등 여행 준비에 도움이 필요하신가요?\n"
                "궁금한 걸 무엇이든 물어보세요!"
            )
        })

    # 이전 메시지 표시
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("제주도 여행이 궁금한가요? 질문을 입력해 보세요!"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # GPT 응답 생성
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[system_message] + st.session_state.messages,
            stream=True,
        )

        # 응답 출력 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
