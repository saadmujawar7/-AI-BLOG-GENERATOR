import streamlit as st
from langchain.llms import CTransformers
from fpdf import FPDF  # Ensure fpdf is installed
import time

# ✅ Set Page Config at the TOP
st.set_page_config(page_title="AI Blog Generator", page_icon="📝", layout="wide")

# ✅ Custom Styling
st.markdown(
    """
    <style>
    .main {background-color: #f8f9fa;}
    .stTextInput, .stSelectbox, .stButton > button {border-radius: 10px; padding: 10px;}
    .stButton > button {background-color: #4CAF50; color: white; font-size: 18px;}
    .stHeader {text-align: center;}
    </style>
    """,
    unsafe_allow_html=True
)

# ✅ Load Llama 2 Model Once
@st.cache_resource
def load_model():
    return CTransformers(
        model="C:/Users/Lenovo/OneDrive/Desktop/LLM2/models/llama-2-7b-chat.ggmlv3.q8_0.bin",  
        model_type="llama",
        config={"temperature": 0.01}
    )

llm = load_model()  # Load model once and reuse

# ✅ Function to Generate Blog Content
def getLLamaResponse(text_input, no_words, blog_style):
    try:
        no_words = int(no_words)  # Convert input to integer
        max_tokens = min(no_words * 2, 512)  # Dynamically set max_new_tokens
        
        prompt = f"""
        Write a blog for {blog_style} job profile on the topic "{text_input}" 
        within {no_words} words.
        """

        response = llm(prompt, max_new_tokens=max_tokens)
        return response
    except ValueError:
        return "⚠️ Please enter a valid number for word count."
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ Function to Save as PDF
def save_as_pdf(blog_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for line in blog_text.split("\n"):
        pdf.cell(200, 10, txt=line, ln=True, align="L")
    
    pdf_output = "blog_output.pdf"
    pdf.output(pdf_output)
    return pdf_output

# ✅ Header Section
st.markdown("""
    <h1 style='text-align: center; color: #333;'>🚀 AI-Powered Blog Generator 📝</h1>
    <p style='text-align: center; font-size: 18px;'>Generate high-quality blogs with Llama 2 AI Model in seconds!</p>
""", unsafe_allow_html=True)

# ✅ Input Section
st.subheader("Enter Blog Details")
input_text = st.text_input("📝 Enter the blog topic")
col1, col2 = st.columns(2)

with col1:
    no_words = st.text_input("🔢 Number of words")

with col2:
    blog_style = st.selectbox("✍️ Writing style", ("researcher", "data analyst", "common people"), index=0)

st.markdown("""---""")  # Add a horizontal line

# ✅ Generate Button
submit = st.button("💡 Generate Blog")

# ✅ Generate Blog and Show Output
if submit:
    if not input_text.strip():
        st.warning("⚠️ Please enter a blog topic.")
    elif not no_words.strip():
        st.warning("⚠️ Please enter the number of words.")
    else:
        with st.spinner("⏳ Generating your blog..."):
            time.sleep(2)  # Simulate loading
            blog_text = getLLamaResponse(input_text, no_words, blog_style)
            st.success("✅ Blog generated successfully!")
            st.markdown("### 📝 Generated Blog Content:")
            st.write(blog_text)
            
            # Download as PDF
            pdf_path = save_as_pdf(blog_text)
            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="📄 Download as PDF",
                    data=pdf_file,
                    file_name="blog_output.pdf",
                    mime="application/pdf"
                )
