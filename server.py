import os
import chromadb
import openai
import logging
from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer

# Setup logging for debugging
logging.basicConfig(level=logging.INFO)

# Initialize FastAPI
app = FastAPI()

# Initialize ChromaDB (Vector Database)
chroma_client = chromadb.PersistentClient(path="./chroma_db")  # Stores vectors locally
collection = chroma_client.get_or_create_collection("pdf_knowledge")

# Initialize Sentence Transformer Model (For Text Embeddings)
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# OpenAI API Key (Set in Render or .env)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract text, and store it in ChromaDB as embeddings.
    """
    try:
        logging.info(f"Received PDF upload request: {file.filename}")

        # Read the PDF
        pdf_reader = PdfReader(file.file)
        text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        
        if not text:
            return {"error": "No text could be extracted from the PDF."}

        # Split text into smaller chunks (optional)
        chunks = [text[i:i+500] for i in range(0, len(text), 500)]

        # Convert text chunks into embeddings
        embeddings = embedder.encode(chunks).tolist()

        # Store in ChromaDB
        for i, chunk in enumerate(chunks):
            collection.add(
                ids=[f"{file.filename}-{i}"],
                documents=[chunk],
                metadatas=[{"source": file.filename}]
            )

        logging.info(f"PDF '{file.filename}' processed and stored successfully!")

        return {"message": f"PDF '{file.filename}' processed and stored successfully!"}

    except Exception as e:
        logging.error(f"Error processing PDF '{file.filename}': {str(e)}")
        return {"error": str(e)}


@app.get("/vraag/{query}")
async def answer_question(query: str):
    """
    Search for the most relevant information in ChromaDB and return an answer.
    """
    try:
        logging.info(f"Received question: {query}")

        # Convert query to vector
        query_embedding = embedder.encode([query]).tolist()

        # Retrieve relevant chunks from ChromaDB
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=3  # Return top 3 most relevant matches
        )

        # If no relevant data is found, return an error
        if not results["documents"] or not results["documents"][0]:
            logging.warning(f"No relevant information found for query: {query}")
            return {"antwoord": "Sorry, geen relevante informatie gevonden in de PDF-database."}

        # Combine the top results as context
        context = " ".join(results["documents"][0])

        logging.info(f"Using context for answer: {context[:500]}...")

        # Generate an answer using OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Geef een nauwkeurig antwoord gebaseerd op de volgende PDF-informatie."},
                {"role": "user", "content": f"Vraag: {query} \n\n PDF Informatie: {context}"}
            ]
        )

        return {"antwoord": response["choices"][0]["message"]["content"]}

    except Exception as e:
        logging.error(f"Error processing question '{query}': {str(e)}")
        return {"error": str(e)}
