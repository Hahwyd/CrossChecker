from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
import json
import logging
from .models import Query
from .scrapper import scrape_wikipedia
from .ai import ai_request

logger = logging.getLogger(__name__)


class HomeView(View):
    def get(self, request):
        return render(request, "checker/index.html")


class CheckWikiView(LoginRequiredMixin, View):
    def post(self, request):
        wiki_url = request.POST.get("wiki_url")
        question = request.POST.get("question")

        if not wiki_url or not question:
            return JsonResponse(
                {"error": "Both URL and question are required."}, status=400
            )

        # Scrape Wikipedia article
        article_text = scrape_wikipedia(wiki_url)
        if not article_text:
            logger.error("Failed to scrape the Wikipedia article.")
            return JsonResponse(
                {"error": "Failed to scrape the Wikipedia article."}, status=500
            )

        # Send data to AI for verification
        ai_response = ai_request(article_text, question)
        if not ai_response:
            logger.error("AI verification failed.")
            return JsonResponse({"error": "AI verification failed."}, status=500)

        # Parse AI response
        try:
            ai_data = json.loads(ai_response)
            result_summary = ai_data.get("summary", "No summary provided.")
            sources = ai_data.get("sources", {})
            # confidence_score = ai_data.get('confidence_score', 0.0)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response: {e}")
            return JsonResponse({"error": "Failed to parse AI response."}, status=500)

        # Save query to database
        try:
            query = Query.objects.create(
                user=request.user,
                wiki_url=wiki_url,
                question=question,
                content=article_text,
                result_summary=result_summary,
                # confidence_score=confidence_score,
                sources=sources,
            )
        except Exception as e:
            logger.error(f"Failed to save query to database: {e}")
            return JsonResponse({"error": "Failed to save query to database."}, status=500)

        return JsonResponse(
            {
                "result_summary": result_summary,
                "sources": sources,
                # 'confidence_score': confidence_score
            }
        )


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        queries = request.user.queries.all()
        return render(request, "checker/profile.html", {"queries": queries})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'checker/signup.html', {'form': form})
