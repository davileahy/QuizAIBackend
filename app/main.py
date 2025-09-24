import logging
from fastapi import FastAPI
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
# Registro das rotas
# --------------------------
app.include_router(quiz.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "QuizAI API is running 🚀"}
