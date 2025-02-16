# import os
# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
# from dotenv import load_dotenv
#
# load_dotenv()
#
# class Chain2:
#     def __init__(self):
#         self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv('GROQ_API_KEY'), model_name="llama-3.3-70b-versatile")
#
#     def write_mail2(self, job):
#         prompt_email = PromptTemplate.from_template(
#             """
#             ### JOB DESCRIPTION:
#             {job_description}
#
#             ### INSTRUCTION:
#             You are Joy Matubber, an Associate Software Engineer at Brain Station 23.
#             Your job is to write a cold email to the client regarding the job mentioned above describing your capability
#             in fulfilling their needs.
#             i have worked on several projects like Seirios, Vento Life Style, and Ventro Life Style, which you generated individually
#             with guidance from your senior.
#             Do not provide a preamble.
#             ### EMAIL (NO PREAMBLE):
#             """
#         )
#         chain_email = prompt_email | self.llm
#         res = chain_email.invoke({"job_description": str(job)})
#         return res.content
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()


class Chain2:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv('GROQ_API_KEY2'), model_name="llama-3.3-70b-versatile")

    def write_mail2(self, job, name, company, experience, skillsIHave, projects):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are {name}, a skilled {experience} professional at {company}  
            Your expertise includes {skillsIHave}, and you have successfully contributed to projects like {projects}.  

            Your goal is to craft a **highly professional cold email** to a potential client, emphasizing:
            - **Your technical expertise**
            - **Your experience working on similar projects**
            - **How your skills align with the client's job posting**
            - **Why they should consider you for this opportunity**
            Do **not** provide a preamble. 
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "name": name,
            "company": company,
            "experience": experience,
            "skillsIHave": skillsIHave,
            "projects": projects
        })
        return res.content
