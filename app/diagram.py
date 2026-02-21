import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

MERMAID_PROMPT = '''
You are an assistant that converts a structured list of code steps into a Mermaid flowchart.
Input: a bullet list where each item is a step of the pipeline, optionally tagged as (decision) or (io).
Output: only the Mermaid flowchart code. Use `graph TD` layout. Label nodes using the text provided.
If an item contains the word 'Condition' or is tagged as (decision), render a diamond node with two branches labeled Yes and No.

Now produce a Mermaid diagram for these steps:
{steps}
'''

def steps_to_mermaid(steps: list) -> str:
    bullet_text = "\n".join([f"- {s['label']}" for s in steps])

    llm = ChatOpenAI(
        model=DEFAULT_MODEL,
        temperature=0,
        api_key=os.environ.get("OPENAI_API_KEY")
    )

    prompt = PromptTemplate(input_variables=["steps"], template=MERMAID_PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt)

    result = chain.run(steps=bullet_text)

    return result
