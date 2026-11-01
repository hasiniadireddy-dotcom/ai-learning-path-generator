
import streamlit as st
from io import BytesIO
from reportlab.pdfgen import canvas

st.set_page_config(page_title="AI Learning Path Generator", page_icon="🎓")

st.title("🎓 AI Learning Path Generator")
st.write("Create a personalized learning roadmap and track your progress.")

# Student details
st.header("1. Student Details")

name = st.text_input("Enter your name")
subject = st.selectbox(
    "Choose your subject",
    ["Python", "Java", "HTML", "Data Science"]
)
level = st.selectbox(
    "Choose your level",
    ["Beginner", "Intermediate", "Advanced"]
)
days = st.number_input("Number of learning days", 1, 90, 7)
goal = st.text_input("Your learning goal")

# Topic library
topics = {
    "Python": {
        "Beginner": ["Introduction to Python", "Variables", "Data Types", "Operators", "Conditional Statements", "Loops", "Functions"],
        "Intermediate": ["Lists", "Tuples", "Dictionaries", "File Handling", "Exception Handling", "Modules", "OOP"],
        "Advanced": ["Decorators", "Generators", "Advanced OOP", "Multithreading", "Libraries", "Projects"]
    },
    "Java": {
        "Beginner": ["Introduction to Java", "Variables", "Data Types", "Operators", "Conditions", "Loops", "Methods"],
        "Intermediate": ["Arrays", "Strings", "Classes", "Inheritance", "Polymorphism", "Exception Handling"],
        "Advanced": ["Collections", "Multithreading", "Generics", "JDBC", "Advanced Projects"]
    },
    "HTML": {
        "Beginner": ["Introduction to HTML", "Basic Tags", "Headings", "Paragraphs", "Links", "Images", "Tables"],
        "Intermediate": ["Forms", "Input Types", "Semantic HTML", "Audio and Video", "Iframes"],
        "Advanced": ["Accessibility", "SEO Basics", "Advanced Forms", "Responsive Design", "Projects"]
    },
    "Data Science": {
        "Beginner": ["Introduction to Data Science", "Python Basics", "NumPy", "Pandas", "Data Visualization"],
        "Intermediate": ["Data Cleaning", "Statistics", "Data Analysis", "Exploratory Data Analysis"],
        "Advanced": ["Machine Learning", "Model Evaluation", "Feature Engineering", "Projects"]
    }
}

# Generate roadmap
st.header("2. Learning Roadmap")

if st.button("Generate Learning Path"):
    selected_topics = topics[subject][level]
    st.session_state.roadmap = selected_topics
    st.session_state.completed = []

    st.subheader(f"Your {subject} Roadmap")
    st.write(f"Student: {name if name else 'Student'}")
    st.write(f"Goal: {goal if goal else 'Improve my skills'}")
    st.write(f"Duration: {days} days")

    for i, topic in enumerate(selected_topics):
        st.write(f"Day {i + 1}: {topic}")

# Progress tracker
st.header("3. Progress Tracker")

if "roadmap" in st.session_state:
    completed = []
    for topic in st.session_state.roadmap:
        if st.checkbox(topic, key="progress_" + topic):
            completed.append(topic)

    st.session_state.completed = completed
    total = len(st.session_state.roadmap)
    done = len(completed)

    st.progress(done / total)
    st.write(f"Completed: {done}/{total} topics")

else:
    st.info("Generate your learning path first to track progress.")

# Learning resources
st.header("4. Learning Resources")

resources = {
    "Python": "https://www.python.org/about/gettingstarted/",
    "Java": "https://dev.java/learn/",
    "HTML": "https://developer.mozilla.org/en-US/docs/Learn_web_development",
    "Data Science": "https://www.kaggle.com/learn"
}

st.write("Recommended learning resource:")
st.link_button("Open Learning Resource", resources[subject])

# Quiz
st.header("5. Knowledge Assessment")

questions = [
    ("Which language is commonly used for Data Science?", ["Python", "HTML", "CSS"], "Python"),
    ("Which keyword defines a function in Python?", ["class", "def", "loop"], "def"),
    ("Which language is used to structure web pages?", ["Java", "HTML", "Python"], "HTML"),
    ("Which keyword creates an object in Java?", ["new", "make", "create"], "new"),
    ("Which library is commonly used for data analysis in Python?", ["Pandas", "HTML", "CSS"], "Pandas")
]

answers = []
for i, (question, options, correct) in enumerate(questions):
    st.write(f"**Q{i + 1}. {question}**")
    answer = st.radio(
        "Choose your answer",
        options,
        key=f"quiz_{i}"
    )
    answers.append(answer)

if st.button("Submit Quiz"):
    score = sum(
        answers[i] == questions[i][2]
        for i in range(len(questions))
    )
    st.session_state.score = score
    st.success(f"Your score: {score}/5")

# Performance dashboard
st.header("6. Student Performance Dashboard")

if "score" in st.session_state:
    score = st.session_state.score
    percentage = score * 20

    st.write(f"Student: {name if name else 'Student'}")
    st.write(f"Subject: {subject}")
    st.write(f"Level: {level}")
    st.metric("Quiz Score", f"{score}/5")
    st.metric("Performance", f"{percentage}%")

    if score == 5:
        st.success("Excellent! You can move to the next level.")
    elif score >= 3:
        st.info("Good work! Revise the topics you missed.")
    else:
        st.warning("Keep practising the basics.")

else:
    st.info("Submit the quiz to view your performance.")

# PDF download
st.header("7. Download Learning Report")

if "roadmap" in st.session_state:
    if st.button("Prepare PDF Report"):
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)

        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, 800, "AI Learning Path Generator Report")

        pdf.setFont("Helvetica", 11)
        pdf.drawString(50, 770, f"Student: {name if name else 'Student'}")
        pdf.drawString(50, 750, f"Subject: {subject}")
        pdf.drawString(50, 730, f"Level: {level}")
        pdf.drawString(50, 710, f"Duration: {days} days")

        y = 675
        pdf.drawString(50, y, "Learning Topics:")
        y -= 25

        for topic in st.session_state.roadmap:
            if y < 60:
                pdf.showPage()
                y = 800
            status = "Completed" if topic in st.session_state.get("completed", []) else "Pending"
            pdf.drawString(50, y, f"- {topic} ({status})")
            y -= 20

        if "score" in st.session_state:
            pdf.drawString(50, y - 10, f"Quiz Score: {st.session_state.score}/5")

        pdf.save()
        buffer.seek(0)

        st.download_button(
            "Download PDF",
            data=buffer,
            file_name="learning_report.pdf",
            mime="application/pdf"
        )

st.divider()
st.caption("Academic project prototype using rule-based recommendations.")
  
