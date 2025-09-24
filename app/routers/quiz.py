import logging
from fastapi import APIRouter, HTTPException
from app.models import QuizRequest, QuizResponse, QuizItem, QuizAlternative
from app.services.gemini import call_gemini_llm

router = APIRouter(prefix="/quiz", tags=["Quiz"])
logger = logging.getLogger(__name__)

@router.post(
    "/generate",
    response_model=QuizResponse,
    summary="Gerar um quiz com múltiplas questões usando o Gemini LLM",
)
async def generate_quiz(request: QuizRequest):
    """
    Gera múltiplas questões de quiz baseado no tema, dificuldade e quantidade informados.
    """
    if not request.topic.strip() or not request.difficulty.strip():
        raise HTTPException(status_code=400, detail="Tema e dificuldade são obrigatórios.")

    try:
        logger.info(f"📥 Requisição recebida: {request.dict()}")
        quizzes = await call_gemini_llm(request.topic, request.difficulty, request.num_questions)

        response = QuizResponse(
            quizzes=[
                QuizItem(
                    question=q["question"],
                    alternatives=[QuizAlternative(text=alt) for alt in q["alternatives"]],
                    correct_answer=q["correct_answer"],
                )
                for q in quizzes
            ]
        )
        logger.info("✅ Quiz completo enviado ao cliente.")
        return response

    except Exception as e:
        logger.exception("❌ Erro inesperado ao gerar quiz")
        raise HTTPException(status_code=500, detail=f"Erro na API Gemini: {e}")
