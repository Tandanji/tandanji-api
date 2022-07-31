from firebase_admin import firestore

class Repository():
  def __init__(self) -> None:
    self.db=firestore.client()
  def setData(self):
    doc_ref = self.db.collection(u'users').document(u'alovelace')
    doc_ref.set({
        u'first': u'Ada',
        u'last': u'Lovelace',
        u'born': 1815
    })
