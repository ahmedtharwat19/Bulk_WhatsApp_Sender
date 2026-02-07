import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# جرب إضافة مستند تجريبي
doc_ref = db.collection("test").document("hello")
doc_ref.set({"msg": "hello world"})
print("✅ Connection successful, document added!")
