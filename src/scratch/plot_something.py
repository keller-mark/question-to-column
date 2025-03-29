import marimo

__generated_with = "0.11.3"
app = marimo.App(width="medium")


@app.cell
def _():
    import anywidget
    import numpy as np
    import pandas as pd
    import os
    from os.path import join
    from oxc_py import transform
    from traitlets import Unicode, Dict, List, Int, Bool
    return (
        Bool,
        Dict,
        Int,
        List,
        Unicode,
        anywidget,
        join,
        np,
        os,
        pd,
        transform,
    )


@app.cell
def _():
    from pyzotero import zotero
    return (zotero,)


@app.cell
def _(join, os):
    ZOTERO_API_KEY = os.environ.get('ZOTERO_API_KEY')
    ZOTERO_PDF_DIR = join(os.environ['HOME'], 'Zotero', 'storage')

    LLAMA_CLOUD_API_KEY = os.environ.get('LLAMA_CLOUD_API_KEY')
    return LLAMA_CLOUD_API_KEY, ZOTERO_API_KEY, ZOTERO_PDF_DIR


@app.cell
def _(ZOTERO_API_KEY, zotero):
    zot = zotero.Zotero(library_id='5416725', library_type='group', api_key=ZOTERO_API_KEY)
    return (zot,)


@app.cell
def _(ZOTERO_PDF_DIR, join, zot):
    def get_papers_in_collection(collection_id='KQ9EAFPZ'):
        items = zot.collection_items(collection_id)

        papers = [ d for d in items if d["data"]["itemType"] == "journalArticle" ]
        attachments = [ d for d in items if d["data"]["itemType"] == "attachment" ]
        
        def get_attachment(item):
            attachment_url = item["links"]["attachment"]["href"]
            attachment_key = attachment_url.split("/")[-1]
            
            for a in attachments:
                if a["key"] == attachment_key:
                    return a
            return None

        def get_paper(item):
            attachment = get_attachment(item)
            return {
                "key": item['data']['key'],
                "title": item['data']['title'],
                "attachment_key": attachment["key"],
                "filename": attachment["data"]["filename"],
                "filepath": join(ZOTERO_PDF_DIR, attachment["key"], attachment["data"]["filename"])
            }
        
        papers_for_table = [
            get_paper(item)
            for item in papers
        ]
        return papers_for_table
    return (get_papers_in_collection,)


@app.cell
def _(get_papers_in_collection):
    papers_for_table = get_papers_in_collection()
    papers_for_table
    return (papers_for_table,)


@app.cell
def _(Dict, List, anywidget, papers_for_table, transform):
    class TableWidget(anywidget.AnyWidget):
        _esm = transform("""
        import * as React from "https://esm.sh/react@18";
        import { createRender, useModelState } from "https://esm.sh/@anywidget/react@0.0.8";

        function Table() {
          const [papers, setPapers] = useModelState("papers");
          const [columns, setColumns] = useModelState("columns");
          return (
            <>
            <style>{`
                .table-widget, .table-widget tr, .table-widget th, .table-widget td {
                    border: 1px solid black;
                }
                .column-manager {
                    padding: 4px;
                }
                .column-manager input, .column-manager textarea {
                    border: 1px solid black;
                }
                .table-widget, .column-manager {
                    flex-grow: 1;
                }
            `}</style>
                <div style={{ display: 'flex', flexDirection: 'row', width: '100%' }}>
                <table className="table-widget">
                    <thead>
                        <tr>
                            <th>Title</th>
                        </tr>
                    </thead>
                    <tbody>
                        {papers.map(p => (
                            <tr>
                                <td>{p.title}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                <div className="column-manager">
                    <h4>Manage Columns</h4>
                    {columns.map(c => (
                        <div style={{ display: 'flex', flexDirection: 'column' }}>
                            <label>Column Name</label>
                            <input value={c.name} type="text" />
                            <label>Instructions</label>
                            <textarea>{c.instructions}</textarea>
                        </div>
                    ))}
                    <button>Add column</button>
                </div>
                </div>
            </>
          );
        }
        const render = createRender(Table);

        export default { render };
        """)
        papers = List(trait=Dict({}), default_value=[]).tag(sync=True)
        columns = List(trait=Dict({}), default_value=[]).tag(sync=True)


    table = TableWidget()
    table.papers = papers_for_table
    # TODO: sync with input/textarea elements
    table.columns = [
        {
            'name': 'Abstract Summary',
            'instructions': 'Please condense the abstract into a one-sentence summary.',
            'answer_structure': None,
        },
        {
            'name': 'Number of Cells',
            'instructions': 'In total, how many cells were profiled in this study?',
            'answer_structure': None,
        }
    ]
    table
    return TableWidget, table


@app.cell
def _():
    # References:
    # - https://docs.llamaindex.ai/en/stable/examples/llm/ollama/#structured-outputs
    # - https://docs.llamaindex.ai/en/stable/examples/cookbooks/oreilly_course_cookbooks/Module-8/Advanced_RAG_with_LlamaParse/#llamaparse-pdf-reader-for-pdf-parsing
    from llama_index.core import SimpleDirectoryReader
    from llama_index.llms.ollama import Ollama
    from llama_index.core.llms import ChatMessage
    from llama_index.core.bridge.pydantic import BaseModel
    from llama_parse import LlamaParse
    return BaseModel, ChatMessage, LlamaParse, Ollama, SimpleDirectoryReader


@app.cell
def _(Ollama):
    llm = Ollama(model="llama3.1:latest", request_timeout=120.0)
    return (llm,)


@app.cell
def _(ChatMessage, llm):
    messages = [
        ChatMessage(
            role="system", content="You are a pirate with a colorful personality"
        ),
        ChatMessage(role="user", content="What is your name"),
    ]
    resp = llm.chat(messages)
    return messages, resp


@app.cell
def _(resp):
    print(resp)
    return


@app.cell
def _(LLAMA_CLOUD_API_KEY, LlamaParse):
    parser = LlamaParse(result_type="markdown", api_key=LLAMA_CLOUD_API_KEY)
    # TODO: if no llamacloud API key, fall back to using Pymupdf
    # See https://github.com/keller-mark/sc-vis-scripts/blob/bd8a855e0f713f3557888b0bddc419bb0a0b7b9e/src/sc_star_scripts/alt_pdf_text_extraction.py#L7
    return (parser,)


@app.cell
async def _(papers_for_table, parser):
    documents = await parser.aload_data(papers_for_table[0]["filepath"])
    return (documents,)


@app.cell
def _(documents):
    print(documents[1].text)
    return


@app.cell
def _(ChatMessage, documents, llm):
    paper_messages = [
        ChatMessage(
            role="system", content="You are extracting information from a scientific document."
        ),
        ChatMessage(role="user", content=f"In total, how many cells were profiled in this study?\n{documents[0].text}"),
        # TODO: obtain structured outputs using Pydantic
        # See https://docs.llamaindex.ai/en/stable/examples/output_parsing/llm_program/
    ]
    paper_resp = llm.chat(paper_messages)
    return paper_messages, paper_resp


@app.cell
def _(paper_resp):
    print(paper_resp)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
