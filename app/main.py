
import streamlit as st
import pandas as pd
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from chains2 import Chain2
from portfolio import Portfolio
from utils import clean_text

def create_streamlit_app(llm, llm_personal, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📩")
    st.title("📮 AI-Powered Email Generator")

    # Input field for URL
    col1, col2 = st.columns(2)
    with col1:
        url_input = st.text_input("🔗 Enter a Job URL:",
                                  value="https://careers.nike.com/lead-software-engineer/job/R-48873")
    with col2:
        email_type = st.selectbox("Choose Email Generation Type:",
                                  ["Generate Email as a Company", "Generate Email for Me"])

    generate_button = None
    submit_personal_data = None
    uploaded_file = None

    # Show input fields for personal details only if "Generate Email for Me" is selected
    if email_type == "Generate Email for Me":
        with st.form(key="personal_data_form"):
            name = st.text_input("👤 Your Name:", value="Joy Matubber")
            company = st.text_input("🏢 Current Company:", value="Brain Station 23")
            experience = st.text_input("📅 Professional Experience:", value="Associate Software Engineer in 2 years")
            skillsIHave = st.text_area("🛠 Skills:", value="Node.js, React, Python, Java, AI, Machine Learning")
            projects = st.text_area("🗂 Projects:", value="Shopify App, Shopify Theme, Seirios, Vento Life Style")
            submit_personal_data = st.form_submit_button("📩 Submit & Generate Email")
    else:
        with st.form(key="company_data_form"):
            uploaded_file = st.file_uploader("Upload Portfolio File", type=["csv"])
            generate_button = st.form_submit_button("📩 Generate Email")

    if generate_button or submit_personal_data:
        with st.spinner('Generating Email...'):
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                jobs = llm.extract_jobs(data)

                if email_type == "Generate Email for Me" and submit_personal_data:
                    for job in jobs:
                        personalized_email = llm_personal.write_mail2(job, name, company, experience, skillsIHave, projects)
                        st.subheader("📄 Personalized Email:")
                        st.code(personalized_email, language='markdown')
                elif email_type == "Generate Email as a Company" and generate_button:
                    if uploaded_file is None:
                        st.error("Please select a file before generating an email.")
                    else:
                        portfolio = Portfolio(file_data=uploaded_file)
                        portfolio.load_portfolio()
                        for job in jobs:
                            skills = job.get('skills', [])
                            links = portfolio.query_links(skills)
                            email_content = llm.write_mail(job, links)
                            st.subheader("📄 Generated Email:")
                            st.code(email_content, language='markdown')
            except Exception as e:
                st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()  # For company emails
    chain_personal = Chain2()  # For personal emails
    create_streamlit_app(chain, chain_personal, None, clean_text)
