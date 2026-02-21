import os
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

DEFAULT_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4')

MERMAID_PROMPT = '''
You are an assistant that converts a structured list of code steps into a Mermaid flowchart.
Input: a bullet list where each item is a step of the pipeline, optionally tagged as (decision) or (io).
Output: only the Mermaid flowchart code. Use `graph TD` layout. Label nodes using the text provided.
If an item contains the word 'Condition' or is tagged as (decision), render a diamond node with two branches labeled Yes and No.

Now produce a Mermaid diagram for these steps:
{steps}
'''

def steps_to_mermaid(steps: list) -> str:
    bullet_lines = []
    for s in steps:
        tag = ''
        if s.get('type') == 'decision':
            tag = ' (decision)'
        elif s.get('type') == 'io':
            tag = ' (io)'
        bullet_lines.append(f"- {s['label']}{tag}")
    bullet_text = '\n'.join(bullet_lines)

    llm = ChatOpenAI(model_name=DEFAULT_MODEL, temperature=0)
    prompt = PromptTemplate(input_variables=['steps'], template=MERMAID_PROMPT)
    chain = LLMChain(llm=llm, prompt=prompt)
    result = chain.run(steps=bullet_text)

    if '```' in result:
        parts = result.split('```')
        # pick the largest fenced block if present
        blocks = [p for p in parts if p.strip().startswith('mermaid') or 'graph' in p]
        if blocks:
            result = blocks[-1]
        else:
            result = parts[-1]
    if result.strip().startswith('mermaid'):
        result = result.split('\n', 1)[1] if '\n' in result else ''
    return result
