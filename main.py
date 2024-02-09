import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
import re
import os
from langchain.prompts import PromptTemplate
from streamlit.components.v1 import html


load_dotenv()
api_key = os.environ['API_KEY']
llm = GoogleGenerativeAI(model="models/text-bison-001", google_api_key=api_key, temperature=0.7)
print()

def render_chatbot():
    # Use st.markdown to create a button
    st.markdown('<div id="chatbot-button" style="position: fixed; bottom: 20px; right: 20px; background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; cursor: pointer;">Chat</div>', unsafe_allow_html=True)

    # Use st.components to load the JavaScript code for the chatbot
    html("""
    <script>
        // Define the function to open the chatbot
        function openChatbot() {
            alert("Open your chatbot here!");  
        }

        // Add a click event listener to the chatbot button
        document.getElementById("chatbot-button").addEventListener("click", openChatbot);
    </script>
    """)
#
def main():
    render_chatbot()
    # Main content area
    st.title("Interview Question and Answer App")


    search_query = st.sidebar.text_input("Enter search query", "")
    search_button = st.sidebar.button("Search")
    # filtered_questions = filter_questions(questions_and_answers, search_query)

    if search_button:
        request = llm.invoke("Interview questions for " + str(search_query))
        matches = re.findall(r'\d+\.\s(.+?)(?=\n\n|$)', request, re.DOTALL)
        questions_and_answers = [{'question': match.split('?')[0].strip(), 'answer': match.split('?')[1].strip()} for
                                 match in matches]
        question = []
        answer = []
        for qa_pair in questions_and_answers:
            question.append(qa_pair['question'])
            answer.append(qa_pair['answer'])

        print(question)
        if len(question) > 0:
            # st.write(str(request))
            display_questions_and_answers(question, answer)
        else:
            st.write("Nothing found")


def display_questions_and_answers(question, answer):
    print( question)
    for index, value in enumerate(question):
        print("initial", index, value)
        ques = value
        ans = answer[index]
        print("question and ans", ques, ans)
        # Display question
        st.subheader(ques)

        button_key = f"answer_button_{index}"
        if st.button(f"Answer {index + 1}", key=button_key):
            st.write(ans)
            st.markdown("---")  # Add a separator line


if __name__ == "__main__":
    main()
