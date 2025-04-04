import re

from . import llm_util, model_util


def extract_sender_name(paragraph):
    # reply_message = "Thanks for your email. I will get back to you soon."
    # Extract sender's name (assumes format: "Regards, Name." or similar)
    # Extract sender's name from common sign-offs
    sender_match = re.search(
        r"(?:Best|Regards|Thanks|Sincerely|Cheers|Warm regards|Kind regards)[,|-]?\s+([\w\s]+)[.,]?$",
        paragraph, re.IGNORECASE
    )
    sender_name = sender_match.group(1).strip() if sender_match else "there"
    return sender_name

def extract_receiver_name(paragraph):
    # Extract receiver's name (assumes email starts with "Hi Name,")
    receiver_match = re.search(r"^(Hi|Hey|Hello|Dear)\s+([\w]+),", paragraph, re.IGNORECASE)
    receiver_name = receiver_match.group(2) if receiver_match else "User"
    return receiver_name

# def extract_receiver_and_sender_names(email_content: str):
#     sender_name, receiver_name, inquiry_questions = llm_util.extract_names_and_questions(email_content)
#     model_util.save_inquiry_question(inquiry_questions, email_content)
#     return sender_name, receiver_name, inquiry_questions

def extract_receiver_and_sender_names(email_content: str):
    sender_name, receiver_name, inquiry_questions = llm_util.extract_names_and_questions(email_content)

    # Generate sender email (example: "John Doe" → "johndoe@example.com")
    sender_email = model_util.generate_email_from_name(sender_name)

    # Save inquiry user and questions
    model_util.save_inquiry_question(inquiry_questions, email_content, sender_name, sender_email)

    return sender_name, receiver_name, inquiry_questions


