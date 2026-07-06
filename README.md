# H-1B Job Eligibility Analyzer

A simple Streamlit application that evaluates whether a job (given its title and description) is likely to qualify as an **H-1B "specialty occupation"** under U.S. immigration standards. The app sends the provided information to the OpenAI API (default model: `gpt-5`) and returns a structured, legal-style analysis.

> ⚠️ **Disclaimer:** This tool is for informational purposes only and does not replace a real attorney. The generated output is not legal advice.

## Features

- Simple web interface for entering a Job Title and Job Description
- Analyzes the 4 criteria used in USCIS H-1B specialty occupation determinations (Criterion 1–4)
- Produces evidence-based output that references/quotes specific parts of the job description
- Separately lists missing/weak points and factors that would strengthen the case
- Uses a fixed, predictable output format (defined in the prompt template)

## Requirements

- Python 3.9+
- An OpenAI API key
- The following Python packages:
  - `streamlit`
  - `openai`

## Installation

1. Download the repository (or the file) to your machine.
2. It's recommended to create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. Install the required packages:

   ```bash
   pip install streamlit openai
   ```

## Environment Variables

Set the following environment variables before running the app:

| Variable | Required | Description |
|---|---|---|
| `OPENAI_API_KEY` | Yes | Your OpenAI API key |
| `OPENAI_MODEL` | No | Model to use (default: `gpt-5`) |

**macOS / Linux:**
```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_MODEL="gpt-5"   # optional
```

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="sk-..."
$env:OPENAI_MODEL="gpt-5"
```

Alternatively, if you'd like to use a `.env` file, install the `python-dotenv` package and add the following lines at the top of the file:

```python
from dotenv import load_dotenv
load_dotenv()
```

## Running the App

Assuming the file is named `app.py`:

```bash
streamlit run app.py
```

After running the command, the app should open automatically in your browser (typically at `http://localhost:8501`).

## Usage

1. Enter the listing's title in the **Job Title** field (e.g., "Senior Software Engineer").
2. Paste the full text of the listing into the **Job Description** field.
3. Click the **Analyze** button.
4. The result is displayed below with a fixed structure:
   - H-1B Likelihood
   - Specialty Occupation Strength
   - Criteria Analysis (Criterion 1–4)
   - Evidence from Description
   - Strongest and Weakest Criteria
   - Key Legal Risks
   - Missing or Weak Points
   - What Would Strengthen This Case
   - Reasoning

## How It Works

- The `analyze_job()` function inserts the entered job title and job description into a fixed prompt template.
- The prompt instructs the model to:
  - Rely only on the facts provided, without making general assumptions.
  - Treat Criterion 1 and 4 as primary factors, and Criterion 2 and 3 as secondary/supporting factors.
  - State that a criterion "cannot be evaluated" (rather than "not satisfied") when information is missing.
  - Return the output in the fixed heading format above, with no extra text.
- The `client.responses.create()` call sends the request to the OpenAI Responses API, and the `output_text` field is displayed to the user.

## Error Handling

- Shows a warning if the Job Title or Job Description is empty.
- Shows a warning and skips the API call if `OPENAI_API_KEY` is not set.
- Displays an error message in the UI if the API call fails (`Exception`).

## Known Limitations

- The model's output may not always strictly follow the format requested in the prompt; this depends on the provider's (OpenAI's) model behavior.
- The `gpt-5` model name can be overridden via an environment variable; make sure the model is accessible under your OpenAI account.
- The app does not persist any data; each analysis is one-off (history is lost on refresh).
- This tool does not provide legal advice; for actual H-1B petitions, consult a licensed immigration attorney.

## License

No license has been specified for this project. Feel free to add your preferred license before distributing it.
