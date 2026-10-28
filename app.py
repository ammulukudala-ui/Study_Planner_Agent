
import streamlit as st
from datetime import date, timedelta

st.set_page_config(page_title="Study Planner Agent", page_icon="📚")

st.title("📚 Study Planner Agent")
st.write("Create your exam study plan and track your progress.")

if "subjects" not in st.session_state:
    st.session_state.subjects = []

st.subheader("Add a Subject")

with st.form("subject_form"):
    subject = st.text_input("Subject name")
    exam_date = st.date_input(
        "Exam date",
        value=date.today() + timedelta(days=7),
        min_value=date.today()
    )
    topics_text = st.text_area(
        "Topics (enter one topic per line)"
    )
    daily_hours = st.number_input(
        "Daily study hours",
        min_value=1,
        max_value=12,
        value=2
    )
    submitted = st.form_submit_button("Create Study Plan")

if submitted:
    topics = [
        topic.strip()
        for topic in topics_text.splitlines()
        if topic.strip()
    ]

    if not subject.strip() or not topics:
        st.error("Enter a subject name and at least one topic.")
    else:
        st.session_state.subjects.append({
            "name": subject.strip(),
            "exam": exam_date,
            "topics": topics,
            "hours": daily_hours,
            "completed": []
        })
        st.success("Study plan created!")

st.divider()
st.subheader("Your Study Plans")

if not st.session_state.subjects:
    st.info("Add your first subject to get started.")
else:
    for index, item in enumerate(st.session_state.subjects):
        with st.expander(item["name"], expanded=True):
            st.write("Exam date:", item["exam"])
            st.write("Daily study target:", item["hours"], "hours")

            for topic_index, topic in enumerate(item["topics"]):
                key = f"topic_{index}_{topic_index}"
                checked = topic in item["completed"]

                new_checked = st.checkbox(
                    topic,
                    value=checked,
                    key=key
                )

                if new_checked and not checked:
                    item["completed"].append(topic)
                elif not new_checked and checked:
                    item["completed"].remove(topic)

            total = len(item["topics"])
            done = len(item["completed"])
            progress = done / total

            st.progress(progress)
            st.write(f"Progress: {done}/{total} topics completed")

            remaining_days = (item["exam"] - date.today()).days
            remaining_topics = [
                t for t in item["topics"]
                if t not in item["completed"]
            ]

            if remaining_topics:
                if remaining_days > 0:
                    st.write("### Suggested study schedule")
                    for day_index, topic in enumerate(remaining_topics):
                        study_day = date.today() + timedelta(
                            days=day_index % remaining_days
                        )
                        st.write(f"- {study_day}: {topic}")
                else:
                    st.warning("Your exam is today. Prioritize remaining topics.")
            else:
                st.success("All topics completed! 🎉")
