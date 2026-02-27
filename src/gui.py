import streamlit as st
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
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

        # Top-level button – generates flashcards for every chunk at once
        if st.button("Generate Flashcards for All Chunks"):
            progress = st.progress(0)
            status = st.empty()
            completed = 0

            with ThreadPoolExecutor() as executor:
                future_to_index = {
                    executor.submit(ai_tool.extract_to_flashcards, chunk): i
                    for i, chunk in enumerate(chunks)
                }
                for future in as_completed(future_to_index):
                    i = future_to_index[future]
                    st.session_state.flashcards[i] = future.result()
                    completed += 1
                    progress.progress(completed / len(chunks))
                    status.text(f"Processed {completed} / {len(chunks)} chunks...")

            status.text("Done!")

        st.divider()

        for i, chunk in enumerate(chunks):
            with st.expander(f"Chunk {i + 1}"):
                tab_source, tab_ai = st.tabs(["Source Text", "Flashcards"])

                with tab_source:
                    st.write(chunk)

                with tab_ai:
                    if i in st.session_state.get("flashcards", {}):
                        cards = st.session_state.flashcards[i]
                        if isinstance(cards, list) and len(cards) > 0:
                            for card in cards:
                                st.markdown(f"**Q: {card.get('question', 'N/A')}**")
                                st.info(f"A: {card.get('answer', 'N/A')}")
                                st.divider()
                        else:
                            st.warning("No flashcards could be generated for this chunk.")
                    else:
                        st.caption("Click \"Generate Flashcards for All Chunks\" above to populate this tab.")
            
    else:
        st.error("Error occured while chunking file")
