import streamlit as st
from code_verifier_params import CodeVerifierParams

def main():
    st.title("Streamlit File Viewer")

    # Sidebar options
    option = st.sidebar.radio("Choose an option:", ("Write Code", "Browse File System"))

    if option == "Write Code":
        # Code writing section
        code = st.text_area("Write your code here:", height=200)
        params = CodeVerifierParams
        params.code = code

        response = params.verify_code()
        st.write(f"Your response the following code:")
        st.code(response, language="python")
    elif option == "Browse File System":
        # File selection section
        selected_file = st.file_uploader("Upload a file", type=["txt", "csv", "json"])
        if selected_file:
            file_content = selected_file.read().decode("utf-8")
            st.write("File content:")
            st.code(file_content, language="text")

    # Submit and cancel buttons
    col1, col2 = st.columns(2)
    if col1.button("Submit"):
        # Implement your submit logic here
        st.success("Submitted successfully!")

    if col2.button("Cancel"):
        # Implement your cancel logic here
        st.warning("Operation canceled.")

if __name__ == "__main__":
    main()