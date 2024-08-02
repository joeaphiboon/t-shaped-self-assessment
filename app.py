import streamlit as st
import pandas as pd
import random

def calculate_scores(answers, question_order):
    breadth_score = sum(answers[i] for i in question_order[:15])
    depth_score = sum(answers[i] for i in question_order[15:])
    return breadth_score, depth_score

def interpret_scores(breadth_score, depth_score):
    breadth_interpretation = (
        "Highly broad skill set; you excel in working across disciplines." if breadth_score >= 60 else
        "Strong breadth; you can effectively collaborate with various departments." if breadth_score >= 45 else
        "Moderate breadth; some areas for improvement in cross-disciplinary skills." if breadth_score >= 30 else
        "Limited breadth; focus on developing skills in different functional areas." if breadth_score >= 15 else
        "Minimal breadth; significant improvement needed in broadening skill set."
    )
    
    depth_interpretation = (
        "Highly specialized; you possess deep expertise in your field." if depth_score >= 48 else
        "Strong depth; you have significant expertise in your area." if depth_score >= 36 else
        "Moderate depth; you have a good foundation but can deepen your knowledge." if depth_score >= 24 else
        "Limited depth; focus on developing expertise in your field." if depth_score >= 12 else
        "Minimal depth; significant improvement needed in deepening your knowledge."
    )
    
    overall_profile = ""
    if breadth_score >= 60 and depth_score >= 48:
        overall_profile = "Excellent T-shaped profile"
    elif breadth_score >= 45 and depth_score >= 36:
        overall_profile = "Strong T-shaped profile"
    elif breadth_score >= 30 and depth_score >= 24:
        overall_profile = "Developing T-shaped profile"
    else:
        overall_profile = "Emerging T-shaped profile"

    suggestions = []
    if breadth_score < 45:
        suggestions.append("Work on expanding your interdisciplinary skills and knowledge.")
    if depth_score < 36:
        suggestions.append("Focus on deepening your expertise in your primary field.")
    if breadth_score >= 45 and depth_score >= 36:
        suggestions.append("Continue balancing the development of both broad and deep skills.")

    overall_interpretation = f"""
    Your T-shaped profile: {overall_profile}

    Breadth Score: {breadth_score}/75
    {breadth_interpretation}

    Depth Score: {depth_score}/60
    {depth_interpretation}

    Suggestions:
    {' '.join(f'- {s}' for s in suggestions)}

    Remember, a well-rounded T-shaped professional excels in both broad interdisciplinary skills and deep expertise in a specific area. Continue to develop both aspects of your profile for optimal career growth and versatility.
    """
    
    return breadth_interpretation, depth_interpretation, overall_interpretation

st.title("T-Shaped Self-Assessment")
st.write(":blue_heart: **by JTIAPBN.Ai**")

questions = [
    "I communicate effectively with people from different departments.",
    "I can collaborate with colleagues from various functional areas.",
    "I often help team members from other disciplines understand complex concepts.",
    "I am good at identifying problems across different areas of the business.",
    "I can apply different problem-solving techniques depending on the situation.",
    "I am comfortable using creative thinking to solve problems.",
    "I can easily adapt to new tools and technologies.",
    "I thrive in situations that require learning new skills quickly.",
    "I am open to change and can work effectively in different environments.",
    "I can manage projects that involve multiple disciplines.",
    "I am effective at prioritizing tasks and meeting deadlines.",
    "I can coordinate the efforts of team members from different departments.",
    "I frequently contribute new ideas and perspectives in team meetings.",
    "I seek out opportunities to innovate in my work.",
    "I can integrate ideas from various disciplines to develop innovative solutions.",
    "I have deep expertise in my primary field of work.",
    "I keep up-to-date with the latest trends and developments in my area of expertise.",
    "I can mentor others in my specific field.",
    "I am proficient in analyzing data relevant to my discipline.",
    "I use evidence-based approaches to make decisions in my work.",
    "I can develop detailed and effective solutions within my area of expertise.",
    "I have a thorough understanding of the specialized tools and methods used in my field.",
    "I regularly attend training and professional development sessions related to my expertise.",
    "I contribute specialized knowledge to projects and discussions.",
    "I am highly skilled in executing tasks within my area of expertise.",
    "I consistently deliver high-quality work in my field.",
    "I can independently handle complex tasks that require deep knowledge."
]

if 'page' not in st.session_state:
    st.session_state.page = 0

if 'answers' not in st.session_state:
    st.session_state.answers = [3] * len(questions)

if 'show_results' not in st.session_state:
    st.session_state.show_results = False

if 'question_order' not in st.session_state:
    st.session_state.question_order = list(range(len(questions)))
    random.shuffle(st.session_state.question_order)

def next_page():
    st.session_state.page += 1

def submit():
    st.session_state.show_results = True

def restart():
    st.session_state.page = 0
    st.session_state.answers = [3] * len(questions)
    st.session_state.show_results = False
    st.session_state.question_order = list(range(len(questions)))
    random.shuffle(st.session_state.question_order)

if not st.session_state.show_results:
    start = st.session_state.page * 5
    end = min(start + 5, len(questions))

    for i in range(start, end):
        q_index = st.session_state.question_order[i]
        st.write(f"Q{i+1}: {questions[q_index]}")
        st.session_state.answers[q_index] = st.radio(
            "Select your rating",
            options=["1 - Strongly Disagree", "2 - Disagree", "3 - Neutral", "4 - Agree", "5 - Strongly Agree"],
            index=2,  # Default to "3 - Neutral"
            key=f"q{i+1}",
            horizontal=True
        )
        st.session_state.answers[q_index] = int(st.session_state.answers[q_index][0])
        st.write("---")

    if st.session_state.page < len(questions) // 5:
        st.button("Next", on_click=next_page)
    else:
        st.button("Submit", on_click=submit)

else:
    breadth_score, depth_score = calculate_scores(st.session_state.answers, st.session_state.question_order)
    breadth_interpretation, depth_interpretation, overall_interpretation = interpret_scores(breadth_score, depth_score)
    
    results = pd.DataFrame({
        "Category": ["Breadth Score", "Depth Score"],
        "Score": [breadth_score, depth_score],
        "Max Score": [75, 60],
        "Interpretation": [breadth_interpretation, depth_interpretation]
    })
    
    st.subheader("Results")
    st.table(results)
    
    st.subheader("Overall T-Shaped Profile Analysis")
    st.write(overall_interpretation)

    st.button("Start Over", on_click=restart)

st.sidebar.markdown("""
### Instructions:
Rate yourself for each statement using the radio buttons:
1 = Strongly Disagree
2 = Disagree
3 = Neutral
4 = Agree
5 = Strongly Agree
""")
