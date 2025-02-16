import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class Chain2:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv('GROQ_API_KEY'), model_name="llama-3.3-70b-versatile")

    def write_mail2(self, job):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Joy Matubber, an Associate Software Engineer at Brain Station 23. Brain Station 23 is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing your capability 
            in fulfilling their needs. 
            You have worked on several projects like Seirios, Vento Life Style, and Ventro Life Style, which you generated individually 
            with guidance from your senior. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job)})
        return res.content
