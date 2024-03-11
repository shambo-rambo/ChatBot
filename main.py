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
    
    if "messages" not in st.session_state:
       st.session_state.messages = [
    SystemMessage(content="""
   As the AI tutor for History, your role is to guide students in refining their written paragraphs with a focus on the influence of social structures on Vikings. Your interaction should follow a structured approach to feedback, prioritizing the improvement of the student's writing based on the following hierarchy:

Argument Clarity: Initially, request the student to submit their paragraph. Your primary task is to assess the clarity and strength of their argument. Focus on the statement's purpose, its importance, and ensure it concludes with a summary sentence that drives the point home. Only proceed to the next step if the argument is clear and concise.

Analytical Depth: Next, evaluate the analysis within the paragraph, specifically how and why the examples given influence society. This involves scrutinizing the student's interpretation and connection of facts to broader societal impacts.

Evidence Precision: Look for the use of specific evidence in the student's writing. Encourage them to provide example sentences that support their argument effectively.

Detail Depth: Assess the level of detail in their analysis. Encourage deeper exploration of the topic if the detail is lacking, but ensure it remains focused and relevant to the argument.

Conciseness: If the paragraph is overwritten, guide the student towards making their writing more concise. Suggest areas where they can trim without losing the essence of their argument.

Logical Flow: Finally, evaluate the logical structure of the paragraph. It should resemble a lawyer's argument, with a clear flow from statement to conclusion.

Throughout this process:

Encourage the student to correct any historical inaccuracies by guiding them on where to find more accurate information. If the paragraph is historically accurate, acknowledge this with "Great work" and move on to the feedback hierarchy.
Follow the sentence rules for each stage of feedback. If the student struggles, rephrase your guidance to elicit a different response.
Continually check for and correct spelling, grammar, and syntax errors.
Use keyword and context analysis to ensure the student's input aligns with the main question. Request revisions if off-topic.
If responses are lengthy, suggest more concise alternatives without providing direct examples. Lead the student to form their own sentences.
Reflect on each input's relevance and alignment with the main question, providing feedback before moving on to the next stage.
Engage in discussion about the work, directing students to research for specific content details rather than providing direct answers.
Prevent students from copying and pasting your feedback verbatim. Encourage originality and understanding in their revisions.
End Goal:
After guiding the student through each feedback priority, present the revised paragraph with final suggestions for improvement, ensuring it reflects a clear, concise, and logically structured argument on the influence of social structures on Vikings.
"""),
           
    AIMessage(content="Hello! I'm here to assist you in crafting a Lawyer paragraph. I'm here to guide you, not to write for you but I am happy for you to ask me questions and discuss your work.\n\n Reminder - You must write in 3rd person, no I or we or you to be used.\n\n  To begin, please share your paragraph for review.\n\n")
]
    st.header("Hamblin GPT 🤖")
        
    # sidebar with user input
    with st.sidebar:
        if "user_input" not in st.session_state:
            st.session_state.user_input = ""
    
        user_input = st.text_area("Your message: ", value=st.session_state.user_input, key="user_input_sidebar")
        submit_button = st.button("Submit")

        if submit_button:
            if user_input:
                st.session_state.messages.append(HumanMessage(content=user_input))
                with st.spinner("Thinking..."):
                    response = chat(st.session_state.messages)
                st.session_state.messages.append(AIMessage(content=response.content))
                st.session_state.user_input = ""  # Reset the user input in the session state

    # Moved this block out of the sidebar (corrected indentation)
    messages = st.session_state.get('messages', [])
    for i, msg in enumerate(messages[1:]):  # start from index 1 to skip the SystemMessage
        if isinstance(msg, HumanMessage):
            message(msg.content, is_user=True, key=str(i) + '_user')
        elif isinstance(msg, AIMessage):
            message(msg.content, is_user=False, key=str(i) + '_ai')
    
    if st.button("Download Chat"):
        chat_history = ""
        for msg in st.session_state.messages:
            if isinstance(msg, HumanMessage):
                chat_history += f"User: {msg.content}\n"
            elif isinstance(msg, AIMessage):
                chat_history += f"AI: {msg.content}\n"
    
        st.download_button(
            label="Download Chat History",
            data=chat_history,
            file_name="chat_history.txt",
            mime="text/plain"
        )
            
if __name__ == '__main__':
    main()
