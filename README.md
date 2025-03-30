# question-to-column

Create a table where rows correspond to scientific papers (from a Zotero collection) and columns correspond to questions.
Parse each paper PDF and obtain the values for each column by asking a local lanaguage model.

```sh
export ZOTERO_API_KEY='something' # TODO: make optional
export LLAMA_CLOUD_API_KEY='something' # TODO: make optional
```

```sh
uv venv
source .venv/bin/activate
uv run marimo edit src/scratch/question_to_column.py
```
