from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Query
from .scrapper import scrape_wikipedia
from .scrapper import check_facts

class CheckWikiView(APIView):
    def post(self, request):
        url = request.data.get("url")
        question = request.data.get("question")

        content = scrape_wikipedia(url)
        result, sources = check_facts(content, question)
        alt_sources = get_alternative_sources(question)

        query = Query.objects.create(
            url=url, question=question, result=result, sources=alt_sources
        )

        return Response({
            "result": result,
            "sources": alt_sources
        })

