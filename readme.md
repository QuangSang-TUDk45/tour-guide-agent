# Multi-Agent System: Quy Nhon Tour Guide Assistant 

![Banner](img/banner.png)

## Overview
Quy Nhon Tour Guide Assistant is an intelligent, multi-agent digital assistant designed to provide a seamless and authentic travel experience in Quy Nhon, Binh Dinh. Unlike generic AI chatbots, this system is strictly grounded in a curated local database, ensuring that every recommendation—from hidden culinary gems to scenic coastal landmarks—is accurate and reliable.

Key Features:
- Intelligent Intent Orchestration: Automatically classifies user queries into categories such as local food, restaurants, destinations, or comprehensive trip planning.

- Personalized Itinerary Planner: Generates detailed day-by-day schedules based on user-defined constraints, including duration, budget, and specific preferences (e.g., seafood, beach activities).

- Database-Grounded Recommendations: Powered by a PostgreSQL backend, the system utilizes string-similarity matching to retrieve the most relevant local data without hallucinations.

- Modern Full-Stack Architecture: Built with a high-performance FastAPI backend and an intuitive Streamlit frontend for a smooth, real-time chat experience.

## Guide line for setup:
1. Open cmd and run command "pip install -r requirements.txt".
2. Init .env file with:
    - HF_TOKEN="Token of Hugging Face here"
    - DB_PASS="PostgreSQL password here"
    - DB_URL = "postgresql://postgres:"""PostgreSQL password here"""@localhost:5432/BinhDinh_TourGuide"
    - data_path = "data\data_raw.xlsx"
2. Run file create_database.py.
3. Run file convert_excel_to_postgre.py.
4. Open cmd and run command "uvicorn main:app --reload".
5. Open cmd and run command "streamlit run app.py".