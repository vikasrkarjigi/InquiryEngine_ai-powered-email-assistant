import json

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import re

from . import views_util, models, model_util
from . import llm_util


def home(request):
    # return HttpResponse("Hello from Open Avenues Build Project!")
    # return render(request, 'home')
    # return render(request, 'auto_reply.html')
    all_inquiry_questions = model_util.retrieve_all_inquiry_questions()
    return render(request, 'auto_reply_inquiry_questions.html', {'inquiry_questions': all_inquiry_questions})



@csrf_exempt # To disable CSRF protection for this view (use with caution!)
def auto_reply_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            paragraph = data.get('content', '')

            # Assignment - 1
            # sender_name = views_util.extract_sender_name(paragraph)
            # receiver_name = views_util.extract_receiver_name(paragraph)

            # Assignment - 2 & 3
            sender_name, receiver_name, inquiry_questions = views_util.extract_receiver_and_sender_names(paragraph)
            # views_util.extract_receiver_and_sender_names(paragraph)
            # print(sender_name, "-->", receiver_name, "-->", inquiry_questions)

            # Check if any questions were extracted
            if not inquiry_questions:
                # Use regex to find questions if llm_util did not extract any
                inquiry_questions = re.findall(r'([^.?!]*\?)', paragraph)

            if sender_name and receiver_name:
                reply_message = f"Hi {sender_name}, \n\n Thanks for your email. I will get back to you soon. \n\n Best, {receiver_name}"
                return JsonResponse({'reply': reply_message, 'status': 'success', 'sender_name': sender_name,
                                     'receiver_name': receiver_name, 'inquiry_questions': inquiry_questions})
            elif sender_name:
                reply_message = f"Hi {sender_name}, \n\n Thanks for your email. I will get back to you soon. \n\n Best,"
                return JsonResponse({'reply': reply_message, 'status': 'Missing reciever name in the response', 'sender_name': sender_name,
                                     'receiver_name': receiver_name, 'inquiry_questions': inquiry_questions})

            elif receiver_name:
                reply_message = f"Hi there, \n\n Thanks for your email. I will get back to you soon. \n\n Best, {receiver_name}"
                return JsonResponse({'reply': reply_message, 'status': 'Missing sender name in the response', 'sender_name': sender_name,
                                     'receiver_name': receiver_name, 'inquiry_questions': inquiry_questions})

            else:
                reply_message = f"Hi there, \n\n Thanks for your email. I will get back to you soon. \n\n Best,"
                return JsonResponse({'reply': reply_message, 'status': 'Missing sender and reciever name in the response', 'sender_name': sender_name,
                                     'receiver_name': receiver_name, 'inquiry_questions': inquiry_questions})


        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format', 'status': 'failure'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed', 'status':'failure'}, status=405)