import streamlit as st
from google import genai
import pypdf
import io

# --- 1. SETUP & THEME ---
st.set_page_config(page_title="ScholarFlow AI", page_icon="🎓", layout="wide")

# This pulls your key safely from the "Secrets" menu in the online compiler
GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
client = genai.Client(api_key=GEMINI_API_KEY)

# --- 2. THE "BRAIN" FUNCTIONS ---
def extract_text_from_pdf(file):
    reader = pypdf.PdfReader(file)
    return " ".join([page.extract_text() for page in reader.pages])

def generate_ai_content(prompt_type, context_text):
    if prompt_type == "notes":
        prompt = f"Create structured, bulleted study notes from this text. Include a 'Key Terms' section:\n\n{context_text}"
    else:
        prompt = f"Explain this concept simply for a student, using examples:\n\n{context_text}"
    
    response = client.models.generate_content(model="gemini-1.5-flash", contents=prompt)
    return response.text

# --- 3. THE USER INTERFACE (UI) ---
st.title("🎓 ScholarFlow: The All-in-One Study System")
st.markdown("### Stop switching tabs. Start mastering your material.")

tab1, tab2 = st.tabs(["📝 Smart PDF Notes", "🔍 Instant Research"])

# --- TAB 1: PDF PROCESSING ---
with tab1:
    st.header("Upload Your Material")
    file = st.file_uploader("Drop your PDF here", type="pdf")
    
    if file:
        if st.button("Generate Pro Notes"):
            with st.spinner("Analyzing your document..."):
                raw_text = extract_text_from_pdf(file)
                # We send the first 10,000 characters to keep it fast
                notes = generate_ai_content("notes", raw_text[:10000])
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info("📄 PDF Content Detected")
                    st.write(raw_text[:500] + "...")
                with col2:
                    st.success("✅ AI-Generated Notes")
                    st.markdown(notes)
                    st.download_button("Download Notes", notes, file_name="ScholarFlow_Notes.txt")

# --- TAB 2: IN-APP RESEARCH ---
with tab2:
    st.header("Search the System")
    query = st.text_input("What concept do you need help with?")
    
    if query:
        with st.spinner("Consulting internal database..."):
            result = generate_ai_content("research", query)
            st.markdown("---")
            st.markdown(f"### Results for: {query}")
            st.write(result)

# --- SIDEBAR FOR THE 'SYSTEM' FEEL ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3413/3413535.png", width=100)
st.sidebar.title("ScholarFlow v1.0")
st.sidebar.info("A responsive, AI-powered environment for modern students.")
