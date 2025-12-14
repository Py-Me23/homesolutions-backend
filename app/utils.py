# app/utils.py

from dotenv import load_dotenv

load_dotenv()  # Ensure environment variables are loaded

def replace_mongo_id(doc):
    """
    Replace MongoDB '_id' field with 'id' as a string.

    Args:
        doc (dict or list): A single document or a list of documents from MongoDB.

    Returns:
        dict or list: Document(s) with '_id' replaced by 'id'.
    """
    if isinstance(doc, list):
        return [replace_mongo_id(d) for d in doc]

    if "_id" in doc:
        doc["id"] = str(doc["_id"])
        del doc["_id"]
    return doc
