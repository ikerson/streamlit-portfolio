import streamlit as st
from pathlib import Path

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
css_file = current_dir / "pages" / "styles" / "main.css"

# load css
with open(css_file) as f:
    st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

st.markdown("# Portfolio Introduction🎈")
st.sidebar.markdown("# Portfolio Introduction🎈")