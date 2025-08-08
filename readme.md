# 📝 AI-Powered Todo List (Full Stack)

A **full-stack Todo List application** with:
- **FastAPI** backend (Python) for task & subtask management
- **SQLAlchemy 2.0** ORM for database models
- **SQLite** database (easily replaceable)
- **OpenAI GPT** integration to auto-generate subtasks
- **React + TypeScript** frontend

---

## 📂 Project Structure

```plaintext
todolist/
├── backend/                   # FastAPI backend
│   ├── AI.py                   # OpenAI subtask generation logic
│   ├── database.py             # SQLAlchemy engine & session setup
│   ├── main.py                 # FastAPI routes & app entry point
│   ├── models.py               # SQLAlchemy models (Todo, Subtask)
│   ├── schemas.py              # Pydantic schemas
│   └── database.db             # SQLite database file
│
├── frontend/                   # React + TypeScript frontend
│   └── my-react-app/
│       ├── public/             # Static assets
│       ├── src/                # Application source
│       │   ├── assets/         
│       │   ├── AddToDo.tsx     # Component to add todos
│       │   ├── ToDo.tsx        # Component to display todos
│       │   ├── App.tsx         # Main app component
│       │   ├── App.css         # App styles
│       │   ├── index.css       # Global styles
│       │   ├── main.tsx        # React entry point
│       │   └── utils.ts        # Utility functions
│       └── package.json        # Frontend dependencies & scripts

```

---

## ⚙️ Requirements

- **Backend**
  - Python 3.10+
  - [pip](https://pip.pypa.io/en/stable/)
  - [OpenAI API key](https://platform.openai.com/)
- **Frontend**
  - Node.js 18+
  - npm or yarn

---

## 📦 Backend Setup

1. **Create and activate virtual environment**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate      # Mac/Linux
.venv\Scripts\activate         # Windows
```

2. **Create and activate virtual environment**
Install dependencies
```bash
pip install -r requirements.txt
```
3. Set OpenAI API key
```bash
export OPENAI_API_KEY="your_api_key_here"   # Mac/Linux
setx OPENAI_API_KEY "your_api_key_here"     # Windows
```
4. Run Backend
```bash
cd backend
uvicorn main:app --reload
```

Backend runs at:
➡ http://127.0.0.1:8000


## 🎨 Frontend Setup
Install dependencies

```bash
cd frontend/my-react-app
npm install
```

Run development server
```bash
npm run dev
```


Frontend runs at:
➡ http://localhost:5173

