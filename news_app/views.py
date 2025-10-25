from django.shortcuts import render, get_object_or_404
from .models import News, Category
from .forms import ContactForm
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy


def news_list(request):
    news_list = News.published.all()
    context = {
        "news_list": news_list
    }

    return render(request, "news/news_list.html", context)

# slug chiqarish uchun news av slug berilgan 
def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        "news": news
    }

    return render(request, 'news/news_detail.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:6]
        context['mahalliy_xabarlar'] =  News.published.all().filter(category__name='Mahalliy').order_by("-publish_time")[:5]
        context['xorij_xabarlar'] =  News.published.all().filter(category__name='Xorij').order_by("-publish_time")[:5]
        context['sport_xabarlar'] =  News.published.all().filter(category__name='Sport').order_by("-publish_time")[:5]
        context['texnologiya_xabarlar'] =  News.published.all().filter(category__name='Texnologiya').order_by("-publish_time")[:5]

        return context

class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langanizngiz uchun rahmat!</h2>")
        context = {
            "form": form
        }
        return render(request, 'news/contact.html', context)
    

class LocalNewsView(ListView):
    model = News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news


class ForeignNewsView(ListView):
    model = News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklari'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news


class TechnologyNewsView(ListView):
    model = News
    template_name = 'news/technology.html'
    context_object_name = 'texnologik_yangiliklari'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news


class SportNewsView(ListView):
    model = News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklari'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news
    

class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'
    slug_field = 'slug'
    slug_url_kwarg = 'news'


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')
    slug_field = 'slug'
    slug_url_kwarg = 'news'


class NewsCreateView(CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'image', 'body', 'category', 'status')