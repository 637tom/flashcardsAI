from concurrent.futures import ThreadPoolExecutor, as_completed
from ai_module import AiModule


def generate_all_flashcards(
    ai_tool: AiModule,
    chunks: list[str],
    on_progress: callable,
    on_status: callable,
) -> dict[int, list[dict] | None]:
    """
    Sends all chunks to the AI in parallel using a thread pool.
    Calls on_progress(float) and on_status(str) as each chunk completes.
    Returns a dict mapping chunk index -> list of flashcard dicts (or None on failure).
    """
    results: dict[int, list[dict] | None] = {}
    completed = 0

    with ThreadPoolExecutor() as executor:
        future_to_index = {
            executor.submit(ai_tool.extract_to_flashcards, chunk): i
            for i, chunk in enumerate(chunks)
        }
        for future in as_completed(future_to_index):
            i = future_to_index[future]
            results[i] = future.result()
            completed += 1
            on_progress(completed / len(chunks))
            on_status(f"Processed {completed} / {len(chunks)} chunks...")

    return results
