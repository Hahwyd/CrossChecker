from django.core.exceptions import ValidationError
from django.core.validators import URLValidator

import re


#validate URL       
def validate_url(url):
    try:
        URLValidator()(url)
    except ValidationError as e:
        raise ValueError(f"Invalid URL: {e}")
    
def validate_wiki_url(url):
    try:
        URLValidator()(url)
    except ValidationError as e:
        raise ValueError(f"Invalid URL: {e}")

    # Check if the URL is a valid wiki URL
    wiki_url_patterns = [
        r"^https?://([a-z]{2})\.wikipedia\.org",
        r"^https?://([a-z]{2})\.wikimedia\.org",
        r"^https?://([a-z]{2})\.wikiquote\.org",
        r"^https?://([a-z]{2})\.wikibooks\.org",
        r"^https?://([a-z]{2})\.wiktionary\.org",
        r"^https?://([a-z]{2})\.wikiversity\.org",
        r"^https?://([a-z]{2})\.wikinews\.org",
        r"^https?://([a-z]{2})\.wikivoyage\.org",
    ]

    is_wiki_url = False
    for pattern in wiki_url_patterns:
        if re.match(pattern, url):
            is_wiki_url = True
            break

    if not is_wiki_url:
        raise ValueError(f"Invalid wiki URL: {url}")
    

#validate question
def validate_question(question):
    if not question:
        raise ValueError("Question cannot be empty")
    if len(question) > 30000:
        raise ValueError("Question is too long (over 30,000 characters)")
    
#question length validator
def validate_question_length(value):
    if len(value) < 5:
        raise ValidationError("Checks must be longer than 5 characters") 

#validate content
def validate_content(content):
    if not content:
        raise ValueError("Content cannot be empty")
    if len(content) > 50000:
        raise ValueError("Content is too long (over 50,000 characters)")
    

