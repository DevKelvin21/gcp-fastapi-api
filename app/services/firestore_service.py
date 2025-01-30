import os
from google.cloud import firestore

ENV_VAR_MSG = "Specified environment variable is not set."

class FirestoreService:
    def __init__(self):
        self.client = firestore.Client()
        self.collection_name = os.environ.get("FIRESTORE_COLLECTION", ENV_VAR_MSG)

    def create_document(self, data: dict) -> str:
        """
        Creates a new document in Firestore with the provided data.
        Returns the document ID.
        """
        doc_ref = self.client.collection(self.collection_name).document()
        doc_ref.set(data)
        return doc_ref.id

    def get_document(self, doc_id: str) -> dict:
        doc_ref = self.client.collection(self.collection_name).document(doc_id)
        doc_snapshot = doc_ref.get()
        if doc_snapshot.exists:
            return doc_snapshot.to_dict()
        return None

    def list_documents(self) -> list:
        docs = self.client.collection(self.collection_name).stream()
        return [{"id": doc.id, **doc.to_dict()} for doc in docs]

    def update_document(self, doc_id: str, data: dict) -> bool:
        doc_ref = self.client.collection(self.collection_name).document(doc_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.update(data)
        return True

    def delete_document(self, doc_id: str) -> bool:
        doc_ref = self.client.collection(self.collection_name).document(doc_id)
        if not doc_ref.get().exists:
            return False
        doc_ref.delete()
        return True
