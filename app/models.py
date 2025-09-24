from typing import List
from pydantic import BaseModel, Field, conint

class QuizRequest(BaseModel):
    topic: str = Field(..., description="O tema do quiz.")
    difficulty: str = Field(
        ...,
        description="Nível de dificuldade (easy, medium, hard).",
        examples=["easy", "medium", "hard"],
    )
    num_questions: int = Field(
        default=3,
        description="Quantidade de questões (mínimo 3, máximo 12).",
        ge=3,
        le=12,
    )

class QuizAlternative(BaseModel):
    text: str

class QuizItem(BaseModel):
    question: str
    alternatives: List[QuizAlternative]
    correct_answer: str

class QuizResponse(BaseModel):
    quizzes: List[QuizItem]
