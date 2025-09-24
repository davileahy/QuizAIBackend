# app/models.py
from typing import List, Dict
from pydantic import BaseModel, Field, conint

class QuizRequest(BaseModel):
    topic: str
    difficulty: str

    num_questions: int = Field(
    default=3,
    description="Quantidade de questões (mínimo 3, máximo 12).",
    ge=3,
    le=12,
)

class QuizAlternative(BaseModel):
    text: str

class QuizQuestion(BaseModel):
    id: int
    question: str
    alternatives: List[QuizAlternative]

class QuizResponse(BaseModel):
    quiz_id: str
    questions: List[QuizQuestion]

class AnswerRequest(BaseModel):
    quiz_id: str
    question_id: int
    selected_answer: str

class AnswerResponse(BaseModel):
    correct: bool

class QuizAnswersResponse(BaseModel):
    quiz_id: str
    correct_answers: Dict[int, str]  # {question_id: correct_answer}