# QuizAI API

QuizAI é uma API FastAPI para gerar quizzes utilizando a API Gemini LLM. A API permite que você envie um tema e uma dificuldade, e receba um quiz com alternativas e a resposta correta.

## Funcionalidades
- Gere quizzes informando um tema e dificuldade
- Retorna uma pergunta, alternativas e a resposta correta
- Documentação OpenAPI/Swagger bem estruturada para fácil teste

## Como começar

### 1. Instale as dependências
Certifique-se de ter o FastAPI e o Uvicorn instalados. Se estiver usando um ambiente virtual, ative-o primeiro.

```
pip install fastapi uvicorn
```

### 2. Execute a API
A partir da raiz do projeto:

```
uvicorn main:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

### 3. Documentação da API
Acesse `http://127.0.0.1:8000/docs` para a interface interativa do Swagger UI.

## Uso da API

### POST `/generate-quiz`
Gera um quiz baseado em um tema e dificuldade.

#### Corpo da Requisição
```
{
  "topic": "string",        // O tema do quiz
  "difficulty": "string"    // Dificuldade: easy, medium ou hard
}
```

#### Resposta
```
{
  "question": "string",
  "alternatives": [
    { "text": "string" },
    ...
  ],
  "correct_answer": "string"
}
```

#### Exemplo
Requisição:
```
{
  "topic": "Programação em Python",
  "difficulty": "easy"
}
```

Resposta:
```
{
  "question": "Qual é um fato importante sobre Programação em Python?",
  "alternatives": [
    { "text": "Alternativa 1" },
    { "text": "Alternativa 2" },
    { "text": "Alternativa 3" },
    { "text": "Alternativa 4" }
  ],
  "correct_answer": "Alternativa 2"
}
```

## Integração com Gemini LLM
- A implementação atual já utiliza a Gemini para gerar quizzes.
- Certifique-se de definir a variável de ambiente `GEMINI_API_KEY` com sua chave Gemini.
- A resposta segue o modelo `QuizResponse`.

## Licença
MIT
