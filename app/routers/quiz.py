# app/routers/quiz.py
import logging
import uuid
from fastapi import APIRouter, HTTPException
from app.models import QuizRequest, QuizResponse, QuizQuestion, QuizAlternative, AnswerRequest, AnswerResponse, QuizAnswersResponse
from app.services.gemini import call_gemini_llm
from app.storage import QUIZ_STORAGE

router = APIRouter(prefix="/quiz", tags=["Quiz"])
logger = logging.getLogger(__name__)

@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(request: QuizRequest):
    try:
        logger.info(f"📥 Nova requisição de quiz: {request.dict()}")

        # Chama Gemini para gerar questões
        quizzes = await call_gemini_llm(request.topic, request.difficulty, request.num_questions)

        # Cria um ID único para esse quiz
        quiz_id = str(uuid.uuid4())
        QUIZ_STORAGE[quiz_id] = {}

        # Monta resposta SEM o gabarito
        response_questions = []
        for i, q in enumerate(quizzes, start=1):
            response_questions.append(
                QuizQuestion(
                    id=i,
                    question=q["question"],
                    alternatives=[QuizAlternative(text=alt) for alt in q["alternatives"]],
                )
            )
            # Armazena resposta correta apenas no backend
            QUIZ_STORAGE[quiz_id][i] = q["correct_answer"]

        logger.info(f"✅ Quiz {quiz_id} gerado e armazenado em memória")
        return QuizResponse(quiz_id=quiz_id, questions=response_questions)

    except Exception as e:
        logger.exception("❌ Erro inesperado ao gerar quiz")
        raise HTTPException(status_code=500, detail=f"Erro ao gerar quiz: {e}")
    
@router.post("/answer", response_model=AnswerResponse)
async def check_answer(request: AnswerRequest):
    """
    Verifica se a resposta escolhida está correta.
    """
    logger.info(f"📝 Verificando resposta do quiz {request.quiz_id} | Questão {request.question_id}")

    if request.quiz_id not in QUIZ_STORAGE:
        raise HTTPException(status_code=404, detail="Quiz não encontrado")

    answers = QUIZ_STORAGE[request.quiz_id]
    if request.question_id not in answers:
        raise HTTPException(status_code=404, detail="Questão não encontrada")

    correct_answer = answers[request.question_id]
    is_correct = (request.selected_answer == correct_answer)

    logger.info(f"Resultado: {'✔️ Correto' if is_correct else '❌ Incorreto'}")
    return AnswerResponse(correct=is_correct)


@router.get("/answers/{quiz_id}", response_model=QuizAnswersResponse)
async def get_all_answers(quiz_id: str):
    """
    Retorna todas as respostas corretas de um quiz específico.
    Útil para exibir o gabarito ao final do quiz.
    """
    logger.info(f"📖 Requisitando gabarito completo do quiz {quiz_id}")

    if quiz_id not in QUIZ_STORAGE:
        raise HTTPException(status_code=404, detail="Quiz não encontrado")

    answers = QUIZ_STORAGE[quiz_id]
    logger.debug(f"✅ Gabarito recuperado: {answers}")

    return QuizAnswersResponse(quiz_id=quiz_id, correct_answers=answers)