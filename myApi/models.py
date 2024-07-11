from django.db import models

class ConversationHistory(models.Model):
    message = models.CharField(max_length = 255)
    reply = models.CharField(max_length = 255)
    timestamp = models.DateTimeField(auto_now_add=True)
