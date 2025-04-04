from django.contrib import admin
from .models import InquiryUser, EmailInquiry, InquiryQuestion

@admin.register(InquiryUser)
class InquiryUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")

@admin.register(EmailInquiry)
class EmailInquiryAdmin(admin.ModelAdmin):
    list_display = ("user", "inquiry_timestamp")
    search_fields = ("user__first_name", "user__last_name", "email_content")

@admin.register(InquiryQuestion)
class InquiryQuestionAdmin(admin.ModelAdmin):
    list_display = ("email_inquiry", "question", "answer")
    search_fields = ("question", "answer")
