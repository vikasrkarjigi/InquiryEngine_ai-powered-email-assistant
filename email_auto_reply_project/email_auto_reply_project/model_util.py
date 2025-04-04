from django.http import JsonResponse

from . import models
from typing import List

from .models import InquiryUser, EmailInquiry, InquiryQuestion


def retrieve_all_inquiry_questions():
    all_inquiry_questions = models.InquiryQuestion.objects.all()
    print(f" ### ### ### {all_inquiry_questions}")
    return all_inquiry_questions

def get_inquiry_history(request):
    questions = retrieve_all_inquiry_questions()
    question_list = [
        {"question": q.question, "answer": q.answer if q.answer else "[No answer yet]"}
        for q in questions
    ]
    return JsonResponse(question_list, safe=False)

# def save_inquiry_question(questions: List[str], email_content: str):
#     # Create EmailInquiry objects
#     email_inquiry = models.EmailInquiry(email_content=email_content)
#     email_inquiry.save()
#
#     # Create InquiryQuestion objects
#     for question in questions:
#         inquiry_question = models.InquiryQuestion(question=question, email_inquiry=email_inquiry)
#         inquiry_question.save()
#
#     return email_inquiry

def save_inquiry_question(questions: list, email_content: str, sender_name: str, sender_email: str):
    """Saves sender details, email inquiry, and extracted questions."""

    # Split sender name into first_name and last_name
    name_parts = sender_name.split()
    first_name = name_parts[0] if len(name_parts) > 0 else "Unknown"
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""

    # Check if user already exists, else create a new user
    user, created = InquiryUser.objects.get_or_create(
        email=sender_email,
        defaults={"first_name": first_name, "last_name": last_name}
    )

    # Save email inquiry
    email_inquiry = EmailInquiry.objects.create(user=user, email_content=email_content)

    # Save each question
    for question in questions:
        InquiryQuestion.objects.create(email_inquiry=email_inquiry, question=question)


def generate_email_from_name(name: str) -> str:
    """Generates an email based on the sender's name."""
    name_parts = name.lower().split()
    email = "".join(name_parts) + "@example.com"
    return email