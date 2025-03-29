# question-to-column

Table where rows correspond to scientific papers and columns correspond to questions.
Convert each question into a column using a local lanaguage model via Ollama.

```sh
export ZOTERO_API_KEY='something' # TODO: make optional
export LLAMA_CLOUD_API_KEY='something' # TODO: make optional
```

```sh
uv venv
source .venv/bin/activate
uv run marimo edit src/scratch/question_to_column.py
```