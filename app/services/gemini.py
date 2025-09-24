import json
import logging
import httpx
import re
from app.config import GEMINI_API_KEY, GEMINI_API_URL

logger = logging.getLogger(__name__)

async def call_gemini_llm(topic: str, difficulty: str, num_questions: int) -> list:
    """
    Chama a API Gemini LLM para gerar múltiplas questões de quiz.
    """
    logger.info(f"➡️ Iniciando geração | Tema: {topic} | Dificuldade: {difficulty} | Questões: {num_questions}")

    prompt = (
        f"Gere {num_questions} perguntas de quiz de múltipla escolha sobre '{topic}', cada uma com 4 alternativas.\n"
        f"Dificuldade: {difficulty}.\n"
        f"Responda **APENAS** com um JSON válido no formato:\n"
        f'[{{"question": "...", "alternatives": ["...","...","...","..."], "correct_answer": "..."}}]'
    )
    logger.debug(f"📝 Prompt enviado ao Gemini:\n{prompt}")

    headers = {"Content-Type": "application/json"}
    params = {"key": GEMINI_API_KEY}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        async with httpx.AsyncClient() as client:
            logger.info("🌐 Enviando requisição para Gemini API...")
            response = await client.post(
                GEMINI_API_URL, headers=headers, params=params, json=data, timeout=60
            )
            logger.info(f"📡 Status da resposta Gemini: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            logger.debug(f"📩 Resposta JSON completa da Gemini:\n{result}")

        # Extrair o texto bruto
        text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        logger.info("✅ Texto bruto recebido da Gemini")
        logger.debug(f"📝 Texto bruto:\n{text}")

        if text.startswith("```"):
            text = re.sub(r"```(json)?", "", text).strip("` \n")
            logger.debug(f"🧹 Texto após limpeza de markdown:\n{text}")

        quizzes = json.loads(text)

        # Garantir que veio uma lista e que tem a quantidade certa
        if not isinstance(quizzes, list):
            raise ValueError("Resposta não é uma lista de questões.")
        if len(quizzes) != num_questions:
            raise ValueError(f"Esperado {num_questions} questões, mas recebi {len(quizzes)}.")

        logger.info(f"🎯 {len(quizzes)} questões parseadas com sucesso.")
        return quizzes

    except json.JSONDecodeError as e:
        logger.error(f"❌ Erro ao interpretar JSON | Texto bruto:\n{text}")
        raise ValueError(f"Falha ao interpretar JSON: {e}")
    except httpx.HTTPStatusError as http_err:
        logger.error(f"❌ Erro HTTP na Gemini API: {http_err}")
        raise
    except Exception as e:
        logger.exception("❌ Falha inesperada ao processar resposta da Gemini")
        raise ValueError(f"Falha ao processar resposta da Gemini: {e}")
