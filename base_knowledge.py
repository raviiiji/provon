"""
Base knowledge system that merges user data with llama2b general knowledge
"""

BASE_KNOWLEDGE_CHUNKS = [
    # General knowledge base (llama2b style)
    "Llama 2 is a large language model developed by Meta. It is trained on a diverse range of internet text data and can perform various natural language processing tasks.",
    "Machine learning is a subset of artificial intelligence that enables systems to learn and improve from experience without being explicitly programmed.",
    "Python is a high-level, interpreted programming language known for its simplicity and readability. It is widely used in data science, web development, and automation.",
    "Natural Language Processing (NLP) is a branch of AI that focuses on enabling computers to understand, interpret, and generate human language in a meaningful way.",
    "Deep learning is a subset of machine learning based on artificial neural networks with multiple layers. It has revolutionized computer vision and NLP.",
    "Data science involves extracting insights from data using statistics, mathematics, and programming. It combines domain expertise with technical skills.",
    "Cloud computing provides on-demand access to computing resources over the internet. Major providers include AWS, Google Cloud, and Microsoft Azure.",
    "APIs (Application Programming Interfaces) allow different software applications to communicate with each other and share data or functionality.",
    "Databases store and organize data for efficient retrieval and management. Common types include relational databases (SQL) and NoSQL databases.",
    "Web development involves creating and maintaining websites and web applications. It includes frontend (HTML, CSS, JavaScript) and backend development.",
    "DevOps combines software development and IT operations to shorten development cycles and improve deployment frequency.",
    "Cybersecurity involves protecting computer systems and networks from digital attacks and unauthorized access.",
    "Artificial Intelligence (AI) refers to machines that can perform tasks that typically require human intelligence, such as learning and problem-solving.",
    "Blockchain is a distributed ledger technology that records transactions across multiple computers in a secure and transparent manner.",
    "The internet is a global system of interconnected networks that allows computers to communicate and share information worldwide.",
    "Software engineering is the systematic application of engineering approaches to software development, focusing on quality and efficiency.",
    "Version control systems like Git help developers track changes to code and collaborate on projects effectively.",
    "Testing is a critical part of software development that ensures code works as expected and meets requirements.",
    "Agile methodology is an iterative approach to software development that emphasizes flexibility, collaboration, and continuous improvement.",
    "Microservices architecture breaks down applications into small, independent services that can be developed and deployed separately.",
]

class BaseKnowledge:
    """Manages base knowledge and merges with user data"""
    
    def __init__(self):
        self.base_chunks = BASE_KNOWLEDGE_CHUNKS
        print(f"✅ Loaded {len(self.base_chunks)} base knowledge chunks (llama2b style)")
    
    def get_base_knowledge(self):
        """Get all base knowledge chunks"""
        return self.base_chunks
    
    def merge_with_user_data(self, user_documents, user_embeddings, user_metadata):
        """
        Merge user data with base knowledge
        Returns combined documents, embeddings, and metadata
        """
        merged_documents = self.base_chunks + user_documents
        merged_metadata = [{"source": "Base Knowledge (llama2b)", "type": "base"} for _ in self.base_chunks]
        merged_metadata.extend(user_metadata)
        
        # For embeddings, we'll handle them separately since base knowledge needs encoding
        merged_embeddings = [None] * len(self.base_chunks)  # Will be encoded on demand
        merged_embeddings.extend(user_embeddings)
        
        print(f"✅ Merged {len(user_documents)} user documents with {len(self.base_chunks)} base knowledge chunks")
        
        return merged_documents, merged_embeddings, merged_metadata
    
    def get_fallback_answer(self, question):
        """
        Provide a fallback answer from base knowledge if user data doesn't have answer
        This prevents "not found" responses
        """
        keywords = question.lower().split()
        
        # Simple keyword matching with base knowledge
        for chunk in self.base_chunks:
            chunk_lower = chunk.lower()
            if any(keyword in chunk_lower for keyword in keywords if len(keyword) > 3):
                return chunk
        
        # Default fallback
        return "I can help with general knowledge about technology, programming, AI, and software development. Please ask a more specific question or upload documents for domain-specific information."
