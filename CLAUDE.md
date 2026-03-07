# AITA - AI Teaching Assistant for CEGE 3201

## Project Overview

Build a web-based AI Teaching Assistant chatbot for **CEGE 3201: Transportation Engineering** at the University of Minnesota.

- Interactive chatbot UI (like ChatGPT/Claude/Gemini)
- User authentication (Google Auth with UMN account)
- RAG-based answers grounded in course materials
- **Pedagogical principle: NEVER give direct answers. Guide students' learning through hints, Socratic questioning, and conceptual explanations.**

Reference implementation: https://github.com/sean0042/VTA (ACL 2025, Streamlit + FAISS + LangChain + OpenAI)

---

## Course Information

- **Course:** CEGE 3201: Transportation Engineering (Spring 2026)
- **Instructor:** Michael Levin, PhD, PE (mlevin@umn.edu)
- **TA:** Simanta Barman (PhD), Tony Smyrnov (UG)
- **Schedule:** T/Th 1:00-1:50pm, 216 Pillsbury Drive 110
- **Textbook:** *Principles of Highway Engineering and Traffic Analysis*, 7th ed., by Mannering, Kilareski, and Washburn
- **Grading:** HW 30%, Lab 15%, Midterm 1 15%, Midterm 2 15%, Final 25%
- **Prerequisites:** PHYS 1301, CEGE 3101, CEGE 3102

---

## Week-Aware Pedagogy

If a student asks about a topic that has NOT been covered yet according to the class schedule, the assistant should:
- Acknowledge the topic exists and will be covered later in the course
- Give a brief, high-level overview (1-2 sentences) so the student has context
- Do NOT go into detail, formulas, or worked examples for future topics
- Redirect the student to focus on the current week's material

### Course Schedule (Week-to-Topic Mapping)

| Week | Lectures (Tue + Thu) | Topics Covered |
|------|----------------------|----------------|
| 1 | | Orientation, Four-step model overview |
| 2 | | Land use, Trip generation |
| 3 | | Trip distribution, Mode choice |
| 4 | | Traffic assignment, Shortest path |
| 5 | | Traffic network analysis, Dynamic traffic assignment |
| 6 | | Project evaluation, Transit demand |
| 7 | | Transit planning, Transit operations |
| 8 | | Midterm 1 review, Midterm 1 |
| 9 | | Queueing theory, Traffic flow theory |
| 10 | | Traffic flow theory, Capacity and level of service |
| 11 | | Capacity and level of service, Traffic signal hardware |
| 12 | | Signal timing, Signal coordination and actuation |
| 13 | | Highway geometric design |
| 14 | | Emerging technologies |
| 15 | | Final exam review |

### Homework Schedule

| HW | Week Due | Topics |
|----|----------|--------|
| HW0 | 1 | Knowledge survey |
| HW1 | 3 | Trip generation |
| HW2 | 4 | Trip distribution |
| HW3 | 5 | Mode choice / traffic assignment |
| HW4 | 6 | Traffic network analysis |
| HW5 | 8 | Traffic assignment / transit |
| HW6 | 9 | Stopping sight distance / traffic flow |
| HW7 | 10 | Traffic flow theory |
| HW8 | 11 | Queueing theory |
| HW9 | 13 | Capacity / LOS |
| HW10 | 14 | Traffic signals |
| HW11 | 15 | Geometric design |

### Testing: Week Selector

