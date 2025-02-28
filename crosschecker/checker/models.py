from django.db import models
from django.contrib.auth.models import User
import logging
from .validators import validate_question_length, validate_question, validate_content, validate_url, validate_wiki_url, validate_wikipedia_url, validate_wikipedia_url_json
from .permissions import IsOwner, IsAdminOrReadOnly
from .utils import scrape_wikipedia

logger= logging.getLogger("checker")



class WikipediaArticle(models.Model):
    url = models.URLField(validators=[validate_wikipedia_url])

class WikipediaArticleJSON(models.Model):
    url = models.URLField(validators=[validate_wikipedia_url_json])


class Query(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="queries", verbose_name="User")
    wiki_url = models.URLField(verbose_name="Wiki url", null=True, blank=True)
    question = models.TextField(verbose_name="User question", null=True, blank=True)
    content = models.TextField(verbose_name="Article text", null=True, blank=True)
    result_summary = models.TextField(verbose_name="Result Summary", null=True, blank=True)
    confidence_score = models.FloatField(verbose_name="AI Confidence Score", null=True, blank=True)
    sources = models.JSONField(verbose_name="Alternative sources", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def clean(self):
        validate_wiki_url(self.wiki_url)
        validate_url(self.wiki_url)
        validate_content(self.content)
        validate_question(self.question)
        validate_question_length(self.question)
        

    def __str__(self):
        return f"{self.user.username}: {self.question[:50]}..."

class MyModel(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        permissions = (
            ('can_edit_mymodel', 'Can edit my model'),
            ('can_manage_mymodel', 'Can manage my model'),
        )