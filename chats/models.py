from django.db import models

class ChatMessage(models.Model):
    user = models.CharField(max_length=255, blank=True)
    message = models.TextField()
    reply = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.message}"