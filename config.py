import os
import sys
import glob
from dotenv import load_dotenv
from aita_core import CourseConfig

load_dotenv()

BASE_DIR = os.path.dirname(__file__)
_client_secret_matches = glob.glob(os.path.join(BASE_DIR, "client_secret*.json"))

# Google Auth requires: client_secret file + GOOGLE_COOKIE_KEY + GOOGLE_REDIRECT_URI
_google_cookie_key = os.getenv("GOOGLE_COOKIE_KEY")
_google_redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
if _client_secret_matches and _google_cookie_key and _google_redirect_uri:
    _google_client_secret = _client_secret_matches[0]
else:
    _google_client_secret = ""
    if _client_secret_matches:
        print("[WARN] Google OAuth: client_secret found but GOOGLE_COOKIE_KEY or "
              "GOOGLE_REDIRECT_URI not set. Falling back to student ID login.",
              file=sys.stderr)

SYSTEM_PROMPT = """\
You are an AI Teaching Assistant for CEGE 3201: Transportation Engineering \
at the University of Minnesota. The course is taught by Prof. Michael Levin and covers \
planning, analysis, and design of transportation systems: travel demand modeling, \
mode choice, network analysis, transit operations, traffic flow theory, level of service, \
signal control, and roadway geometric design.

The textbook is "Principles of Highway Engineering and Traffic Analysis" (7th ed.) \
by Mannering, Kilareski, and Washburn.

YOUR CORE PRINCIPLE: You must NEVER give direct answers to homework or exam problems. \
Instead, you should:
- Ask Socratic questions to guide students toward understanding
- Provide hints and point students to relevant concepts or course materials
- Explain underlying principles without solving the specific problem
- Encourage students to attempt the problem first and share their reasoning
- When students share their work, help them identify errors conceptually
- Use analogies and simple examples (different from homework) to build intuition

CRITICAL — CATCHING MISCONCEPTIONS:
When a student provides an example, explanation, or reasoning, you MUST carefully check \
whether it is correct before praising or accepting it. Specifically:
- Check if the example actually satisfies all assumptions/conditions of the concept \
(e.g., equilibrium conditions, flow conservation, valid units, correct formulas)
- If the student's example violates an assumption you just explained, point it out \
immediately and gently — do NOT say "Great start!" and move on
- Ask the student: "Does your answer satisfy all the conditions we discussed?" \
before confirming it is correct
- It is better to catch a misconception early than to let it pass uncorrected
- Remember: students learn MORE from having their mistakes caught than from being told \
they are right when they are wrong

When responding:
- If your answer draws on course materials, cite the source (e.g., "See Slides: Traffic flow theory")
- If a question is clearly a homework problem, acknowledge it and help them understand the concept, but do NOT solve it
- Be encouraging, patient, and supportive
- Keep responses focused and concise — students want clarity, not walls of text
- If the question is not related to the course, politely redirect
- Use LaTeX for math: inline with single dollars $t(x) = t_0(1 + 0.15(x/C)^4)$ and display math with double dollars $$t(x) = t_0\\left(1 + 0.15\\left(\\frac{x}{C}\\right)^4\\right)$$
- IMPORTANT: Never use \\[ \\] or \\( \\) for LaTeX. Always use $...$ for inline and $$...$$ for display equations.

You will be provided with relevant context from course materials to ground your responses.\
"""

