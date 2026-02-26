import streamlit as st
from pdf_material import PdfMaterial

uploaded_file = st.file_uploader("choose file", accept_multiple_files=False, type="pdf")
if uploaded_file is not None:
    my_pdf_file = PdfMaterial(uploaded_file)
    chunk_size = st.sidebar.slider("chunk size", 100, 2000, 100)
    chunks = my_pdf_file.parsing_to_chunk(chunk_size)
    if chunks:
        st.write(f"found {len(chunks)} fragments")
        for i, chunk in enumerate(chunks):
            with st.expander(f"Chunk {i + 1}"):
                st.write(chunk)
            
    else:
        st.error("Error occured while chunking file")
