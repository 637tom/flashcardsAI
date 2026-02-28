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

        # Initialise session state bucket for flashcards
        if "flashcards" not in st.session_state:
            st.session_state.flashcards = {}

        # button – generates flashcards for every chunk at once
        if st.button("Generate Flashcards for All Chunks"):
            status = st.empty()
            for i, chunk in enumerate(chunks):
                status.text(f"Processing chunk {i + 1} / {len(chunks)}...")
                st.session_state.flashcards[i] = ai_tool.extract_to_flashcards(chunk)#keeping generated FC in memory for later use
            status.text("Done!")

        st.divider()

        for i, chunk in enumerate(chunks):
            with st.expander(f"Chunk {i + 1}"):
                tab_source, tab_ai = st.tabs(["Source Text", "Flashcards"])

                with tab_source:
                    st.write(chunk)

                with tab_ai:
                    cards = st.session_state.get("flashcards", {}).get(i)
                    if cards:
                        for card in cards:
                            st.markdown(f"**Q: {card.get('question', 'N/A')}**")#bolded question of a FC, get value for "question if does not exit write N/A"
                            st.info(f"A: {card.get('answer', 'N/A')}")#info box with answer of a FC
                            st.divider()
                    else:
                        st.caption("No flashcards yet. Click \"Generate Flashcards for All Chunks\".")
            
    else:
        st.error("Error occured while chunking file")
