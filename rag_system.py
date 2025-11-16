import ollama
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import sys

# Import the document processor and backend systems
from document_processor import DocumentProcessor
from backend_db import BackendDatabase
from base_knowledge import BaseKnowledge

# Try to import sentence-transformers, fallback to simpler method
HAS_SENTENCE_TRANSFORMERS = False
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
    print("✅ sentence-transformers available")
except Exception as e:
    print(f"⚠️ sentence-transformers failed: {e}")
    print("⚠️  Using simple keyword-based search")

class PurePythonRAG:
    def __init__(self):
        print("🚀 Initializing Provon RAG System with Backend Database...")
        self.doc_processor = DocumentProcessor()
        self.backend_db = BackendDatabase()
        self.base_knowledge = BaseKnowledge()
        self.has_sentence_transformers = HAS_SENTENCE_TRANSFORMERS
        
        # Initialize embedding model if available
        if self.has_sentence_transformers:
            try:
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("✅ Using sentence-transformers for embeddings")
            except Exception as e:
                print(f"⚠️ Sentence transformers failed: {e}")
                self.has_sentence_transformers = False
        else:
            print("⚠️  Using simple keyword-based search")
        
        # Load documents from backend database
        self.documents = self.backend_db.get_all_documents()
        self.embeddings = self.backend_db.get_all_embeddings()
        self.metadata = self.backend_db.get_all_metadata()
        
        # Merge with base knowledge if no user documents exist
        if not self.documents:
            print("📚 Loading base knowledge (llama2b)...")
            base_docs = self.base_knowledge.get_base_knowledge()
            base_embeddings = [None] * len(base_docs)
            base_metadata = [{"source": "Base Knowledge (llama2b)", "type": "base"} for _ in base_docs]
            
            self.documents = base_docs
            self.embeddings = base_embeddings
            self.metadata = base_metadata
            self.backend_db.add_documents(base_docs, base_embeddings, base_metadata)
        
        print(f"🎉 Provon RAG System Ready! ({len(self.documents)} documents loaded)")
    
    def add_documents(self, file_paths):
        """Add documents to the knowledge base and save to backend"""
        chunk_count = 0
        new_documents = []
        new_embeddings = []
        new_metadata = []
        
        for file_path in file_paths:
            filename = os.path.basename(file_path)
            print(f"📄 Processing: {filename}")
            
            text = self.doc_processor.process_file(file_path)
            if text.startswith("Error"):
                print(f"   ❌ Failed: {text}")
                continue
                
            chunks = self.doc_processor.chunk_text(text)
            print(f"   ✅ Created {len(chunks)} chunks")
            
            for chunk in chunks:
                # Store the chunk
                self.documents.append(chunk)
                new_documents.append(chunk)
                
                meta = {"source": filename, "file_path": file_path, "type": "user"}
                self.metadata.append(meta)
                new_metadata.append(meta)
                
                # Generate embedding if using sentence-transformers
                if self.has_sentence_transformers:
                    try:
                        embedding = self.embedding_model.encode([chunk])[0]
                        self.embeddings.append(embedding)
                        new_embeddings.append(embedding)
                    except Exception as e:
                        print(f"   ⚠️  Embedding failed: {e}")
                        # Add placeholder
                        placeholder = np.zeros(384)
                        self.embeddings.append(placeholder)
                        new_embeddings.append(placeholder)
                else:
                    # Simple bag-of-words style representation
                    words = chunk.lower().split()
                    word_set = set(words)
                    self.embeddings.append(word_set)
                    new_embeddings.append(word_set)
                
                chunk_count += 1
        
        # Save to backend database
        if new_documents:
            self.backend_db.add_documents(new_documents, new_embeddings, new_metadata)
        
        print(f"📊 Total knowledge base: {len(self.documents)} chunks")
        return chunk_count
    
    def simple_similarity(self, query, chunk_data):
        """Simple similarity calculation for keyword matching"""
        if isinstance(chunk_data, set):
            # For word sets
            query_words = set(query.lower().split())
            common_words = len(query_words.intersection(chunk_data))
            return common_words / len(query_words) if query_words else 0
        else:
            # For embeddings
            return 0.5  # Default medium similarity
    
    def query(self, question, num_results=5):
        """Query the knowledge base with base knowledge fallback"""
        print(f"🔍 Querying: {question}")
        
        if not self.documents:
            # Fallback to base knowledge
            fallback_answer = self.base_knowledge.get_fallback_answer(question)
            return {
                "answer": fallback_answer,
                "sources": ["Base Knowledge (llama2b)"],
                "context_chunks": [fallback_answer],
                "scores": [0.8]
            }
        
        try:
            # Calculate similarities
            similarities = []
            
            if self.has_sentence_transformers and self.embeddings:
                # Use proper semantic search
                query_embedding = self.embedding_model.encode([question])[0]
                for emb in self.embeddings:
                    if isinstance(emb, np.ndarray):
                        sim = cosine_similarity([query_embedding], [emb])[0][0]
                        similarities.append(sim)
                    else:
                        similarities.append(0.1)
            else:
                # Use keyword matching
                for chunk_data in self.embeddings:
                    sim = self.simple_similarity(question, chunk_data)
                    similarities.append(sim)
            
            # Get top results
            top_indices = np.argsort(similarities)[-num_results:][::-1]
            
            # Build context from top results
            context = ""
            sources = []
            context_chunks = []
            scores = []
            
            for idx in top_indices:
                if similarities[idx] > 0.1:  # Minimum threshold
                    chunk = self.documents[idx]
                    source = self.metadata[idx]['source']
                    score = similarities[idx]
                    
                    context += f"📚 From {source} (relevance: {score:.2f}):\n{chunk}\n\n"
                    if source not in sources:
                        sources.append(source)
                    context_chunks.append(chunk)
                    scores.append(score)
            
            if not context:
                # Use base knowledge as fallback
                fallback_answer = self.base_knowledge.get_fallback_answer(question)
                context = f"📚 From Base Knowledge (llama2b):\n{fallback_answer}\n\n"
                sources = ["Base Knowledge (llama2b)"]
                context_chunks = [fallback_answer]
                scores = [0.7]
            
            # Create prompt for Ollama
            prompt = f"""Based ONLY on the following context from my documents, answer the question.

CONTEXT:
{context}

QUESTION: {question}

IMPORTANT RULES:
1. Use ONLY information from the provided context
2. If the answer isn't in the context, say "This information is not available in my documents"
3. Format your answer clearly
4. Mention which documents contained the information

ANSWER:"""
            
            # Get response from Ollama
            try:
                response = ollama.generate(model='llama2:latest', prompt=prompt)
                answer = response['response']
            except Exception as e:
                answer = f"🤖 AI Error: {str(e)}\n\n💡 Make sure Ollama is running with 'ollama serve'"
            
            return {
                "answer": answer,
                "sources": sources,
                "context_chunks": context_chunks,
                "scores": scores
            }
            
        except Exception as e:
            return {
                "answer": f"❌ Search error: {str(e)}",
                "sources": [],
                "context_chunks": [],
                "scores": []
            }
    
    def get_collection_info(self):
        """Get information about the knowledge base"""
        return f"📊 Knowledge base: {len(self.documents)} document chunks"