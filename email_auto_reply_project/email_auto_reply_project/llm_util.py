from google import genai
from .settings import GEMINI_API_KEY


def extract_names_and_questions(email_content: str):
    # Initialize the Gemini client
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Assignment 2
    # Define your prompt content (replace this with your actual prompt)
    # email_content = "Hello Yuan, how are you doing today? Best, Isa"

    # prompt = f"""
    #     Given the following email content, extract the only sender and receiver names,
    #     don't include any other messages or different format:
    #
    #     Email Content: "{email_content}"
    #
    #     The output should be as in the below format and if you don't find either Sender Name or Receiver Name in the
    #     email content, pass empty string to the respective field.
    #     Sender Name:
    #     Receiver Name:
    #
    #     """

    # Assignment 3
    prompt = f"""
               Given the following email content, extract the sender and receiver names and also all inquiry 
               questions. Do not include greetings, introductory phrases, or any context. Only include the exact 
               questions as they appear, with each question on a new line.

               Email Content: "{email_content}"

               The output should be in the following format, and if you don't find either Sender Name or Receiver Name in the 
               email content, pass an empty string to the respective field.
               Sender Name: 
               Receiver Name:
               Inquiry Questions:[
                   [First inquiry question],
                   [Second inquiry question],
                   ...
                   ..
               ]

               Strictly include only sentences that are actual questions (ending with a question mark) and 
               do not include any statements, greetings, or non-question sentences.
               If there are no questions, return an empty list: '"Inquiry Questions": []'.
               """

    try:
        # Sending the request to the Gemini model
        response = client.models.generate_content(
            model="gemini-2.0-flash",  # Specify the Gemini model
            contents=[
                "you are a helpful assistant.",  # Input as a string, not a dictionary
                prompt  # User prompt
            ]
        )

        # Print the response from Gemini model
        print(response.text)  # Assuming response.text contains the generated output

        # Check if the response has valid text
        response_text = response.text.strip() if response.text else ""
        if not response_text:
            raise ValueError("Empty response from Gemini model")

        # Initialize default values
        sender_name = ""
        receiver_name = ""
        inquiry_questions = []

        # Split the response into lines and process
        in_questions = False
        lines = response_text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith("Sender Name:"):
                sender_name = line.split("Sender Name:")[-1].strip()
            elif line.startswith("Receiver Name:"):
                receiver_name = line.split("Receiver Name:")[-1].strip()
            elif line.startswith("Inquiry Questions:"):
                in_questions = True  # Start reading questions
                continue  # Skip the current line
            elif in_questions:
                if line == "]":  # End of the questions block
                    in_questions = False
                    continue
                # Extract the question from the line, removing commas and brackets
                question = line.strip(" [],")
                if question:
                    inquiry_questions.append(question)

        # Return the extracted names and questions list
        print(sender_name, "-->", receiver_name, "-->", inquiry_questions)
        return sender_name, receiver_name, inquiry_questions

    except Exception as e:
        print(f"Error occurred: {e}")
        return "", "", []