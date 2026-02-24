# from unstructured.partition.pdf import partition_pdf
# from app.rag.vision import describe_image

# def load_pdf(path):

#     elements = partition_pdf(
#         filename=path,
#         strategy="hi_res",
#         extract_images_in_pdf=True,
#         infer_table_structure=True
#     )

#     docs = []

#     for el in elements:

#         text = el.text or ""
#         category = el.category

#         if category == "Table":
#             text = f"TABLE CONTENT:\n{text}"

#         if category == "Image":
#             image_path = el.metadata.image_path

#             if image_path:
#                 description = describe_image(image_path)
#                 text = f"IMAGE DESCRIPTION:\n{description}"

#         docs.append({
#             "text": text,
#             "metadata": {
#                 "type": category,
#                 "page": el.metadata.page_number
#             }
#         })

#     return docs
from unstructured.partition.pdf import partition_pdf
from app.rag.vision import describe_image
from collections import defaultdict

# def load_pdf(path):
#     elements = partition_pdf(
#         filename=path,
#         strategy="hi_res",
#         extract_images_in_pdf=True,
#         infer_table_structure=True
#     )

#     docs = []

#     for el in elements:
#         text = el.text or ""
#         category = el.category

#         if len(text) < 15:
#             continue
               
        
#         if category in ["Title", "UncategorizedText"]:
#             continue

#         if category == "Table":
#             lines = [line.strip() for line in text.split("\n") if line.strip()]
#             for line in lines:
#                 docs.append({
#                     "text": f"TABLE ROW:\n{line}",
#                     "metadata": {
#                         "type": category,
#                         "page": el.metadata.page_number
#                     }
#                 })
#             continue 
#         if category == "Image":
#             # image_path = el.metadata.image_path
#             # if image_path:
#             #     description = describe_image(image_path)
#             #     text = f"IMAGE DESCRIPTION:\n{description}"
#             continue

#         docs.append({
#             "text": text,
#             "metadata": {
#                 "type": category,
#                 "page": el.metadata.page_number
#             }
#         })

#     return docs
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

        # Ignorer les textes trop courts
        if len(text.strip()) < 15:
            continue

        # Ignorer les titres et textes non catégorisés
        if category in ["Title", "UncategorizedText"]:
            continue

        # Gérer les tables
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

        # Ignorer les images pour l'instant (ou utiliser describe_image si tu veux)
        if category == "Image":
            # image_path = el.metadata.image_path
            # if image_path:
            #     description = describe_image(image_path)
            #     text = f"IMAGE DESCRIPTION:\n{description}"
            continue

        # Ajouter texte filtré
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

