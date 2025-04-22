This project is a full-stack AI-powered image similarity engine built using Streamlit, Qdrant vector database, and transformer-based deep learning model RestNet-50. It allows users to explore visually similar images across three classes: cat, dog, and wild.

The backend processes each image to extract semantic embeddings using ResNet-50, stores them in Qdrant, and enables real-time similarity search based on a selected reference image.


Use Case:

i) Visual search based on similarity

ii) Multiclass categorization: cat, dog, wild

iii) Efficient search across high-dimensional feature vectors


Tech Stack:

i) For Frontend, I used Streamlit

ii) For Embedding Model: ResNet-50 (from HuggingFace Transformers)

iii) For Vector Storage: Qdrant Cloud

iv) Programming: Python language


Features:

i) Upload and preprocess images by class

ii) Generate embeddings using microsoft/resnet-50

iii) Store embeddings and metadata in Qdrant vector DB

iv) Streamlit interface for selecting class (cat, dog, wild)

v) Display similar images dynamically on user interaction


How It Works:

1. Image Embedding:

i) All images (from ./afhq/train/{class} folders) are resized to maintain aspect ratio

ii) Images are passed through ResNet-50 to extract logits as feature embeddings

iii) Embeddings are stored alongside metadata (class, base64 image, path)


3. Vector Storage:
   
i) Embeddings are stored in Qdrant with the following config:

ii) VectorParams(size=embedding_length, distance=Distance.COSINE)

iii) Each class (cat, dog, wild) has a unique ID offset (0, 10000, 20000 respectively)


5. Interactive App:
   
i) Streamlit loads initial images by class

ii) When a user clicks "Find similar images," nearest neighbors are queried using Qdrant

iii) Filtered results by type are displayed in a grid layout



Setup and Run:

1) Prerequisites:
   
Python 3.8+

HuggingFace Transformers

Qdrant Client


3) Clone and Install:
   
git clone https://github.com/raya-jahan/Multiclass_Image_Similarity_Finding_AI.git

cd Multiclass_Image_Similarity_Finding_AI

pip install -r requirements.txt


5) Set Environment:
   
Create a .env file

QDRANT_DB_URL=https://your-qdrant-url

QDRANT_API_KEY=your-secret-api-key


7) Generate Embeddings:
   
Run the embedding script

python get-image-embeddings.py


9) Launch the App:
    
streamlit run app.py



Folder Structure:

Multiclass_Image_Similarity_Finding_AI/

├── app.py                     # Streamlit frontend

├── get-image-embeddings.py   # Embedding + upload logic

├── .env                      # Secrets for Qdrant

├── README.md

└── ./afhq/train/             # Image data (cat/dog/wild)



Future Work:

i) Add image upload and dynamic indexing

ii) Support pagination and filters

iii) Use ONNX or quantized models for real-time performance

iv) Deploy to Streamlit Cloud with persistent DB connection



