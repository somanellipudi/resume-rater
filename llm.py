from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field
from typing import List

class ResumeRating(BaseModel):
    overall_score: float = Field(description="Overall score out of 10")
    strengths: List[str] = Field(description="List of strengths in the resume")
    gaps: List[str] = Field(description="List of gaps or missing qualifications")
    improvements: List[str] = Field(description="List of suggested improvements")

def rate_resume(company_name: str, job_description: str, resume_text: str):
    # Initialize components lazily to ensure environment variables are loaded
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    parser = JsonOutputParser(pydantic_object=ResumeRating)
    
    prompt = ChatPromptTemplate.from_template("""
        You are a hiring domain evaluator.

        Company Name:
        {company_name}

        Job Description:
        {job_description}

        Candidate Resume:
        {resume}

        Tasks:
        1. Infer the company's primary business domain
        2. List key domain areas relevant to this company
        3. Identify candidate experience related to this domain
        4. Identify missing or weak domain exposure
        5. Rate domain relevance from 1–10

        Rules:
        - Use general public knowledge of the company
        - Do not assume resume experience not stated

        Return JSON only:
        {format_instructions}
        """)
    
    chain = prompt | llm | parser
    
    return chain.invoke({
        "company_name": company_name,
        "job_description": job_description,
        "resume": resume_text,
        "format_instructions": parser.get_format_instructions()
    })

