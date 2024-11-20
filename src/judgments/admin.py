from django.contrib import admin
from .models import Judgment, JudgmentScrapeEvent

# Register your models here.
admin.site.register(Judgment)
admin.site.register(JudgmentScrapeEvent)