For testing purposes, the sidebar includes a week selector (1-15) that controls which week the assistant treats as "current." Topics from later weeks trigger the "we'll cover that later" response. In production, this should be replaced with automatic date-based week calculation.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Frontend (Streamlit)               │
│  ┌──────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │  Login /  │  │  Chat UI     │  │  Admin Panel  │  │
│  │  Google   │  │  (multi-turn │  │  (upload docs │  │
│  │  Auth     │  │   dialogue)  │  │   manage DB)  │  │
│  └──────────┘  └──────────────┘  └───────────────┘  │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│              Backend (OpenAI + FAISS)                 │
│  ┌──────────────────────────────────────────────┐    │
│  │  Conversational RAG Pipeline                  │    │
│  │  1. FAISS vector retrieval (top-k docs)       │    │
│  │  2. Week-filtered context                     │    │
│  │  3. LLM response with pedagogical guardrails  │    │
│  └──────────────────────────────────────────────┘    │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│              Data Layer                              │
│  ┌─────────────┐  ┌────────────┐  ┌──────────────┐  │
│  │ FAISS Vector │  │ Interaction│  │ Course Docs  │  │
│  │ Store        │  │ Logs       │  │ (PDFs, .tex) │  │
│  │ (embeddings) │  │ (SQLite)   │  │              │  │
│  └─────────────┘  └────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Component            | Technology                          |
|----------------------|-------------------------------------|
| Language             | Python 3.11+                        |
| Web Framework        | Streamlit                           |
| LLM                  | OpenAI API (GPT-4o-mini)            |
| Embeddings           | OpenAI text-embedding-3-large       |
| Vector Store         | FAISS                               |
| Authentication       | Google OAuth (UMN @umn.edu)         |
| Document Processing  | PDFMiner, custom chunking           |
| Logging/Analytics    | SQLite                              |
| Deployment           | Docker + Nginx                      |

---

## Course Materials Available

Located in `course_materials/`:
- **Slides (1)/Slides/**: 14 topic directories with LaTeX source (content.tex), compiled slides, and handout PDFs
  - 1 Orientation, 2 Trip generation, 3 Trip distribution, 4 Mode choice, 5 Shortest path, 6 Traffic assignment, 7 Four-step planning, 7 Public transit, 8 Stopping sight distance, 9 Traffic flow theory, 10 Queueing theory, 11 Capacity LOS, 12 Traffic signals, 13 Geometric design, 14 Pavement engineering
- **Homework handouts (1)/Homework handouts/**: HW0-HW11 (with solutions), Lab 1-Lab 4
- **Homeworks/**: LaTeX source for homework assignments
- **syllabus/**: Course syllabus (PDF + LaTeX)

---

## File Structure

```
AITA_3201/
├── CLAUDE.md                  # This file - project plan & instructions
├── .env                       # API keys (not committed)
├── .gitignore
├── requirements.txt
├── main.py                    # Streamlit app entry point (login + chat + admin routing)
├── rag.py                     # RAG pipeline (FAISS retrieval + OpenAI LLM)
├── add_document.py            # Document ingestion pipeline
├── config.py                  # Centralized configuration (schedule, topics, paths)
├── db.py                      # SQLite database (interactions, feedback, feature requests)
├── admin.py                   # Admin dashboard
├── utils.py                   # Helper utilities
├── Dockerfile
├── docker-compose.yml
├── nginx/                     # Nginx reverse proxy config
├── faiss_db/                  # FAISS vector store (not committed)
│   ├── index.faiss
│   └── metadata.pkl
├── course_materials/          # Source course documents
│   ├── Slides (1)/Slides/     # Slide topic directories with content.tex + Handout.pdf
│   ├── Homework handouts (1)/ # HW PDFs (questions + solutions)
│   ├── Homeworks/             # LaTeX source for HWs
│   └── syllabus/              # Syllabus PDF + LaTeX
├── docs/                      # Processed document records
│   └── doc.jsonl
└── backup/                    # Vector store backups
```

---

## Key Design Decisions

1. **No homework solutions in vector store** - Prevents the chatbot from regurgitating answers. Solutions are skipped during ingestion.

2. **Pedagogical guardrails in system prompt** - The system prompt is the primary mechanism to ensure the bot guides learning rather than giving answers.

3. **Week-aware filtering** - RAG retrieval filters chunks by week so future topics aren't shown. System prompt also instructs the LLM to redirect future-topic questions.

4. **No LangChain** - Direct OpenAI + FAISS for simplicity and control.

5. **Handouts inside slide directories** - Unlike CEGE 3102 which had a separate Handouts folder, CEGE 3201 stores handout PDFs inside each slide topic directory.

# currentDate
Today's date is 2026-03-06.
