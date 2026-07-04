import streamlit as st


def load_css():

    st.markdown(
        """
<style>

/* Main container */
.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

/* Chat messages */
[data-testid="stChatMessage"]{
    border-radius:18px;
    padding:14px;
    margin-bottom:12px;
    border:1px solid rgba(255,255,255,.08);
}

/* Sidebar */
[data-testid="stSidebar"]{
    border-right:1px solid rgba(255,255,255,.08);
}

/* Buttons */
.stButton>button{
    border-radius:12px;
}

/* File uploader */
[data-testid="stFileUploader"]{
    border-radius:12px;
}

</style>
""",
        unsafe_allow_html=True,
    )