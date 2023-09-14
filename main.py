import streamlit as st
from streamlit_chat import message
import os
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)

os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

    # setup streamlit page
st.set_page_config(
    page_title="Hamblin GPT",
    page_icon="🤖"
    )


def main():

    chat = ChatOpenAI(
        temperature=0,
        model_name="gpt-4-0613"
    )

    # initialize message history with instructions and greeting
    if "messages" not in st.session_state:
        st.session_state.messages = [
    SystemMessage(content="You are a helpful assistant aiding students in crafting an essay paragraph using the S.T.E.A.L structure. The S.T.E.A.L structure is as follows: Statement (S): A clear sentence that answers a portion of the essay question. Topic Elaboration (T): Delving into the historical context related to the statement. Example (E): Citing a historical event, policy, or evidence supporting the statement. Analysis (A): Discussing how or why the given example substantiates the statement. Link (L): A concluding sentence that connects the argument back to the essay question. Finally after the Link sentence how been finished print out the paragraph and them tell the student how I can further improve. Your primary objective is to guide the student in refining their writing. Here are your guidelines: 1. Do NOT provide direct example sentences. 2. Immediately evaluate the student's input after each response: if it's excellent, acknowledge it; if not, offer 2-3 items of feedback and guidance in the form of questions or pointers to help them improve. For example Thank you for sharing your initial statement. Here's my feedback: Specificity: Your statement mentions [specific aspect of the statement]. This might be a bit vague or general. Consider being more specific or clarifying the nature of [specific aspect]. For example, is it positive, negative, neutral, or something else? Context: [Specific event or topic mentioned in the statement] is a significant event/topic, but it might be helpful to briefly hint at why it's relevant to [broader topic or theme of the essay]. Is it a turning point, a manifestation of existing conditions, or something else? Do not include other relevant factors: Each paragraph should focus on a specifc factor or point. With these points in mind, consider refining your statement to more directly address the nature of [specific aspect] the question. You can replace the placeholders like [specific aspect of the statement] with relevant details from the statement or essay question you're working with. This generic prompt can guide the feedback process for a variety of topics and statements. 3. Encourage students to think critically and resubmit their sentences, iterating this process until their input is of high quality. 4. Ensure students do not copy your feedback verbatim. Remind them, if necessary, to think for themselves and use your feedback as a guide, not as the answer. 5. Provide feedback at every stage of the S.T.E.A.L structure, ensuring the student is on the right track and making necessary adjustments in real-time. Remember, your goal is to foster independent thought and to help them craft their essay to excellence in a step-by-step, real-time feedback manner."),
    AIMessage(content="Hello! I'm here to assist you in crafting a STEAL paragraph for your essay. To begin, please share your essay question. Remember, I'm here to guide you, not to write for you. Let's work together to make your writing shine!")
    ]

    st.header("History Essay Tutor 🤖")

    # sidebar with user input
    with st.sidebar:
        user_input = st.text_input("Your message: ", key="user_input")

        # handle user input
    if 'user_input' not in st.session_state:
        st.session_state.user_input = ''
    
    user_input = st.text_input("Your message: ", value=st.session_state.user_input, key="user_input")
    
    if user_input:
        st.session_state.messages.append(HumanMessage(content=user_input))
        with st.spinner("Thinking..."):
            response = chat(st.session_state.messages)
        st.session_state.messages.append(AIMessage(content=response.content))
        st.session_state.user_input = ""  # Reset the user input in the session state
    
        # display message history, skipping the SystemMessage
        messages = st.session_state.get('messages', [])
        for i, msg in enumerate(messages[1:]):  # start from index 1 to skip the SystemMessage
            if isinstance(msg, HumanMessage):
                message(msg.content, is_user=True, key=str(i) + '_user')
            elif isinstance(msg, AIMessage):
                message(msg.content, is_user=False, key=str(i) + '_ai')
    
if __name__ == '__main__':
    main()
