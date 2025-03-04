from django.http import HttpResponse,HttpResponseForbidden,HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout, authenticate
import json
import logging
from .models import Query, MyModel, CustomUser
from .scrapper import scrape_wikipedia
from .ai import ai_request
from rest_framework import generics
from .permissions import IsOwner, IsAdminOrReadOnly
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm,CustomAuthenticationForm,UserUpdateForm, PasswordConfirmationForm
from django.views.generic import ListView,TemplateView,DetailView,CreateView,FormView,RedirectView,UpdateView,DeleteView

logger = logging.getLogger("checker")


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

class UserRegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "checker/register.html"
    success_url = reverse_lazy("home")
    def post(self, request, *args, **kwargs):
        logger.info(f"total users {CustomUser.objects.count()}")
        return super().post(request, *args, **kwargs)

class UserLoginView(FormView):
    form_class = CustomAuthenticationForm
    template_name = "checker/login.html"
    success_url = reverse_lazy("home")

    def form_valid(self,form):
        if form.cleaned_data.get("username") and form.cleaned_data.get("password"):
            user = form.get_user()
            if user:  # Ensure the user exists
                login(self.request, user)
                logger.info(f"{user.username} logged in")
        else:
            return self.form_invalid(form)
        return super().form_valid(form)

class UserLogoutView(LoginRequiredMixin,RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        logger.warning(f"{request.user.username} logged out")
        return super().get(request, *args, **kwargs)
    





class ErrorPage(TemplateView):
    template_name = "checker/error_page.html"

class MyModelList(generics.ListAPIView):
    queryset = MyModel.objects.all()
    permission_classes = [IsAdminOrReadOnly]

class MyModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyModel.objects.all()
    permission_classes = [IsOwner]

class CustomUserDeleteView(DeleteView):
    model = CustomUser
    template_name = 'checker/user_confirm_delete.html'  # Replace with your template path
    success_url = reverse_lazy('home')  # Redirect after successful delete

    def get_object(self, queryset=None):
        # Ensure the user can only delete their own account
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'password_form' not in context:
            context['password_form'] = PasswordConfirmationForm()
        return context

    