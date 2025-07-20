from google.cloud import firestore

db = firestore.Client()

def store_summary_to_firestore(workflow_id: str, summary: str):
    doc_ref = db.collection("summaries").document(workflow_id)
    doc_ref.set({"summary": summary})

def get_summary_from_firestore(workflow_id: str) -> str:
    doc = db.collection("summaries").document(workflow_id).get()
    return doc.to_dict().get("summary") if doc.exists else None

def store_scraped_data(workflow_id: str, data: dict):
    db.collection("scraped_data").document(workflow_id).set(data)
