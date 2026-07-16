import os
os.environ["TRANSFORMERS_VERBOSITY"] = "error"

import streamlit as st
from ui.ui import main

if __name__ == "__main__":
    main()