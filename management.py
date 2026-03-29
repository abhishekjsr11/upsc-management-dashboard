import streamlit as st
import random

# 1. THE MEGA SYLLABUS MATRIX (Expanded to 18-20 concepts per unit)
SYLLABUS_MAP = {
    "Managerial Functions": ["Evolution of Management Thoughts", "Planning & MBO", "Organizing & Span of Mgmt", "Control Systems", "Decision Making Models", "Managerial Skills & Roles", "Entrepreneurship", "Innovation Management", "Global Environment Managing", "Flexible Systems Management", "Managerial Ethics", "Value Chain Processes", "Line and Staff Relationships", "Delegation & Empowerment", "Decentralization Strategies", "Management by Exception", "Corporate Social Responsibility", "Crisis Management"],
    "Org. Behaviour": ["Individual personality & Values", "Perception & Attitude", "Motivation Theories", "Learning & Reinforcement", "Work Stress Management", "Power & Politics", "Conflict & Negotiation", "Leadership Styles", "Communication Dynamics", "Job Design", "Organizational Culture", "Diversity Management", "Learning Organizations", "Change & Development", "Virtual Organizations", "Emotional Intelligence", "Transactional Analysis", "Bureaucratic vs Organic structures"],
    "HRM": ["Strategic HRM", "Human Resource Planning", "Job Analysis & Design", "Job Evaluation", "Recruitment & Selection", "Training & Development", "Promotion & Transfer", "Performance Management", "Compensation & Benefits", "Employee Morale", "Industrial Relations", "Collective Bargaining", "Workers Participation", "HR Accounting & Audit", "International HRM", "Talent Management", "Succession Planning", "Outsourcing HR functions"],
    "Accounting": ["GAAP & IFRS", "Financial Statement Analysis", "Inventory Valuation", "Depreciation Accounting", "Fund Flow Analysis", "Cash Flow Statements", "Cost Ledger & Control", "Overhead Costing", "Job & Process Costing", "Budgetary Control", "Zero-Base Budgeting", "Standard Costing", "Marginal & Absorption Costing", "Responsibility Accounting", "Inflation Accounting", "Environmental Accounting", "Cost-Volume-Profit Analysis"],
    "Financial Mgmt": ["Goal of Finance Function", "Valuation of Bonds/Shares", "Working Capital Management", "Cash & Inventory Management", "Cost of Capital", "Capital Budgeting (NPV/IRR)", "Financial & Operating Leverage", "Capital Structure Theories", "Dividend Policy", "Corporate Distress Strategy", "Capital & Money Markets", "Leasing & Venture Capital", "CAPM & Portfolio Theory", "Financial Derivatives", "Foreign Exchange Risk", "Mergers & Acquisitions Finance"],
    "Marketing": ["Marketing Strategy Formulation", "Segmentation & Targeting", "Positioning & Differentiation", "Competition Analysis", "Consumer & Industrial Behavior", "Market Research", "Product Strategy (PLC)", "Pricing Strategies", "Marketing Channels", "Integrated Marketing Communications", "Customer Satisfaction & Retention", "Services & Retail Management", "Digital & Internet Marketing", "Brand Management", "Social Media Marketing", "Green Marketing Trends"],
    "Strategic Mgmt": ["Strategic Intent (Vision/Mission)", "Environmental Analysis", "Internal Analysis & SWOT", "Impact Matrix & Experience Curve", "BCG & GE Nine-Cell Matrix", "Value Chain Analysis", "Growth Strategies", "Mergers & Acquisitions", "Strategic Planning & Implementation", "Balanced Scorecard", "Blue Ocean Strategy", "Corporate Governance", "McKinsey 7S Framework", "Ansoff Product-Market Grid", "Competitor Intelligence"]
}

# 15 UPSC Archetypes (The Multiplier)
QUESTION_STYLES = [
    "Critically examine the relevance of {concept} in the Indian corporate context. (20 marks)",
    "Explain the theoretical foundations of {concept} and its practical hurdles. (10 marks)",
    "Compare and contrast {concept} with contemporary digital-age practices. (15 marks)",
    "As a CEO, how would you leverage {concept} for sustainable advantage? (20 marks)",
    "Discuss the limitations of {concept} in a VUCA environment. (15 marks)",
    "How does {concept} integrate with overall Strategic Planning and Goal setting? (20 marks)",
    "Distinguish between traditional approaches and modern application of {concept}. (10 marks)",
    "Analyze how {concept} influences long-term shareholder value creation. (20 marks)",
    "Evaluate the shift in {concept} strategies due to remote work trends. (15 marks)",
    "What are the ethical implications of {concept} in the context of CSR? (10 marks)",
    "Describe a scenario where a failure in {concept} led to decline. (15 marks)",
    "Explain the role of {concept} in improving organizational agility. (15 marks)",
    "Illustrate the application of {concept} using a case study of an Indian PSU. (20 marks)",
    "How has the concept of {concept} evolved over the last two decades? (15 marks)",
    "To what extent does {concept} serve as a tool for competitive benchmarking? (10 marks)"
]

# 2. SESSION STATE
if 'completed_questions' not in st.session_state:
    st.session_state.completed_questions = set()

# 3. UI SETUP
st.set_page_config(page_title="2000+ Management Tracker", layout="wide")
st.title("📚 UPSC Management: 2000+ Practice Question Matrix")

# 4. SIDEBAR
st.sidebar.header("Tracking Center")
selected_topic = st.sidebar.selectbox("Select Syllabus Unit", list(SYLLABUS_MAP.keys()))

# Metric and Progress
total_qs_possible = sum(len(concepts) * len(QUESTION_STYLES) for concepts in SYLLABUS_MAP.values())
done_count = len(st.session_state.completed_questions)

st.sidebar.metric("Questions Completed", done_count)
st.sidebar.progress(min(done_count / 1000, 1.0)) # Goal 1000

# Topic Mastery Logic
topic_done = len([k for k in st.session_state.completed_questions if k.startswith(selected_topic)])
st.sidebar.write(f"**{selected_topic} Mastery:** {topic_done} questions")

if st.sidebar.button("Reset All Data"):
    st.session_state.completed_questions = set()
    st.rerun()

# 5. GENERATOR
st.subheader(f"Unit: {selected_topic}")

topic_pool = []
concepts = SYLLABUS_MAP[selected_topic]

for concept in concepts:
    for style in QUESTION_STYLES:
        q_text = style.format(concept=concept)
        # Using a stable key based on the text hash
        q_id = f"{selected_topic}_{hash(q_text)}"
        topic_pool.append((q_id, q_text))

random.Random(selected_topic).shuffle(topic_pool)
num_display = st.sidebar.slider("Questions to show", 10, len(topic_pool), 150)
display_list = topic_pool[:num_display]

st.write(f"Generating **{len(topic_pool)}** unique questions for this unit.")

# 6. DISPLAY
for i, (q_id, q_text) in enumerate(display_list, 1):
    col1, col2 = st.columns([0.05, 0.95])
    with col1:
        checked = st.checkbox("", key=q_id, value=(q_id in st.session_state.completed_questions))
        if checked: st.session_state.completed_questions.add(q_id)
        else: st.session_state.completed_questions.discard(q_id)
    with col2:
        if q_id in st.session_state.completed_questions:
            st.write(f"~~Question {i}: {q_text}~~ ✅")
        else:
            st.write(f"**Question {i}:** {q_text}")

st.divider()
st.info(f"Targeting 1000? You have about {1000 - done_count} to go!")