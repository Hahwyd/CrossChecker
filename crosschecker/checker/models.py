from django.db import models
from django.contrib.auth.models import User
import logging

logger= logging.getLogger("checker")


class Query(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queries", verbose_name="User")
    wiki_url = models.URLField(verbose_name="Wiki url", null=True, blank=True)
    question = models.TextField(verbose_name="User question", null=True, blank=True)
    content = models.TextField(verbose_name="Article text", null=True, blank=True)
    result_summary = models.TextField(verbose_name="Result Summary", null=True, blank=True)
    confidence_score = models.FloatField(verbose_name="AI Confidence Score", null=True, blank=True)
    sources = models.JSONField(verbose_name="Alternative sources", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"{self.user.username}: {self.question[:50]}..."
