import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import quiz

# --------------------------
# Configuração global de logging
# --------------------------
logging.basicConfig(
    level=logging.DEBUG,  # DEBUG para ver tudo no console
    format="%(asctime)s - [%(levelname)s] - %(name)s - %(message)s"
)

# --------------------------
# Inicialização da aplicação
# --------------------------
app = FastAPI(
    title="QuizAI API",
    description="API para gerar quizzes usando o Gemini LLM.",
    version="1.0.0",
)

# --------------------------
# Configuração de CORS
# --------------------------
origins = [
    "http://localhost:3000",  # React dev server
    "http://127.0.0.1:3000",
    # Adicione aqui o domínio do frontend em produção, ex:
    # "https://meuquiz.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,         # quem pode acessar
    allow_credentials=True,
    allow_methods=["*"],           # libera todos os métodos (GET, POST, etc.)
    allow_headers=["*"],           # libera todos os headers
)


# --------------------------
# Registro das rotas
# --------------------------
app.include_router(quiz.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "QuizAI API is running 🚀"}
