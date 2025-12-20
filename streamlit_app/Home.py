import requests
import streamlit as st

API_BASE = "http://127.0.0.1:8000"


def fetch_score(target_role: str):
    res = requests.get(f"{API_BASE}/profile/score", params={"target_role": target_role})
    res.raise_for_status()
    return res.json()


def fetch_profile():
    res = requests.get(f"{API_BASE}/profile/current")
    res.raise_for_status()
    return res.json()



def fetch_roadmap():
    res = requests.get(f"{API_BASE}/roadmap/mock")
    res.raise_for_status()
    return res.json()


def fetch_jobs():
    res = requests.get(f"{API_BASE}/jobs/mock")
    res.raise_for_status()
    return res.json()


def fetch_interview_questions():
    res = requests.get(f"{API_BASE}/interview/mock_questions")
    res.raise_for_status()
    return res.json()


def main():
    st.set_page_config(page_title="CareerPilot", layout="wide")
    st.title("🚀 CareerPilot – Career Operating System")

    # Sidebar
    st.sidebar.header("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Roadmap", "Jobs", "Interview Prep", "Upload Resume"],
    )

    # ---------------- Dashboard ----------------
    if page == "Dashboard":
        profile = fetch_profile()

        st.subheader("Profile Overview")

        col_top1, col_top2 = st.columns([2, 1])

        with col_top1:
            st.write(f"**Name:** {profile['name']}")
            st.write(f"**Headline:** {profile['headline']}")
            # Let user choose / override target role
            target_role = st.selectbox(
                "Target role",
                options=["Data Scientist", "ML Engineer", "Backend Engineer"],
                index=0,
            )
            st.write(f"Current target: **{target_role}**")

        with col_top2:
            st.markdown("**Career Readiness Score**")
            score_data = fetch_score(target_role)
            score_value = score_data["score"]
            st.metric(
                "Score",
                f"{score_value} / 100",
            )
            st.progress(score_value / 100.0)

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Skills")
            for s in profile["skills"]:
                st.write(f"- {s['name']} (level {s['level']}/5)")

        with col2:
            st.subheader("Experience")
            for e in profile["experiences"]:
                st.write(f"- {e['title']} @ {e['company']} — {e['years']} years")

    # ---------------- Roadmap ----------------
    elif page == "Roadmap":
        data = fetch_roadmap()
        st.subheader(f"Learning Roadmap for {data['target_role']}")
        for item in data["items"]:
            with st.expander(f"Week {item['week']}: {item['skill']}"):
                st.markdown("**Objectives:**")
                for obj in item["objectives"]:
                    st.write(f"- {obj}")
                st.markdown("**Resources:**")
                for r in item["resources"]:
                    st.write(f"- {r}")
                st.markdown("**Project idea:**")
                st.write(item["project_idea"])

    # ---------------- Jobs ----------------
    elif page == "Jobs":
        jobs = fetch_jobs()
        st.subheader("Matching Jobs")
        for job in jobs:
            st.markdown(f"### {job['title']} @ {job['company']}")
            st.write(job["location"])
            st.write(f"Match score: **{job['match_score']} / 100**")
            st.write("Required skills: " + ", ".join(job["required_skills"]))
            st.write(f"[Job link]({job['link']})")
            st.markdown("---")

    # ---------------- Interview Prep ----------------
    elif page == "Interview Prep":
        qset = fetch_interview_questions()
        st.subheader(f"Interview Questions – {qset['role']}")
        for q in qset["questions"]:
            st.markdown(f"**[{q['category'].title()} | Difficulty {q['difficulty']}/5]**")
            st.write(q["question"])
            st.markdown("---")

    # ---------------- Upload Resume ----------------
    elif page == "Upload Resume":
        st.subheader("Upload your resume")

        uploaded_file = st.file_uploader("Choose a PDF or DOCX file", type=["pdf", "docx"])

        if uploaded_file is not None:
            st.write(f"Selected file: {uploaded_file.name}")
            if st.button("Upload to CareerPilot"):
                files = {
                    "file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                }
                try:
                    res = requests.post(f"{API_BASE}/profile/upload_resume", files=files)
                    if res.status_code == 200:
                        data = res.json()
                        st.success(f"Uploaded and saved as: {data['saved_path']}")
                    else:
                        st.error(f"Upload failed: {res.status_code} {res.text}")
                except Exception as e:
                    st.error(f"Error uploading file: {e}")


if __name__ == "__main__":
    main()
