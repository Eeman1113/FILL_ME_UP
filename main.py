import streamlit as st
import openai
import requests
from bs4 import BeautifulSoup
import re

openai.api_key = 'Your API Key'

def generate_text(prompt):
    responseObject = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Answer the questions as a student filling the form. (Write good big answers)(If the question has options select the correct option)"},
            {"role": "user", "content": prompt},
        ],
        max_tokens=256
    )
    response = responseObject["choices"][0]["message"]["content"]
    return response

def get_form_text(link):
    url = link
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    code = soup.text.strip()

    # Use regular expression to split the text based on multiple delimiters
    delimiters = ["Your answer", "Your email address", "Date"]
    pattern = "|".join(map(re.escape, delimiters))
    parts = re.split(pattern, code)

    return parts

def main():
    st.markdown("<h1 style='text-align: center;'>FILL_ME_UP 記入</h1>", unsafe_allow_html=True)#人工知能
    # st.title("FILL_ME_UP")

    link = st.text_input("Enter the Google Forms link:")
    if st.button("Generate Responses"):
        if link:
            form_parts = get_form_text(link)

            responses = {}
            for i, part in enumerate(form_parts, start=1):
                question_prompt = f"{part.strip()} []"
                answer = generate_text(question_prompt)
                responses[f"Question {i}"] = {"question": part.strip(), "answer": answer.strip()}

            st.subheader("Generated Responses:")
            # Display questions Display answers
            # for key, value in responses.items():
            for key, value in list(responses.items())[:-1]:

                st.markdown('___')
                st.markdown(f"**{key}:**     \n{value['question']}")
                st.markdown(f"**Answer:**     \n")
                st.code(f"{value['answer']}\n",language='textile')
                # st.markdown('___')
                # st.markdown(f"**{key}:**<br>{value['question']}")
                # st.markdown(f"**Answer:**<br>{value['answer']}<br>")
            st.markdown('___')
            st.balloons()

        else:
            st.warning("Please enter a valid Google Forms link.")

if __name__ == "__main__":
    main()
