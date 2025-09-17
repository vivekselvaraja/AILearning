import streamlit as st

# -----------------------------
# Prompt Engineering Questions
# -----------------------------
questions = [
    {
        "question": "What does Prompt Engineering refer to?",
        "options": [
            "A method for training neural networks",
            "A technique for generating content",
            "A process of designing and crafting input prompts to optimize the output of AI models",
            "A method for evaluating AI models"
        ],
        "answer": "A process of designing and crafting input prompts to optimize the output of AI models"
    },
    {
        "question": "Why is prompt engineering important in AI?",
        "options": [
            "It helps reduce model size",
            "It improves the quality and relevance of model outputs",
            "It increases training speed",
            "It eliminates the need for datasets"
        ],
        "answer": "It improves the quality and relevance of model outputs"
    },
    {
        "question": "Which strategy best reduces hallucinations in LLM outputs?",
        "options": [
            "Use creative prompts with open-ended phrasing",
            "Provide realistic constraints and context",
            "Ignore rare user inputs",
            "Increase temperature parameter"
        ],
        "answer": "Provide realistic constraints and context"
    },
    {
        "question": "What does 'few-shot prompting' involve?",
        "options": [
            "Training the model with millions of examples",
            "Providing a single example and expecting generalization",
            "Giving a few examples to guide the model's behavior",
            "Using reinforcement learning with feedback loops"
        ],
        "answer": "Giving a few examples to guide the model's behavior"
    },
    {
        "question": "How can you shorten LLM responses without losing quality?",
        "options": [
            "Increase batch size during inference",
            "Use more vague prompts",
            "Set a max token limit and use specific prompts",
            "Reduce model attention span"
        ],
        "answer": "Set a max token limit and use specific prompts"
    },
    {
        "question": "What is 'bias amplification' in AI systems?",
        "options": [
            "Underperformance due to noisy data",
            "Overfitting training data",
            "Exaggeration of existing biases in outputs",
            "Improved accuracy through repetition"
        ],
        "answer": "Exaggeration of existing biases in outputs"
    },
    {
        "question": "Which method improves prompt relevance and clarity?",
        "options": [
            "Iteratively refine based on model output",
            "Increase training epochs",
            "Add random tokens to diversify output",
            "Use vague instructions"
        ],
        "answer": "Iteratively refine based on model output"
    },
    {
        "question": "What is chain-of-thought prompting?",
        "options": [
            "A way to chain multiple models together",
            "A method to generate step-by-step reasoning",
            "A technique for compressing prompts",
            "A way to randomize model outputs"
        ],
        "answer": "A method to generate step-by-step reasoning"
    },
    {
        "question": "Which prompt style is best for classification tasks?",
        "options": [
            "Open-ended narrative prompts",
            "Multiple-choice format with clear labels",
            "Creative writing prompts",
            "Conversational prompts"
        ],
        "answer": "Multiple-choice format with clear labels"
    },
    {
        "question": "What does temperature control in LLMs affect?",
        "options": [
            "Model size",
            "Output randomness",
            "Training speed",
            "Token limit"
        ],
        "answer": "Output randomness"
    },
    {
        "question": "Which of the following is a benefit of zero-shot prompting?",
        "options": [
            "Requires labeled data",
            "Works without examples",
            "Needs fine-tuning",
            "Reduces inference time"
        ],
        "answer": "Works without examples"
    },
    {
        "question": "How can developers ensure generative AI avoids spreading misinformation?",
        "options": [
            "Using current and reliable sources",
            "Encouraging creativity over accuracy",
            "Reducing model size",
            "Using vague prompts"
        ],
        "answer": "Using current and reliable sources"
    },
    {
        "question": "What is the role of context in prompt engineering?",
        "options": [
            "It limits model creativity",
            "It helps guide the model toward relevant outputs",
            "It increases training time",
            "It reduces token usage"
        ],
        "answer": "It helps guide the model toward relevant outputs"
    },
    {
        "question": "Which prompt format is most effective for multilingual tasks?",
        "options": [
            "Monolingual prompts only",
            "Prompts with translation examples",
            "Prompts with emojis",
            "Prompts with random tokens"
        ],
        "answer": "Prompts with translation examples"
    },
    {
        "question": "What is the main goal of prompt tuning?",
        "options": [
            "To train a new model",
            "To adjust model architecture",
            "To optimize prompt inputs for better performance",
            "To reduce dataset size"
        ],
        "answer": "To optimize prompt inputs for better performance"
    }
]

# -----------------------------
# Session State Initialization
# -----------------------------
if "score" not in st.session_state:
    st.session_state.score = 0
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "feedback" not in st.session_state:
    st.session_state.feedback = []

# -----------------------------
# Feedback Generator
# -----------------------------
def get_feedback(is_correct):
    import random
    if is_correct:
        return random.choice(["✅ Good job!", "🎯 Impressive!", "👏 Well done!", "🔥 You're on fire!"])
    else:
        return random.choice(["❌ Oops! Wrong answer.", "😬 Great attempt, but practice more.", "🤔 Not quite right.", "📚 Keep learning!"])

# -----------------------------
# Quiz Logic
# -----------------------------
def next_question(selected_option):
    q = questions[st.session_state.current_q]
    is_correct = selected_option == q["answer"]
    if is_correct:
        st.session_state.score += 1
    st.session_state.answers.append(selected_option)
    st.session_state.feedback.append(get_feedback(is_correct))
    st.session_state.current_q += 1

def skip_question():
    st.session_state.answers.append("Skipped")
    st.session_state.feedback.append("⏭️ Skipped")
    st.session_state.current_q += 1

# -----------------------------
# UI Rendering
# -----------------------------
st.title("🧠 Prompt Engineering Quiz")
st.write("Test your knowledge of prompt engineering. Get instant feedback and a detailed review at the end!")

if st.session_state.current_q < len(questions):
    q = questions[st.session_state.current_q]
    st.subheader(f"Question {st.session_state.current_q + 1}")
    selected = st.radio(q["question"], q["options"], key=st.session_state.current_q)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit"):
            next_question(selected)
    with col2:
        if st.button("Skip"):
            skip_question()
else:
    st.success("🎉 Quiz Completed!")
    st.write(f"✅ Final Score: {st.session_state.score} / {len(questions)}")

    st.subheader("📋 Detailed Review")
    for i, q in enumerate(questions):
        st.markdown(f"**Q{i+1}: {q['question']}**")
        st.write(f"Your answer: `{st.session_state.answers[i]}`")
        st.write(f"Correct answer: `{q['answer']}`")
        st.write(st.session_state.feedback[i])
        st.markdown("---")

    if st.button("Restart Quiz"):
        st.session_state.score = 0
        st.session_state.current_q = 0
        st.session_state.answers = []
        st.session_state.feedback = []