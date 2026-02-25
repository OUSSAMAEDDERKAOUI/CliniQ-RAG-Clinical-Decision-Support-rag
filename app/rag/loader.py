
from unstructured.partition.pdf import partition_pdf
from app.rag.vision import describe_image
from collections import defaultdict

def load_pdf(path):
    elements = partition_pdf(
        filename=path,
        strategy="hi_res",
        extract_images_in_pdf=True,
        infer_table_structure=True
    )

    docs = []

    for el in elements:
        text = el.text or ""
        category = el.category

        if len(text.strip()) < 15:
            continue

        if category in ["Title", "UncategorizedText"]:
            continue

        if category == "Table":
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            for line in lines:
                docs.append({
                    "text": f"TABLE ROW:\n{line}",
                    "metadata": {
                        "type": category,
                        "page": el.metadata.page_number
                    }
                })
            continue

        if category == "Image":
            # image_path = el.metadata.image_path
            # if image_path:
            #     description = describe_image(image_path)
            #     text = f"IMAGE DESCRIPTION:\n{description}"
            continue

        docs.append({
            "text": text,
            "metadata": {
                "type": category,
                "page": el.metadata.page_number
            }
        })

    return docs



def group_docs_by_page(docs):
    texts_by_page = defaultdict(list)
    for d in docs:
        page = d["metadata"]["page"]
        texts_by_page[page].append(d["text"])
    grouped_docs = []
    for page, texts in texts_by_page.items():
        grouped_docs.append({
            "text": " ".join(texts),
            "metadata": {"page": page}
        })
    return grouped_docs



from unstructured.partition.pdf import partition_pdf
from collections import defaultdict
import pandas as pd

def table_element_to_rows(el):
    md = el.metadata

    html = None
    for key in ["text_as_html", "table_as_html", "html"]:
        if hasattr(md, key) and getattr(md, key):
            html = getattr(md, key)
            break

    if not html:
        return []  # fallback possible

    dfs = pd.read_html(html)
    if not dfs:
        return []

    df = dfs[0].copy()
    df.columns = [str(c).strip() for c in df.columns]
    df = df.fillna("")

    # utile si cellules vides sur certaines lignes (souvent le cas)
    df = df.replace("", pd.NA).ffill().fillna("")

    page = md.page_number
    rows = []
    for i, row in df.iterrows():
        parts = []
        for col in df.columns:
            val = str(row[col]).strip()
            if val:
                parts.append(f"{col}: {val}")
        if parts:
            rows.append({
                "text": " | ".join(parts),
                "metadata": {"type": "TableRow", "page": page, "row_index": int(i)}
            })
    return rows


def load_pdf(path):
    elements = partition_pdf(
        filename=path,
        strategy="hi_res",
        extract_images_in_pdf=True,
        infer_table_structure=True
    )

    docs = []
    for el in elements:
        category = el.category
        text = (el.text or "").strip()

        if category in ["Title", "UncategorizedText", "Image"]:
            continue

        if category == "Table":
            row_docs = table_element_to_rows(el)
            if row_docs:
                docs.extend(row_docs)
            else:
                # fallback si pas de html : on garde ton ancien mode
                lines = [line.strip() for line in text.split("\n") if line.strip()]
                for line in lines:
                    docs.append({
                        "text": f"TABLE LINE:\n{line}",
                        "metadata": {"type": "TableLine", "page": el.metadata.page_number}
                    })
            continue

        if len(text) < 15:
            continue

        docs.append({
            "text": text,
            "metadata": {"type": category, "page": el.metadata.page_number}
        })

    return docs

