#!/usr/bin/env python3
"""
Management script for Provon backend database
Use this to manage your persistent knowledge base
"""

import sys
import os
from backend_db import BackendDatabase
from base_knowledge import BaseKnowledge
from document_processor import DocumentProcessor

def show_menu():
    print("\n" + "="*50)
    print("🧠 Provon Backend Manager")
    print("="*50)
    print("1. View database statistics")
    print("2. Clear database")
    print("3. Add documents from file")
    print("4. Export database info")
    print("5. Reset to base knowledge only")
    print("0. Exit")
    print("="*50)

def view_stats():
    db = BackendDatabase()
    stats = db.get_stats()
    print(f"\n📊 Database Statistics:")
    print(f"   Total documents: {stats['total_documents']}")
    print(f"   Last updated: {stats['last_updated']}")
    
    # Show sources
    metadata = db.get_all_metadata()
    sources = {}
    for meta in metadata:
        source = meta.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print(f"\n📚 Documents by source:")
    for source, count in sources.items():
        print(f"   {source}: {count} chunks")

def clear_database():
    confirm = input("\n⚠️  Are you sure you want to clear the database? (yes/no): ")
    if confirm.lower() == 'yes':
        db = BackendDatabase()
        db.clear_database()
        print("✅ Database cleared!")
    else:
        print("❌ Cancelled")

def add_documents_from_file():
    file_path = input("\nEnter file path (PDF, TXT, or DOCX): ").strip()
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return
    
    print(f"📄 Processing: {file_path}")
    
    processor = DocumentProcessor()
    text = processor.process_file(file_path)
    
    if text.startswith("Error"):
        print(f"❌ {text}")
        return
    
    chunks = processor.chunk_text(text)
    print(f"✅ Created {len(chunks)} chunks")
    
    db = BackendDatabase()
    filename = os.path.basename(file_path)
    
    # Create embeddings (simple for now)
    embeddings = [None] * len(chunks)
    metadata = [{"source": filename, "file_path": file_path, "type": "user"} for _ in chunks]
    
    db.add_documents(chunks, embeddings, metadata)
    print(f"✅ Added {len(chunks)} chunks to database!")

def export_database_info():
    db = BackendDatabase()
    output_file = "database_export.txt"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Provon Database Export\n")
        f.write("="*50 + "\n\n")
        
        stats = db.get_stats()
        f.write(f"Total documents: {stats['total_documents']}\n")
        f.write(f"Last updated: {stats['last_updated']}\n\n")
        
        documents = db.get_all_documents()
        metadata = db.get_all_metadata()
        
        for i, (doc, meta) in enumerate(zip(documents, metadata)):
            f.write(f"\n--- Document {i+1} ---\n")
            f.write(f"Source: {meta.get('source', 'Unknown')}\n")
            f.write(f"Type: {meta.get('type', 'Unknown')}\n")
            f.write(f"Content: {doc[:200]}...\n")
    
    print(f"✅ Database exported to {output_file}")

def reset_to_base_knowledge():
    confirm = input("\n⚠️  Reset database to base knowledge only? (yes/no): ")
    if confirm.lower() == 'yes':
        db = BackendDatabase()
        db.clear_database()
        
        base = BaseKnowledge()
        base_docs = base.get_base_knowledge()
        base_embeddings = [None] * len(base_docs)
        base_metadata = [{"source": "Base Knowledge (llama2b)", "type": "base"} for _ in base_docs]
        
        db.add_documents(base_docs, base_embeddings, base_metadata)
        print("✅ Database reset to base knowledge!")
    else:
        print("❌ Cancelled")

def main():
    while True:
        show_menu()
        choice = input("Select option: ").strip()
        
        if choice == '1':
            view_stats()
        elif choice == '2':
            clear_database()
        elif choice == '3':
            add_documents_from_file()
        elif choice == '4':
            export_database_info()
        elif choice == '5':
            reset_to_base_knowledge()
        elif choice == '0':
            print("\n👋 Goodbye!")
            break
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    main()
