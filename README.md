
---

# 📘 QuizAI API

QuizAI é uma API construída em **FastAPI** que gera quizzes de múltipla escolha utilizando a **Gemini LLM**.
Ela foi projetada para **evitar trapaças**: o backend nunca expõe as respostas corretas diretamente ao frontend.

---

## 🚀 Funcionalidades

* Gera quizzes de múltiplas questões sobre qualquer tema e nível de dificuldade.
* Retorna apenas perguntas e alternativas, nunca a resposta correta.
* Permite verificar respostas uma a uma.
* Disponibiliza o **gabarito completo** somente ao final do quiz.
* Documentação automática via **Swagger** em `/docs`.

---

## 🛠️ Tecnologias

* [FastAPI](https://fastapi.tiangolo.com/)
* [httpx](https://www.python-httpx.org/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* Gemini LLM API (Google)

---

## 📂 Estrutura do projeto

```
quizai/
│── app/
│   ├── __init__.py
│   ├── main.py           # Ponto de entrada da aplicação
│   ├── config.py         # Configurações e variáveis de ambiente
│   ├── models.py         # Modelos Pydantic
│   ├── storage.py        # Armazenamento temporário dos gabaritos
│   ├── services/
│   │   └── gemini.py     # Chamada à API Gemini
│   └── routers/
│       └── quiz.py       # Rotas da API
│
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Configuração

### 1. Clonar o projeto

```bash
git clone https://github.com/seu-repo/quizai.git
cd quizai
```

### 2. Criar ambiente virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Definir variáveis de ambiente

Crie um arquivo `.env`:

```
GEMINI_API_KEY=sua_chave_aqui
```

### 5. Rodar a API

```bash
uvicorn app.main:app --reload
```

Acesse em:
👉 `http://127.0.0.1:8000/docs` (Swagger UI)
👉 `http://127.0.0.1:8000/redoc` (ReDoc)

---

## 🔌 Endpoints

### 1. **Gerar quiz**

`POST /quiz/generate`

Gera um quiz com múltiplas questões (mínimo 3, máximo 12).

#### Corpo da requisição

```json
{
  "topic": "Programação em Python",
  "difficulty": "medium",
  "num_questions": 5
}
```

#### Resposta

```json
{
  "quiz_id": "a4c3c5e0-b8d3-4f21-9d5c-34bb85c5d91f",
  "questions": [
    {
      "id": 1,
      "question": "Qual destas opções é uma estrutura de dados em Python?",
      "alternatives": [
        {"text": "Array"},
        {"text": "Tuple"},
        {"text": "Struct"},
        {"text": "Class"}
      ]
    }
  ]
}
```

⚠️ Não há `correct_answer` na resposta.

---

### 2. **Responder questão**

`POST /quiz/answer`

Verifica se a resposta do usuário está correta.

#### Corpo da requisição

```json
{
  "quiz_id": "a4c3c5e0-b8d3-4f21-9d5c-34bb85c5d91f",
  "question_id": 1,
  "selected_answer": "Tuple"
}
```

#### Resposta

```json
{
  "correct": true
}
```

---

### 3. **Gabarito completo**

`GET /quiz/answers/{quiz_id}`

Retorna todas as respostas corretas de um quiz específico (apenas no final).

#### Exemplo

```
GET /quiz/answers/a4c3c5e0-b8d3-4f21-9d5c-34bb85c5d91f
```

#### Resposta

```json
{
  "quiz_id": "a4c3c5e0-b8d3-4f21-9d5c-34bb85c5d91f",
  "correct_answers": {
    "1": "Tuple",
    "2": "List",
    "3": "Dictionary",
    "4": "Set",
    "5": "Class"
  }
}
```

---

## 🔒 Segurança

* O **gabarito nunca é enviado junto com as perguntas**.
* As respostas corretas ficam armazenadas apenas no backend (`QUIZ_STORAGE`).
* Somente no final do quiz o gabarito pode ser solicitado pelo cliente.

---

## ⚛️ Exemplo de fluxo em React

Um fluxo simples em React usando **fetch**:

```jsx
import React, { useState } from "react";

function QuizApp() {
  const [quiz, setQuiz] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [score, setScore] = useState(0);
  const [finished, setFinished] = useState(false);
  const [answers, setAnswers] = useState({});

  // 1. Gerar quiz
  const startQuiz = async () => {
    const res = await fetch("http://127.0.0.1:8000/quiz/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        topic: "Programação em Python",
        difficulty: "medium",
        num_questions: 3,
      }),
    });
    const data = await res.json();
    setQuiz(data);
    setCurrentQuestion(0);
    setScore(0);
    setFinished(false);
    setAnswers({});
  };

  // 2. Responder questão
  const answerQuestion = async (selected) => {
    const res = await fetch("http://127.0.0.1:8000/quiz/answer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        quiz_id: quiz.quiz_id,
        question_id: quiz.questions[currentQuestion].id,
        selected_answer: selected,
      }),
    });
    const data = await res.json();

    if (data.correct) {
      setScore((prev) => prev + 1);
    }
    setAnswers((prev) => ({
      ...prev,
      [quiz.questions[currentQuestion].id]: selected,
    }));

    if (currentQuestion + 1 < quiz.questions.length) {
      setCurrentQuestion((prev) => prev + 1);
    } else {
      setFinished(true);
    }
  };

  // 3. Buscar gabarito ao final
  const getResults = async () => {
    const res = await fetch(`http://127.0.0.1:8000/quiz/answers/${quiz.quiz_id}`);
    const data = await res.json();
    console.log("Gabarito:", data.correct_answers);
    alert(`Você acertou ${score} de ${quiz.questions.length}`);
  };

  if (!quiz) return <button onClick={startQuiz}>Iniciar Quiz</button>;

  if (finished)
    return (
      <div>
        <h2>Quiz finalizado!</h2>
        <p>Você acertou {score} de {quiz.questions.length}</p>
        <button onClick={getResults}>Ver gabarito</button>
      </div>
    );

  const q = quiz.questions[currentQuestion];

  return (
    <div>
      <h2>{q.question}</h2>
      {q.alternatives.map((alt, idx) => (
        <button key={idx} onClick={() => answerQuestion(alt.text)}>
          {alt.text}
        </button>
      ))}
    </div>
  );
}

export default QuizApp;
```

---

