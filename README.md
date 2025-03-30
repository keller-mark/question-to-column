# question-to-column

Interactive table [widget](https://github.com/manzt/anywidget) where rows correspond to scientific papers (from a Zotero collection) and columns correspond to questions.
Convert each question into a column using a [local lanaguage model](https://github.com/ollama/ollama).

```sh
export ZOTERO_API_KEY='something' # TODO: make optional
export LLAMA_CLOUD_API_KEY='something' # TODO: make optional
```

```sh
uv venv
source .venv/bin/activate
uv run marimo edit src/scratch/question_to_column.py
```