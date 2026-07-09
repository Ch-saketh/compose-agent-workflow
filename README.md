# Composio AI Product Operations – Take-Home Assignment

An autonomous AI-powered research pipeline that evaluates SaaS applications for integration readiness by discovering official documentation, extracting structured metadata, verifying the results, benchmarking applications, and automatically generating an HTML case study.

---

## 🚀 Live Demo

**Live HTML Case Study**

https://ai-product-research-pipeline-qsqi-rmkj38etb.vercel.app

**Portfolio**

https://saketh-chokkapu-portfolio.vercel.app

---

## 📌 Overview

Evaluating SaaS applications manually is repetitive and time-consuming. This project automates the workflow by researching official documentation, extracting integration-related information, validating the extracted results, and generating a structured engineering report.

The pipeline follows a modular multi-agent architecture, making it easy to extend, debug, and scale.

---

## ✨ Features

- AI-powered documentation research
- Official documentation discovery
- Structured JSON output
- Verification with confidence scoring
- Benchmark analysis across applications
- Interactive HTML case study generation
- Modular pipeline architecture
- Easily extensible for additional applications

---

## 🏗️ System Architecture

```text
                 apps.csv
                     │
                     ▼
            Discovery Agent
                     │
                     ▼
             Research Agent
                     │
                     ▼
           Verification Agent
                     │
                     ▼
          Verified JSON Output
                     │
                     ▼
                Analyzer
                     │
                     ▼
          HTML Report Generator
                     │
                     ▼
        Interactive HTML Report
```

---

## 📂 Project Structure

```text
project/
│
├── data/
│   ├── apps.csv
│   └── processed/
│
├── src/
│   ├── main.py
│   ├── pipeline.py
│   ├── discovery.py
│   ├── researcher.py
│   ├── verifier.py
│   ├── analyzer.py
│   ├── report.py
│   └── utils.py
│
├── templates/
│   └── report.html
│
├── output/
│   ├── report.html
│   ├── style.css
│   └── script.js
│
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🧠 Pipeline Components

### Discovery Agent

Finds official developer resources such as:

- Developer Documentation
- API Reference
- Authentication Guides
- Pricing
- Webhooks
- MCP Information

---

### Research Agent

Reads the discovered documentation and extracts:

- Category
- Authentication
- API Type
- API Coverage
- Self-Service Availability
- MCP Support
- Buildability
- Main Blockers
- Supporting Evidence

---

### Verification Agent

Performs a second validation pass by:

- Reviewing extracted information
- Assigning confidence scores
- Suggesting corrections
- Improving reliability

---

### Analyzer

Aggregates verified data to generate:

- Authentication statistics
- API distribution
- Category distribution
- Buildability insights
- Common blockers
- Overall benchmark metrics

---

### Report Generator

Automatically generates a clean HTML case study containing:

- Executive Summary
- Research Matrix
- Benchmark Dashboard
- Verification Summary
- Architecture
- Workflow
- Key Insights

---

# ⚙️ Setup

## 1. Clone the repository

```bash
git clone https://github.com/Ch-saketh/Composio-ai-ops-pipeline.git

cd Composio-ai-ops-pipeline
```

---

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate

### macOS / Linux

```bash
source venv/bin/activate
```

### Windows

```bash
venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file.

Example:

```env
GEMINI_API_KEY=YOUR_API_KEY
```

---

## 5. Add Applications

Edit

```text
data/apps.csv
```

Each row should contain:

```csv
app,seed_url
Slack,https://slack.com
GitHub,https://docs.github.com/rest
Stripe,https://stripe.com/docs/api
```

---

## 6. Run the pipeline

```bash
python src/main.py
```

---

## 📄 Output

The pipeline automatically generates:

```text
data/processed/
```

Verified JSON for every processed application.

and

```text
output/report.html
```

Interactive HTML Case Study.

---

## 📊 Research Workflow

```text
Load CSV
      │
      ▼
Discover Documentation
      │
      ▼
Research Official Sources
      │
      ▼
Generate Structured JSON
      │
      ▼
Verify Results
      │
      ▼
Analyze Dataset
      │
      ▼
Generate HTML Report
```

---

## 📝 Implementation Note

This repository demonstrates the complete research workflow using a representative sample of SaaS applications.

The architecture is designed to process all applications listed in `data/apps.csv`.

During development, Google Gemini free-tier API rate limits limited the number of live requests that could be executed. Providing a valid API key and rerunning the pipeline automatically continues processing and regenerates the final report.

---

## 🚀 Future Improvements

- OpenRouter Support
- Local LLM (Ollama)
- Browser Automation
- Parallel Processing
- Retry Queue
- Caching
- RAG-based Documentation Retrieval
- Multi-model Verification

---

## 🛠️ Tech Stack

- Python
- Google Gemini
- HTML
- CSS
- JavaScript
- Chart.js
- Mermaid
- JSON
- CSV

---

## 📧 Contact

**Saketh Chokkapu**

Portfolio: https://saketh-chokkapu-portfolio.vercel.app

LinkedIn: https://www.linkedin.com/in/saketh-chokkapu-3a668a2b9/

GitHub: https://github.com/Ch-saketh

---

## 📄 License

This repository was developed as part of the **Composio AI Product Operations Intern Take-Home Assignment**.
