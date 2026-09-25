from app.evaluation.schemas import EvaluationCase


EVALUATION_DATASET = [

    # -------------------------
    # SQL
    # -------------------------

    EvaluationCase(
        question="Which ad had the highest ROAS?",
        query_type="sql",
        expected_route="sql",
    ),

    EvaluationCase(
        question="Which ad had the lowest CPA?",
        query_type="sql",
        expected_route="sql",
    ),

    EvaluationCase(
        question="What is the average ROAS by marketing angle?",
        query_type="sql",
        expected_route="sql",
    ),

    EvaluationCase(
        question="Which Facebook ads had the highest ROAS?",
        query_type="sql",
        expected_route="sql",
    ),

    EvaluationCase(
        question="Which platform generated the most conversions?",
        query_type="sql",
        expected_route="sql",
    ),

    # -------------------------
    # Semantic
    # -------------------------

    EvaluationCase(
        question="Which ads use urgency messaging?",
        query_type="semantic",
        expected_route="vector",
    ),

    EvaluationCase(
        question="Find ads using premium messaging.",
        query_type="semantic",
        expected_route="vector",
    ),

    EvaluationCase(
        question="Which ads use discount-focused language?",
        query_type="semantic",
        expected_route="vector",
    ),

    EvaluationCase(
        question="Find ads with social proof messaging.",
        query_type="semantic",
        expected_route="vector",
    ),

    EvaluationCase(
        question="Which ads have an urgent tone?",
        query_type="semantic",
        expected_route="vector",
    ),

    # -------------------------
    # Hybrid
    # -------------------------

    EvaluationCase(
        question=(
            "Find high-performing Facebook ads "
            "that use urgency messaging."
        ),
        query_type="hybrid",
        expected_route="hybrid",
    ),

    EvaluationCase(
        question=(
            "Find Google ads with high ROAS "
            "that use discount messaging."
        ),
        query_type="hybrid",
        expected_route="hybrid",
    ),

    EvaluationCase(
        question=(
            "Which high-performing ads use premium positioning?"
        ),
        query_type="hybrid",
        expected_route="hybrid",
    ),

    EvaluationCase(
        question=(
            "Find Facebook ads with ROAS above 2 "
            "using urgency messaging."
        ),
        query_type="hybrid",
        expected_route="hybrid",
    ),

    EvaluationCase(
        question=(
            "Which high-performing ads use social proof "
            "and what characteristics do they share?"
        ),
        query_type="hybrid",
        expected_route="hybrid",
    ),
]