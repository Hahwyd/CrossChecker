from django.http import HttpResponse, HttpResponseForbidden, HttpResponseNotFound, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView, CreateView, FormView, RedirectView, UpdateView, DeleteView
from rest_framework import generics
from .models import Query, CustomUser
from .scrapper import scrape_wikipedia
from .ai import ai_request
from .permissions import IsOwner, IsAdminOrReadOnly
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm, PasswordConfirmationForm
import json
import logging

logger = logging.getLogger("checker")

debug_logger = logging.getLogger('debug')
info_logger = logging.getLogger('info')
warning_logger = logging.getLogger('warning')
error_logger = logging.getLogger('error')
critical_logger = logging.getLogger('critical')

def my_view(request):
    debug_logger.debug('This is a debug message')
    info_logger.info('This is an info message')
    warning_logger.warning
    error_logger.error
    critical_logger.critical


class HomePageView(TemplateView):
    template_name = "checker/index.html"

    def get(self, request, *args, **kwargs):
        logger.info(f"The home page is visited by {request.user}")
        return super().get(request, *args, **kwargs)


class CheckWikiView(LoginRequiredMixin, TemplateView):
    template_name = "checker/index.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        wiki_url = request.POST.get("wiki_url")
        question = request.POST.get("question")
        if not wiki_url or not question:
            return JsonResponse({"error": "Both URL and question are required."}, status=400)
        # Scrape Wikipedia article
        article_text = scrape_wikipedia(wiki_url)
        if not article_text:
            logger.error("Failed to scrape the Wikipedia article.")
            return JsonResponse({"error": "Failed to scrape the Wikipedia article."}, status=500)
        # Send data to AI for verification
        ai_response = ai_request(article_text, question)
        if not ai_response:
            logger.error("AI verification failed.")
            return JsonResponse({"error": "AI verification failed."}, status=500)
        # Parse AI response
        try:
            result_summary = ai_response.get("result_summary", "No summary provided.")
            sources = {
                "url1": ai_response.get("url1", ""),
                "url2": ai_response.get("url2", ""),
                "url3": ai_response.get("url3", ""),
                "url4": ai_response.get("url4", ""),
                "url5": ai_response.get("url5", ""),
            }
            confidence_score = ai_response.get("confidence_score", 0)
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
                confidence_score=confidence_score,
                sources=sources,
            )
            return redirect("query_results", query_id=query.id)
        except Exception as e:
            logger.error(f"Failed to save query to database: {e}")
            return JsonResponse({"error": "Failed to save query to database."}, status=500)


class UserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        queries = request.user.queries.all()
        return render(request, "checker/profile.html", {"queries": queries})


class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "checker/register.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome, {self.object.username}! Your account has been created successfully.")
        return response

    def post(self, request, *args, **kwargs):
        logger.info(f"total users {CustomUser.objects.count()}")
        return super().post(request, *args, **kwargs)


class UserLoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = "checker/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        if form.cleaned_data.get("username") and form.cleaned_data.get("password"):
            user = form.get_user()  # Authenticating the user
            if user:  # Ensure the user exists
                login(self.request, user)
                logger.info(f"{user.username} logged in")
                messages.success(self.request, f"Welcome back, {user.username}!")
                return super().form_valid(form)
        messages.error(self.request, "Invalid username or password.")
        return self.form_invalid(form)


class UserLogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        logger.warning(f"{request.user.username} logged out")
        messages.success(request, f"Goodbye, {request.user.username}! You have been successfully logged out.")
        return super().get(request, *args, **kwargs)


class ErrorPage(TemplateView):
    template_name = "checker/error_page.html"


class CustomUserDeleteView(DeleteView):
    model = CustomUser
    template_name = "checker/user_confirm_delete.html"
    success_url = reverse_lazy("home")  # Redirect after successful delete

    def get_object(self, queryset=None):
        # Ensure the user can only delete their own account
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "password_form" not in context:
            context["password_form"] = PasswordConfirmationForm()
        return context


class QueryResultsView(LoginRequiredMixin, View):
    def get(self, request, query_id):
        # Receiving the request, checking that it belongs to the current user
        query = get_object_or_404(Query, id=query_id, user=request.user)
        return render(request, "checker/results.html", {"query": query})
