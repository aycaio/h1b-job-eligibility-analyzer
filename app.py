import os

import streamlit as st
from openai import OpenAI


APP_TITLE = "H-1B Job Eligibility Analyzer"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")


def analyze_job(job_title: str, job_description: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
You are a U.S. immigration attorney providing a structured H-1B evaluation for a SPECIFIC case.

IMPORTANT:
- This is case-specific analysis
- Do NOT give general explanations
- Base everything only on the provided facts
- Do not rely on general assumptions about job titles
- Base your conclusion strictly on the described duties and stated requirements
- If information is missing, identify it under "Missing or Weak Points"

Analyze whether the role is likely to qualify as an H-1B specialty occupation.
Explicitly state for Criteria 1, 2, 3, and 4 whether each is:
- Satisfied
- Not clearly satisfied
- Not satisfied

Use only the provided facts when assessing the criteria.
Quote or closely reference the specific parts of the job description that support your analysis.
If the description is very short, explain why it is insufficient.
Do not repeat the entire job description. Extract only the most relevant phrases or explain why the description lacks sufficient detail.
Treat Criterion 1 and Criterion 4 as primary factors.
Treat Criterion 2 and Criterion 3 as supporting or secondary factors.
Explicitly identify which criteria are the strongest or weakest.
Prioritize Criteria 1 and 4 when determining overall H-1B likelihood.
If information for Criterion 2 or Criterion 3 is missing, state that it cannot be evaluated rather than assuming it is not satisfied.
In the Reasoning section, clearly explain which criteria drive the conclusion.
Highlight whether Criterion 1 and Criterion 4 are satisfied or not, and why.
Explain that Criterion 2 and Criterion 3 are supporting and may be indeterminate if facts are missing.
Do not list the criteria mechanically in the Reasoning section. Provide a prioritized, analytical explanation.
When appropriate, include a sentence identifying the strongest weaknesses or strengths in the case, prioritizing Criterion 1 and Criterion 4 over the others.

Return your answer EXACTLY in the format below. Do not add extra text.

H-1B Likelihood:

Specialty Occupation Strength:

Criteria Analysis:
- Criterion 1:
- Criterion 2:
- Criterion 3:
- Criterion 4:

Evidence from Description:
- 

Strongest and Weakest Criteria:
- Strongest:
- Weakest:

Key Legal Risks:
- 
- 

Missing or Weak Points:
- 
- 

What Would Strengthen This Case:
- 
- 

Reasoning:

Job Title:
{job_title}

Job Description:
{job_description}
""".strip()

    response = client.responses.create(
        model=DEFAULT_MODEL,
        input=prompt,
    )

    return response.output_text.strip()


st.set_page_config(page_title=APP_TITLE, page_icon=":page_facing_up:")
st.title(APP_TITLE)

job_title = st.text_input("Job Title")
job_description = st.text_area("Job Description", height=220)
analysis = None

if st.button("Analyze", type="primary"):
    if not job_title.strip() or not job_description.strip():
        st.error("Please enter both a job title and a job description.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("Missing OPENAI_API_KEY. Set it in your environment and try again.")
    else:
        with st.spinner("Analyzing job eligibility..."):
            try:
                analysis = analyze_job(job_title.strip(), job_description.strip())
            except Exception as exc:
                st.error(f"Analysis failed: {exc}")

if analysis:
    st.subheader("Analysis Result")
    with st.container(border=True):
        st.markdown(analysis)
