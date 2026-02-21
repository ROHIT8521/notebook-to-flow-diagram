from parser import extract_cells
from analyzer import extract_steps_from_cells
from diagram import steps_to_mermaid
from renderer import mermaid_to_image_url

st.set_page_config(page_title='Notebook → Flow Diagram', layout='wide')

st.title('📘 Notebook → Flow Diagram')
st.markdown('Upload a Databricks or Jupyter notebook and get a visual flow diagram of the pipeline.')

with st.sidebar:
    st.header('Settings')
    model = st.text_input('OpenAI Model', value=os.environ.get('OPENAI_MODEL', 'gpt-4'))
    fmt = st.selectbox('Diagram format', ['png', 'svg'])
    show_cells = st.checkbox('Show parsed cells', value=False)

uploaded = st.file_uploader('Upload notebook (.ipynb, .py, .dbc)', type=['ipynb', 'py', 'dbc'])

if uploaded is not None:
    raw = uploaded.read()
    try:
        cells = extract_cells(uploaded.name, raw)
    except Exception as e:
        st.error(f'Could not parse file: {e}')
        st.stop()

    if show_cells:
        st.subheader('Parsed cells')
        for i, (ctype, code) in enumerate(cells):
            with st.expander(f'Cell {i+1} ({ctype})'):
                st.code(code, language='python')

    st.markdown('---')
    if st.button('Generate diagram'):
        with st.spinner('Analyzing code...'):
            steps = extract_steps_from_cells(cells)
        st.success(f'Extracted {len(steps)} steps')

        st.subheader('Textual description')
        for s in steps:
            st.write(f"- {s['id']}: {s['label']} ({s['type']})")

        st.subheader('Mermaid flowchart')
        mermaid = steps_to_mermaid(steps)
        if not mermaid.strip():
            st.error('Failed to generate mermaid diagram')
        else:
            st.code(mermaid, language='')
            img_url = mermaid_to_image_url(mermaid, fmt=fmt)
            st.image(img_url, caption='Generated diagram', use_column_width=True)
            st.markdown(f'[Open image in new tab]({img_url})')

        st.info('Tip: try switching OpenAI model to gpt-3.5-turbo if you want cheaper runs.')
