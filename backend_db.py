import json
import os
from datetime import datetime
import pickle

class BackendDatabase:
    """Persistent backend database for Provon"""
    
    def __init__(self, db_path="data/provon_db.pkl"):
        self.db_path = db_path
        self.data = {
            "documents": [],
            "embeddings": [],
            "metadata": [],
            "last_updated": None
        }
        self.ensure_db_exists()
        self.load_database()
    
    def ensure_db_exists(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.db_path) if os.path.dirname(self.db_path) else ".", exist_ok=True)
    
    def load_database(self):
        """Load database from disk"""
        if os.path.exists(self.db_path):
            try:
                with open(self.db_path, 'rb') as f:
                    self.data = pickle.load(f)
                print(f"✅ Loaded {len(self.data['documents'])} documents from backend database")
            except Exception as e:
                print(f"⚠️ Error loading database: {e}")
                self.data = {
                    "documents": [],
                    "embeddings": [],
                    "metadata": [],
                    "last_updated": None
                }
        else:
            print("📝 Creating new backend database...")
    
    def save_database(self):
        """Save database to disk"""
        try:
            with open(self.db_path, 'wb') as f:
                pickle.dump(self.data, f)
            self.data["last_updated"] = datetime.now().isoformat()
            print(f"✅ Database saved with {len(self.data['documents'])} documents")
        except Exception as e:
            print(f"❌ Error saving database: {e}")
    
    def add_documents(self, documents, embeddings, metadata):
        """Add documents to the backend database"""
        self.data["documents"].extend(documents)
        self.data["embeddings"].extend(embeddings)
        self.data["metadata"].extend(metadata)
        self.data["last_updated"] = datetime.now().isoformat()
        self.save_database()
        return len(self.data["documents"])
    
    def get_all_documents(self):
        """Get all documents from backend"""
        return self.data["documents"]
    
    def get_all_embeddings(self):
        """Get all embeddings from backend"""
        return self.data["embeddings"]
    
    def get_all_metadata(self):
        """Get all metadata from backend"""
        return self.data["metadata"]
    
    def clear_database(self):
        """Clear all data from database"""
        self.data = {
            "documents": [],
            "embeddings": [],
            "metadata": [],
            "last_updated": None
        }
        self.save_database()
        print("🗑️ Database cleared")
    
    def get_stats(self):
        """Get database statistics"""
        return {
            "total_documents": len(self.data["documents"]),
            "last_updated": self.data["last_updated"]
        }
