import streamlit as st
from pdf_material import PdfMaterial
from ai_module import AiModule

# Sidebar configuration
with st.sidebar:
    st.header("Settings")
    chunk_size = st.slider("chunk size", 100, 2000, 1000)
    overlap_size = st.slider("over-lap size", 50, 1000, 150)

uploaded_file = st.file_uploader("choose file", accept_multiple_files=False, type="pdf")

if uploaded_file is not None:
    my_pdf_file = PdfMaterial(uploaded_file)

    chunks = my_pdf_file.parsing_to_chunk(chunk_size, overlap_size)
    ai_tool = AiModule()

    if chunks:
        st.write(f"found {len(chunks)} fragments")
        for i, chunk in enumerate(chunks):
            with st.expander(f"Chunk {i + 1}"):
                tab_source, tab_ai = st.tabs(["Source Text", "AI key Points"])

                with tab_source:
                    st.write(chunk)

                with tab_ai:
                    if st.button(f"Extract facts from chunk {i+1}"):
                        with st.spinner("DeepSeek is thinking..."):
                            facts = ai_tool.extract_key_points(chunk)
                            st.subheader("Key facts Extracted:")
                            st.info(facts)
            
            
    else:
        st.error("Error occured while chunking file")
