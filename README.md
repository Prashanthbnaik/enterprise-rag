# RetrievalStack

RetrievalStack is a production-grade Retrieval-Augmented Generation (RAG) backend built for scalable document intelligence systems.

It provides hybrid retrieval, reranking, caching, persistent vector storage, and cloud deployment as a live API.

This project demonstrates end-to-end AI backend engineering, infrastructure awareness, and production deployment practices.

---

## Live Deployment

**Base URL**  
https://retrievalstack.up.railway.app  

**Swagger Documentation**  
https://retrievalstack.up.railway.app/docs  

**Health Check**  
GET /api/health  

---

## What This System Solves

Naive RAG systems often suffer from:

- Low retrieval precision  
- Hallucinated answers  
- No persistence  
- No caching  
- Weak deployment architecture  

RetrievalStack addresses these through:

- Hybrid dense + lexical retrieval  
- Cross-encoder reranking  
- Persistent vector storage  
- Distributed caching  
- Stateless API architecture  
- Cloud-native deployment  

---

## System Architecture

Client  
→ FastAPI (Stateless API Layer)  
→ Hybrid Retrieval Layer  
  • FAISS (Dense Search)  
  • BM25 (Lexical Search)  
→ CrossEncoder Reranker  
→ Groq LLM  
→ Redis Cache  
→ Persistent Volume Storage  

### Design Goals

- Stateless API
- Externalized storage
- Restart resilience
- Horizontal scaling readiness

---

## Core Architecture Principles

### 1. Layered Design

The system is divided into independent components:

- API Layer  
- Retrieval Layer  
- Reranking Layer  
- Generation Layer  
- Cache Layer  
- Storage Layer  

This ensures maintainability, scalability, and extensibility.

---

### 2. Stateless Service

FastAPI remains stateless. Persistent state is externalized:

- FAISS index stored on mounted volume  
- Uploaded documents stored persistently  
- Redis handles query caching  

This enables:

- Container restarts without data loss  
- Horizontal scaling  
- Deployment flexibility  

---

### 3. Multi-Stage Retrieval

RetrievalStack uses a three-stage retrieval pipeline:

1. Dense embedding search (Sentence Transformers + FAISS)  
2. Sparse lexical scoring (BM25)  
3. Cross-encoder reranking  

This improves retrieval precision compared to embedding-only RAG implementations.

---

### 4. Performance Optimization

Redis caching reduces:

- Repeated LLM calls  
- Latency  
- Inference cost  

Identical queries are served from cache.

---

## Technology Stack

### Backend
- FastAPI  
- Python 3.10  
- Uvicorn  

### Retrieval
- Sentence Transformers  
- FAISS  
- BM25  

### Reranking
- CrossEncoder  

### LLM
- Groq API  

### Caching
- Redis  

### Infrastructure
- Docker  
- Railway  
- Persistent Volume Storage  

---

## API Endpoints

### GET /
Returns service metadata.

### POST /api/upload
Indexes an uploaded document (PDF, CSV, or URL) into the vector store.

### POST /api/query
Performs hybrid retrieval, reranking, and LLM answer generation.

### GET /api/health
Used for deployment verification and monitoring.

---

## Example Query

**Request**

POST /api/query

```json
{
  "question": "Summarize the document"
}
```

**Response**

```json
{
  "answer": ""The documents discuss the concept of fine-tuning and LoRA (Low-Rank Adaptation) in the context of language modeling and other natural language processing tasks [Source 1, Source 2, Source 3]. LoRA is an approach that uses low-rank matrices for adaptation, eliminating the need for full-rank gradient updates to weight matrices [Source 3]. The goal of these approaches is to maximize conditional probabilities for each token, with the ultimate objective of improving model performance [Source 1, Source 2, Source 4, Source 5]. LoRA can be combined with other methods, such as prefix-tuning, to further optimize model performance [Source 4, Source 5]."",
  "contexts": [
    "context-output pairs:\nZ={(xi, yi)}i=1,...,N,\nwhere both xiandyiare sequences of tokens. For instance, in NL2SQL, xi\nmight represent a natural language question and yiwould be the corresponding\nSQL query; in summarization, xirepresents the article and yiwould be its\nsummary.\nIn traditional fine-tuning, the model is initialized using the pre-trained weights\nΦ0, which are then updated to Φ 0+ ∆Φ by optimizing the model’s parameters\nto maximize the conditional probabilities for each token:\nmax\nΦX",
    "context-output pairs:\nZ={(xi, yi)}i=1,...,N,\nwhere both xiandyiare sequences of tokens. For instance, in NL2SQL, xi\nmight represent a natural language question and yiwould be the corresponding\nSQL query; in summarization, xirepresents the article and yiwould be its\nsummary.\nIn traditional fine-tuning, the model is initialized using the pre-trained weights\nΦ0, which are then updated to Φ 0+ ∆Φ by optimizing the model’s parameters\nto maximize the conditional probabilities for each token:\nmax\nΦX",
    "trained parameters. LoRA extends this approach by eliminating the need for\nfull-rank gradient updates to weight matrices. Instead, LoRA uses low-rank\nmatrices for adaptation. If LoRA is applied to all weight matrices, and all\nbiases are trained, the expressiveness of full fine-tuning is recovered by setting\nthe LoRA rank requal to the rank of the pre-trained weight matrices. As the\nnumber of trainable parameters increases, LoRA approaches the full fine-tuning",
    "•Combining with Other Methods : LoRA can be used with other ap-\nproaches, like prefix-tuning, to further optimize model performance.\n2 Problem Statement\nAlthough our approach is independent of the specific training objective, we focus\non language modeling as the central application. Below, we outline the key\naspects of the language modeling problem, particularly the goal of maximizing\nconditional probabilities based on task-specific prompts.",
    "•Combining with Other Methods : LoRA can be used with other ap-\nproaches, like prefix-tuning, to further optimize model performance.\n2 Problem Statement\nAlthough our approach is independent of the specific training objective, we focus\non language modeling as the central application. Below, we outline the key\naspects of the language modeling problem, particularly the goal of maximizing\nconditional probabilities based on task-specific prompts."],
  "latency": 1.124
}
```

---

## Local Development

Clone the repository:

```bash
git clone <repository-url>
cd retrievalstack
```

Build and run:

```bash
docker compose up --build
```

Open:

http://localhost:8000/docs

---

## Production Deployment

- Dockerized container  
- Railway cloud hosting  
- Dynamic port binding  
- Persistent volume attached  
- Redis deployed  
- Healthcheck enabled  
- Restart policy configured  

**Allocated Resources**

- 2 vCPU  
- 1 GB RAM  

The system preserves the FAISS index across deployments.

---

## Environment Configuration

Required environment variables:

```
GROQ_API_KEY=GROQ_API_KEY
REDIS_HOST=redis
REDIS_PORT=6379
```

---

## Potential Enhancements

- Multi-tenant document isolation  
- JWT authentication  
- API key management  
- Rate limiting  
- Structured logging  
- Observability (Prometheus / Grafana)  
- Horizontal scaling with replicas  

---

## Project Objective

RetrievalStack was built to demonstrate:

- AI backend engineering  
- Infrastructure-aware design  
- Retrieval optimization strategies  
- Production deployment practices  
- Cloud-native API architecture  

This is not a notebook prototype.  
It is a deployed, persistent AI backend engineered using production principles.
