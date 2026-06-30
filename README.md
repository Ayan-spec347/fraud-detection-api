# Real-Time Fraud Detection Engine & API 

An end-to-end machine learning pipeline and low-latency RESTful API designed to detect fraudulent financial transactions in real-time. 

This project bridges the gap between complex data science and production-ready software engineering. It utilizes high-dimensional graph-topology features to isolate botnet rings and deploys the optimized model via a fully containerized FastAPI backend.

##  Tech Stack
* **Machine Learning:** Python, XGBoost, Scikit-Learn, Pandas
* **Graph Processing:** NetworkX
* **Backend Architecture:** FastAPI, Uvicorn
* **DevOps / Deployment:** Docker, Git

##  Key Technical Highlights
* **Low-Latency API:** Architected a RESTful API capable of parsing live financial JSON payloads and returning integrated ML predictions in **under 50 milliseconds**.
* **Graph-Topology Engineering:** Utilized **NetworkX** to map bipartite network structures, dynamically isolating multi-node botnet rings from standard network traffic.
* **Optimized ML Performance:** Trained an XGBoost classifier on heavily imbalanced temporal data, achieving a **0.20 PR-AUC** (outperforming standard baselines).
* **Business-Logic Alignment:** Shifted probability decision thresholds to **0.90** to drastically minimize false-positive customer friction during live transaction processing.
* **Production-Ready Deployment:** Fully containerized the application environment using **Docker** for scalable, isolated deployment.

##  Project Structure
```text
├── api/
│   ├── main.py              # FastAPI application and routing
│   └── test_api.py          # API testing scripts
├── models/                  # Serialized XGBoost models (*.pkl)
├── notebooks/               # Jupyter notebooks for EDA and ML pipeline
├── Dockerfile               # Containerization instructions
├── requirements.txt         # Python dependencies
└── .gitignore
