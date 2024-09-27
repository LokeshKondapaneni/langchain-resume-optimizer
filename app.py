import streamlit as st
from resume_parser import parse_resume
import random
from langchain_utils import extract_keywords, generate_resume_content, update_resume
from scrape import scrape_resume, fetch_url_content

st.title("Resume Optimizer")
action = st.radio("Select Action:", ("Create a New Resume", 
                                     "Update Existing Resume"))

if action == "Update Existing Resume":
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
else:
    uploaded_file = False

job_description = st.text_area("Job Descriotion")
role = st.text_input("Interested Role")

if st.button("Process"):
    if action == "Update Existing Resume" and uploaded_file is not None and job_description and role:
        resume_text = parse_resume(uploaded_file)
        keywords = extract_keywords(job_description)
        urls_keywords = scrape_resume(role)

        fetched_data = [fetch_url_content(url) for url in urls_keywords]

        updated_resume = update_resume(original_resume=resume_text,
                                       role=role, 
                                       keywords=keywords,
                                       fetched_resumes=fetched_data)
        
        st.download_button("Download Updated Resume",
                           updated_resume,
                           file_name="updated_resume.txt")
        
        st.write("Updated Resume:")
        st.write(updated_resume)

        st.write("Similar resume urls found:")
        st.write(urls_keywords)

    elif action == "Create a New Resume" and job_description and role:
        keywords = extract_keywords(job_description)
        urls_keywords = scrape_resume(role)

        fetched_data = [fetch_url_content(url) for url in urls_keywords]

        new_resume_content = generate_resume_content(keywords=keywords,
                                                     fetched_resumes=fetched_data)
        
        st.download_button("Download New Generated Resume",
                           new_resume_content,
                           file_name="new_resume.txt")
        
        st.write("Generated Resume:")
        st.write(new_resume_content)

        st.write("Similar resume urls found:")
        st.write(urls_keywords)

    else:
        st.error("Please fill all fields to proceed.")