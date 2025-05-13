
# RAG Benchmark (NarrativeQA)

This script processes the NarrativeQA dataset to benchmark Retrieval-Augmented Generation (RAG) systems by:

1. **Loading Data**:
   - Loads the `deepmind/narrativeqa` dataset from HuggingFace `datasets`.

2. **Data Cleaning**:
   - Extracts questions, answers, and documents.
   - Cleans HTML and newline characters from documents.

3. **Filtering**:
   - Keeps only answers longer than 2 words.
   - Keeps only samples where the answer appears exactly once in the document.

4. **Context Generation**:
   - Extracts a small window of text (one sentence before and after) around the answer as `rag_context`.

5. **Selection**:
   - Sorts by answer word count and selects the top 10.

6. **Output**:
   - Saves the resulting DataFrame to an Excel file (`RAG Benchmark.xlsx`).

## Output

- `RAG Benchmark.xlsx`: Contains the filtered QA pairs with context for RAG evaluation.

## Requirements

Install the dependencies:

```bash
pip install datasets beautifulsoup4 pandas openpyxl tqdm
```

## Notes

- Adjust `window_size` in `get_rag_context` for broader context range.
