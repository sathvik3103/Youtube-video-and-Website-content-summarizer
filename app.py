import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

st.title("Summarize Any YouTube Video or Website of Your Choice!")
st.subheader("Provide below the URL of the item to Summarize:")

with st.sidebar:
    groq_api_key = st.text_input("Groq API Key:", value="", type='password')

generic_url = st.text_input("URL", label_visibility="collapsed")

llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)

prompt_template = """
Provide a summary of the following content in no more than 500 words:
Content: {text}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

if st.button("Summarize"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide all the required information!")
    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It should be a valid YT video URL or a Website URL.")
    else:
        try:
            with st.spinner("Cooking your summary..."):
                if "youtube.com" in generic_url:
                    loader = YoutubeLoader.from_youtube_url(generic_url, add_video_info=True)
                    docs = loader.load()
                    
                    # Debugging: Check if docs are loaded
                    if not docs:  
                        st.error("No transcript available for this video.")
                    
                    # Debugging: Print loaded documents
                    st.write("Loaded Documents:", [doc.page_content for doc in docs])

                else:
                    loader = UnstructuredURLLoader(urls=[generic_url], ssl_verify=False,
                                                   headers={"User-Agent": "Mozilla/5.0"})
                    docs = loader.load()

                # Ensure docs contain text
                if len(docs) == 0 or all(doc.page_content.strip() == "" for doc in docs):
                    st.error("No content found to summarize.")

                # Prepare input for summarization
                text_to_summarize = "\n".join(doc.page_content for doc in docs if doc.page_content.strip())
                
                if not text_to_summarize.strip():  # Check if combined text is empty
                    st.error("No valid content found to summarize.")
                
                prompt = PromptTemplate(template=prompt_template, input_variables=["text"])
                
                # Initialize the summarization chain
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                
                # Run the summarization chain with correct input key
                output_summary = chain.run({"input_documents": docs})  # Use 'input_documents' key
                
                if output_summary:  # Check if summary is generated
                    st.success(output_summary)
                else:
                    st.error("Failed to generate summary.")
        except Exception as e:
            st.exception(f"Exception: {e}")