import streamlit as st
from groq import Groq

# Set page configuration
st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate tailored posts, captions, and hashtags in seconds.")

# Sidebar for API key input
st.sidebar.header("Settings")
groq_api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

# Input Form
with st.form("content_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        platform = st.selectbox("Target Platform", ["LinkedIn", "Instagram", "Twitter/X", "Facebook", "Blog Post"])
        content_type = st.selectbox("Content Type", ["Educational", "Promotional", "Storytelling", "Opinion/Thought Leadership", "Announcement"])
        tone = st.selectbox("Tone of Voice", ["Professional", "Casual & Friendly", "Energetic", "Witty & Humorous", "Inspiring"])

    with col2:
        topic = st.text_input("Topic / Key Idea", placeholder="e.g., Launching a new remote work tool")
        audience = st.text_input("Target Audience", placeholder="e.g., Tech founders, Freelancers, Students")

    submit_btn = st.form_submit_button("Generate Content ✨")

# Generation Logic
if submit_btn:
    if not groq_api_key:
        st.error("Please enter your Groq API Key in the sidebar.")
    elif not topic or not audience:
        st.warning("Please provide both a topic and a target audience.")
    else:
        with st.spinner("Drafting your post..."):
            try:
                # Initialize Groq Client
                client = Groq(api_key=groq_api_key)
                
                # Construct Prompt
                prompt = f"""
                You are an expert social media copywriter. Generate a high-performing post based on these specs:
                - Platform: {platform}
                - Content Type: {content_type}
                - Topic: {topic}
                - Target Audience: {audience}
                - Tone: {tone}

                Output structure:
                1. A catchy headline/hook.
                2. Main body copy (formatted with clear spacing/emojis appropriate for the platform).
                3. A Call to Action (CTA).
                4. A block of 5-8 highly relevant hashtags.
                """

                # Call Groq API
                completion = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                )

                output = completion.choices[0].message.content

                st.success("Generated Content:")
                st.markdown(output)

            except Exception as e:
                st.error(f"An error occurred: {e}")
