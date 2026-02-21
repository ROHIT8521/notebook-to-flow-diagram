# Notebook → Flow Diagram

Converts Databricks / Jupyter notebooks into Mermaid flowcharts using LangChain + OpenAI and Streamlit UI.

## Run locally

1. python -m venv .venv && source .venv/bin/activate
2. pip install -r requirements.txt
3. export OPENAI_API_KEY=sk-...
4. streamlit run app/main.py

## Deploy (free)

- Push to GitHub.
- On Streamlit Community Cloud or Hugging Face Spaces, connect the repo and set the environment variable `OPENAI_API_KEY`.

## Notes

- OpenAI API calls are not free — model usage will be billed to your OpenAI account.
