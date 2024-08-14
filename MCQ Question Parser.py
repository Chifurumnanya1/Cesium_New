import streamlit as st
import re

def convert_mcq_content(mcq_text):
    # Split the input text into individual lines
    lines = mcq_text.strip().splitlines()
    
    formatted_output = []
    current_question = ""
    current_answers = []

    # Regular expressions to match question numbers and answer options
    question_regex = re.compile(r"^\d+\.\s*(.+)")
    answer_regex = re.compile(r"^[A-Za-z][\.\)]\s*(.+)")
    
    for line in lines:
        line = line.strip()
        if line:
            question_match = question_regex.match(line)
            answer_match = answer_regex.match(line)
            
            if question_match:
                # Save the previous question and its answers
                if current_question:
                    formatted_output.append(f"## {current_question}")
                    formatted_output.extend(current_answers)
                    formatted_output.append("")  # Add a space after each question
                
                # Start a new question
                current_question = question_match.group(1)
                current_answers = []
            elif answer_match:
                # Add the answer to the current list of answers
                current_answers.append(f"** {answer_match.group(1)}")
        else:
            # Handle non-continuous MCQ format (empty line between questions)
            if current_question:
                formatted_output.append(f"## {current_question}")
                formatted_output.extend(current_answers)
                formatted_output.append("")  # Add a space after each question
                current_question = ""
                current_answers = []
    
    # Add the last question and its answers
    if current_question:
        formatted_output.append(f"## {current_question}")
        formatted_output.extend(current_answers)

    return "\n".join(formatted_output)

def main():
    st.title("MCQ Converter")
    st.write("Upload a text file containing MCQ questions, and this app will process it and provide the output as a downloadable text file.")

    uploaded_file = st.file_uploader("Choose a text file", type="txt")

    if uploaded_file is not None:
        # Read the file content as string
        mcq_text = uploaded_file.read().decode("utf-8")
        
        # Convert the MCQ content
        converted_text = convert_mcq_content(mcq_text)

        # Create a downloadable text file with the converted content
        st.download_button(
            label="Download converted file",
            data=converted_text,
            file_name="converted_mcq.txt",
            mime="text/plain"
        )

if __name__ == "__main__":
    main()