CONFIG = CourseConfig(
    course_id="3201",
    course_name="CEGE 3201: AI Teaching Assistant",
    course_short_name="CEGE 3201 AITA",
    course_description=(
        "Welcome! This AI assistant helps you learn transportation engineering "
        "concepts for **CEGE 3201: Transportation Engineering**."
    ),
    system_prompt=SYSTEM_PROMPT,
    week_topics={
        1:  ["Orientation", "Four-step model overview"],
        2:  ["Land use", "Trip generation"],
        3:  ["Trip distribution", "Mode choice"],
        4:  ["Traffic assignment", "Shortest path"],
        5:  ["Traffic network analysis", "Dynamic traffic assignment"],
        6:  ["Project evaluation", "Transit demand"],
        7:  ["Transit planning", "Transit operations"],
        8:  ["Midterm 1 review"],
        9:  ["Queueing theory", "Traffic flow theory"],
        10: ["Traffic flow theory", "Capacity and level of service"],
        11: ["Capacity and level of service", "Traffic signal hardware"],
        12: ["Signal timing", "Signal coordination and actuation"],
        13: ["Highway geometric design"],
        14: ["Emerging technologies"],
        15: ["Final exam review"],
    },
    topic_num_to_week={
        1: 1, 2: 2, 3: 3, 4: 3, 5: 4, 6: 4, 7: 6,
        8: 9, 9: 9, 10: 9, 11: 10, 12: 11, 13: 13, 14: 13,
    },
    hw_num_to_week={
        0: 1, 1: 3, 2: 4, 3: 5, 4: 6, 5: 8,
        6: 9, 7: 10, 8: 11, 9: 13, 10: 14, 11: 15,
    },
    lab_num_to_week={
        1: 2, 2: 5, 3: 9, 4: 12,
    },
    study_guide_to_week={},
    textbook_url="https://en.wikibooks.org/wiki/Fundamentals_of_Transportation",
    textbook_chapter_to_week={
        "Introduction": 1,
        "Planning": 1,
        "Land_Use_Forecasting": 2,
        "Trip_Generation": 2,
        "Destination_Choice": 3,
        "Modal_Split": 3,
        "Route_Choice": 4,
        "Networks": 4,
        "Evaluation": 6,
        "Transit": 6,
        "Transit_Demand": 6,
        "Transit_Operations_and_Capacity": 7,
        "Network_Design_and_Frequency": 7,
        "Queueing": 9,
        "Traffic_Flow": 9,
        "Queueing_and_Traffic_Flow": 9,
        "Shockwaves": 10,
        "Traffic_Signals": 12,
        "Traffic_Control_Devices": 12,
        "Design": 13,
        "Sight_Distance": 13,
        "Vertical_Curves": 13,
        "Horizontal_Curves": 13,
    },
    example_prompts={
        1: [
            "What topics does this course cover?",
            "What is the four-step transportation planning model?",
            "What are the prerequisites for this course?",
            "How is the grading structured?",
        ],
        2: [
            "What is trip generation?",
            "How do I build a linear regression model for trip prediction?",
            "What factors affect household trip generation?",
            "Help me with this week's homework",
        ],
        3: [
            "How does the gravity model work for trip distribution?",
            "What is the multinomial logit model?",
            "How do travel times affect trip distribution?",
            "Help me with this week's homework",
        ],
        4: [
            "What is user equilibrium in traffic assignment?",
            "How does Dijkstra's shortest path algorithm work?",
            "What is the Braess paradox?",
            "Help me with this week's homework",
        ],
        5: [
            "What is system optimal traffic assignment?",
            "How does the BPR function work?",
            "What is the price of anarchy?",
            "Help me with this week's homework",
        ],
        6: [
            "How do you evaluate transportation projects?",
            "What factors influence transit demand?",
            "What is the difference between transit modes?",
            "Help me with this week's homework",
        ],
        7: [
            "How do you plan a transit route?",
            "What is headway and how is it determined?",
            "How do you calculate bus cycle time?",
            "Help me with this week's homework",
        ],
        8: [
            "What topics should I review for the midterm?",
            "Can you help me practice traffic assignment problems?",
            "What are the key formulas for trip distribution?",
            "Help me review mode choice concepts",
        ],
        9: [
            "What is queueing theory?",
            "How do you calculate D/D/1 queue delays?",
            "What is the Greenshields traffic flow model?",
            "Help me with this week's homework",
        ],
        10: [
            "What is the flow-density relationship?",
            "How do you determine freeway level of service?",
            "What is time-mean speed vs space-mean speed?",
            "Help me with this week's homework",
        ],
        11: [
            "How do you calculate freeway capacity?",
            "What factors affect level of service?",
            "What is saturation flow rate?",
            "Help me with this week's homework",
        ],
        12: [
            "How do you design a traffic signal timing plan?",
            "What is Webster's formula for cycle length?",
            "How does signal coordination work?",
            "Help me with this week's homework",
        ],
        13: [
            "How do you design a vertical curve?",
            "What is stopping sight distance?",
            "How do you calculate minimum curve length?",
            "Help me with this week's homework",
        ],
        14: [
            "How will autonomous vehicles affect transportation?",
            "What are current trends in transportation engineering?",
            "How do emerging technologies change traffic flow?",
            "Help me review for the final exam",
        ],
        15: [
            "What topics should I focus on for the final?",
            "Can you help me review traffic signal timing?",
            "Help me practice capacity/LOS problems",
            "What are the key formulas for geometric design?",
        ],
    },
    base_dir=BASE_DIR,
    course_materials_dir=os.path.join(BASE_DIR, "course_materials"),
    faiss_db_dir=os.path.join(BASE_DIR, "faiss_db"),
    docs_dir=os.path.join(BASE_DIR, "docs"),
    backup_dir=os.path.join(BASE_DIR, "backup"),
    data_dir=os.getenv("AITA_DATA_DIR", os.path.join(BASE_DIR, "data")),
    admin_password=os.getenv("ADMIN_PASSWORD", ""),
    cookie_name="aita_3201_auth",
    cookie_key=_google_cookie_key or "",
    redirect_uri=_google_redirect_uri or "http://localhost:30002",
    google_client_secret_file=_google_client_secret,
)
