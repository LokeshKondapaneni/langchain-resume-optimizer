from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.exceptions import OutputParserException
from langchain_openai import ChatOpenAI
import openai

load_dotenv()
openai.api_key = os.environ['OPENAI_API_KEY']
llm = ChatOpenAI(model="davinci-002")

def extract_keywords(job_description):
    parser = JsonOutputParser()

    prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {job_description}
            ### INSTRUCTION:
            The scraped text is the job description from the career's page of a website.
            Your job is to extract the technical skills and keywords from the job description, and return them in JSON format containing the following keys: `skills` and `keywords`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
    chain = prompt_extract | llm | parser
    result = chain.invoke({"job_description": job_description})
    return result


def generate_resume_content(role, keywords, fetched_resumes):
    fetched_content = "\n".join(fetched_resumes)
    parser = StrOutputParser()
    prompt_extract = PromptTemplate.from_template(
            """
            ### CONTENT FROM SIMILAR RESUMES:
            {resumes}
            ### KEYWORDS
            {keywords}
            ### INSTRUCTION:
            You are a professional in the field of {role}.
            Create bullet points for a new resume for the role {role} focusing on accomplishments and skills that align with these keywords.
            You can refer to the content from similar resumes for insights, if necessary.
        """
    )
    chain = prompt_extract | llm | parser
    result = chain.invoke({'resumes': fetched_content, 'keywords': keywords, 'role': role})
    return result

def update_resume(original_resume, role, keywords, fetched_resumes):
    parser = StrOutputParser()
    fetched_content = "\n".join(fetched_resumes)
    prompt_extract = PromptTemplate.from_template(
            """
            ### ORIGINAL RESUME
            {original_resume}
            ### CONTENT FROM SIMILAR RESUMES:
            {resumes}
            ### KEYWORDS
            {keywords}
            ### INSTRUCTION:
            You are a professional in the field of {role}.
            Update the original resume for the role {role} by integrating the keywords and insights from these similar resumes, ensuring it remains coherent and professional.
        """
    )
    chain = prompt_extract | llm | parser
    result = chain.invoke({'original_resume': original_resume,'resumes': fetched_content, 'keywords': keywords, 'role': role})
    return result