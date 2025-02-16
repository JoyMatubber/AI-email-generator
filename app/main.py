
import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from chains2 import Chain2
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, llm_personal, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    st.title("📧 AI-Powered Email Generator")

    # Input field for URL
    url_input = st.text_input("🔗 Enter a Job URL:", value="https://careers.nike.com/lead-software-engineer/job/R-48873")

    # Buttons for generating emails
    col1, col2 = st.columns(2)
    with col1:
        submit_button = st.button("🔍 Generate Email As a Company")
    with col2:
        personalized_button = st.button("📩 Generate Email for Me")

    if submit_button or personalized_button:
        with st.spinner('Generating Email...'): # Show loader while fetching data

            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)

                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)

                    if submit_button:
                        email_content = llm.write_mail(job, links)
                        st.subheader("📄 Generated Email:")
                        st.code(email_content, language='markdown')

                    if personalized_button:
                        personalized_email = llm_personal.write_mail2(job)
                        st.subheader("📄 Personalized Email:")
                        st.code(personalized_email, language='markdown')

            except Exception as e:
                st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()  # For company emails
    chain_personal = Chain2()  # For personal emails
    portfolio = Portfolio()
    create_streamlit_app(chain, chain_personal, portfolio, clean_text)
