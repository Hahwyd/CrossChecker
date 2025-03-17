from django.db import models
from django.contrib.auth.models import User, AbstractUser, Permission, Group
import logging
from .validators import validate_question_length, validate_question, validate_content, validate_url, validate_wiki_url, validate_wikipedia_url, validate_wikipedia_url_json, validate_email,validate_username
from .permissions import IsOwner, IsAdminOrReadOnly

logger = logging.getLogger("checker")
debug_logger = logging.getLogger("debug")
info_logger = logging.getLogger("info")
warning_logger = logging.getLogger("warning")
error_logger = logging.getLogger("error")
critical_logger = logging.getLogger("critical")


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, validators=[validate_email])
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text="for the groups this user belongs to the user will get all permissions of the groups.",
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_permissions",
        related_query_name="custom_user",
    )

    def __str__(self) -> str:
        return self.username

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith(""):
            self.set_password(self.password)
        if self.first_name:
            self.first_name = self.first_name.capitalize()
        if self.last_name:
            self.last_name = self.last_name.capitalize()
        logger.info(f"Saving {self.username} with {self.password}")
        super().save(*args, **kwargs)

    def clean(self) -> None:
        super().clean()
        validate_username(self.username)

    class Meta:
        ordering = ["username", "first_name", "last_name"]
        db_table = "crosschecker_db"
        verbose_name = "User"
        verbose_name_plural = "Users"


class WikipediaArticle(models.Model):
    url = models.URLField(validators=[validate_wikipedia_url])


class WikipediaArticleJSON(models.Model):
    url = models.URLField(validators=[validate_wikipedia_url_json])


class Query(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="queries", verbose_name="User")
    wiki_url = models.URLField(verbose_name="Wiki url", null=True, blank=True)
    question = models.TextField(verbose_name="User question", null=True, blank=True)
    content = models.TextField(verbose_name="Article text", null=True, blank=True)
    result_summary = models.TextField(verbose_name="Result Summary", null=True, blank=True)
    confidence_score = models.IntegerField(verbose_name="AI Confidence Score", null=True, blank=True)
    sources = models.JSONField(verbose_name="Alternative sources", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def clean(self):
        validate_wiki_url(self.wiki_url)
        validate_url(self.wiki_url)
        validate_content(self.content)
        validate_question(self.question)
        validate_question_length(self.question)

    '''def __str__(self):
        return f"{self.user.username}: {self.question[:50]}... On {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}"'''
