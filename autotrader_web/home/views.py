from django.shortcuts import render
from django.views.generic.base import TemplateView
from myroot.languages import languages
from car_details.models import *
import math
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from myroot.models import Message, Setting, Gallery, About, Faq, Partner, Service, Team, Testimonial, SocialMedia, \
    SocialMediaAccounts, Blog
from auction.models import *
from django.conf import settings
from service.recaptcha import RecaptchaService
from service.auction.calculator import AuctionCalculatorService


def extract_useful_data_from_cars(cars, lang):
    res = []

    lang_keys = {
        "ENG": {
            "brand": "Brand[0].NameEn",
            "model": "Model[0].NameEn",
            "fuel": "Fuel[0].NameEn",
            "speedbox": "SpeedBox[0].NameEn",
            "bantype": "BanType[0].NameEn",
            "color": "Color[0].NameEn",
            "status": "Status[0].NameEn",
        },
        "RUS": {
            "brand": "Brand[0].NameRu",
            "model": "Model[0].NameRu",
            "fuel": "Fuel[0].NameRu",
            "speedbox": "SpeedBox[0].NameRu",
            "bantype": "BanType[0].NameRu",
            "color": "Color[0].NameRu",
            "status": "Status[0].NameRu",
        },
        "AZE": {
            "brand": "Brand[0].NameAz",
            "model": "Model[0].NameAz",
            "fuel": "Fuel[0].NameAz",
            "speedbox": "SpeedBox[0].NameAz",
            "bantype": "BanType[0].NameAz",
            "color": "Color[0].NameAz",
            "status": "Status[0].NameAz",
        }
    }

    for car in cars:
        try:
            brand = eval("car." + lang_keys[lang]["brand"])
        except:
            brand = ""
        try:
            model = eval("car." + lang_keys[lang]["model"])
        except:
            model = ""
        try:
            fuel = eval("car." + lang_keys[lang]["fuel"])
        except:
            fuel = ""
        try:
            speedbox = eval("car." + lang_keys[lang]["speedbox"])
        except:
            speedbox = ""
        try:
            bantype = eval("car." + lang_keys[lang]["bantype"])
        except:
            bantype = ""
        try:
            color = eval("car." + lang_keys[lang]["color"])
        except:
            color = ""
        try:
            status = eval("car." + lang_keys[lang]["status"])
        except:
            status = ""

        imgs = []

        for img in car.CarImage:
            imgs.append({
                "src": img.MainImage
            })

        res.append({
            "imgs": imgs,
            "brand": brand,
            "model": model,
            "id": car.Id,
            "img": car.MainImage,
            "fuel": fuel,
            "year": car.Year,
            "speedbox": speedbox,
            "distance": car.Distance,
            "bantype": bantype,
            "color": color,
            "price": car.Price,
            "location": car.Location,
            "price_with_sale": car.PriceWithSale,
            "currency_symbol": car.Currency.Symbol,
            "status": status
        })

    return res


class CalculatorView(TemplateView):
    template_name = 'home/calculator-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["lang"] = languages[request.lang]
        context["settings"] = Setting.objects.all()[0]
        context["current_lang"] = request.lang
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        context["about"] = About.objects.all()[0]
        context["cities"] = Cities.objects.all()
        context["auctions"] = AuctionCompany.objects.all()
        response = render(request, self.template_name, context)

        return response


class HomeCalculator(APIView):

    def get(self, request):
        auction_id = self.request.GET["auction"]
        price = self.request.GET["price"]
        city = self.request.GET["city"]
        auction_calculator_service = AuctionCalculatorService()
        auction_calculator_service.calculate(auction_id, price, city)
        response = auction_calculator_service.json()
        return Response(response)


class GalleryView(TemplateView):
    template_name = 'home/gallery-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context["lang"] = languages[request.lang]
        context["gallery"] = Gallery.objects.all()
        context["current_lang"] = request.lang
        context["settings"] = Setting.objects.all()[0]
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        context["about"] = About.objects.all()[0]
        response = render(request, self.template_name, context)

        return response


class AboutView(TemplateView):
    template_name = 'home/about-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context["lang"] = languages[request.lang]

        context["about"] = About.objects.all()[0]
        context["current_lang"] = request.lang
        context["partners"] = Partner.objects.all()
        context["faqs"] = Faq.objects.all()
        context["settings"] = Setting.objects.all()[0]
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        response = render(request, self.template_name, context)

        return response


class ContactView(TemplateView):
    template_name = 'home/contact-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        context["lang"] = languages[request.lang]
        context["settings"] = Setting.objects.all()[0]
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        context["current_lang"] = request.lang
        context["about"] = About.objects.all()[0]

        response = render(request, self.template_name, context)

        return response


class AboutServicesView(TemplateView):
    template_name = 'home/about-services-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["settings"] = Setting.objects.all()[0]
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        context["current_lang"] = request.lang
        context["about"] = About.objects.all()[0]
        context["lang"] = languages[request.lang]
        context["services"] = Service.objects.all()
        response = render(request, self.template_name, context)

        return response


class TeamView(TemplateView):
    template_name = 'home/team-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["lang"] = languages[request.lang]
        context["settings"] = Setting.objects.all()[0]
        context["current_lang"] = request.lang
        context["about"] = About.objects.all()[0]
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        context["teams"] = Team.objects.all()
        response = render(request, self.template_name, context)

        return response


class TeamDetailsView(TemplateView):
    template_name = 'home/team-details-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["lang"] = languages[request.lang]
        context["current_lang"] = request.lang
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        context["about"] = About.objects.all()[0]
        member_id = self.kwargs["member_id"]
        context["team"] = Team.objects.get(Id=member_id)
        context["settings"] = Setting.objects.all()[0]
        context["recent_cars"] = extract_useful_data_from_cars(Car.objects.all()[0:4], lang)
        response = render(request, self.template_name, context)

        return response


class BlogView(TemplateView):
    template_name = 'home/blog-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["lang"] = languages[request.lang]
        context["current_lang"] = request.lang
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        context["about"] = About.objects.all()[0]
        context["blog"] = Blog.objects.all()
        context["settings"] = Setting.objects.all()[0]

        response = render(request, self.template_name, context)

        return response


class BlogDetailsView(TemplateView):
    template_name = 'home/blog-details-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["lang"] = languages[request.lang]
        context["recent_cars"] = extract_useful_data_from_cars(Car.objects.all()[0:4], request.lang)
        context["current_lang"] = request.lang
        context["recent_blogs"] = Blog.objects.all()[0:4]
        context["settings"] = Setting.objects.all()[0]
        context["about"] = About.objects.all()[0]
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        blog_id = self.kwargs["postid"]

        current_blog = Blog.objects.get(Id=blog_id)
        Blog.objects.filter(Id=blog_id).update(Count=current_blog.Count + 1)

        context["blog"] = current_blog
        response = render(request, self.template_name, context)

        return response


class CarsView(TemplateView):
    template_name = 'home/cars-page.html'

    def get_left_right_buttons(self, total_pages, current_page):
        try:
            left = None
            right = None
            if current_page - 1 >= 1:
                left = current_page - 1
            if current_page + 1 <= total_pages:
                right = current_page + 1
            return {"left": left, "right": right}
        except:
            return []

    def get_page_buttons(self, total_pages, current_page):
        try:
            pages = []
            base_url = "/cars?"

            for fil in self.request.GET.keys():
                if fil != "page":
                    base_url += fil + "=" + self.request.GET[fil] + "&"

            current_index = current_page - 1
            for page in range(1, total_pages + 1):
                pages.append({
                    "page": str(page),
                    "url": (base_url + "page=" + str(page))
                })
            final_pages = []
            if current_index - 1 >= 0:
                final_pages.append(pages[current_index - 1])
            final_pages.append(pages[current_index])
            if current_index + 1 < len(pages):
                final_pages.append(pages[current_index + 1])

            return final_pages
        except:
            return []

    def get(self, request, *args, **kwargs):
        try:
            if self.request.GET["view"] == "grid":
                self.template_name = "home/cars-page-grid.html"
        except:
            pass

        context = self.get_context_data()
        cars = Car.objects.all()

        context["lang"] = languages[request.lang]

        if "page" not in request.GET.keys():
            page = 1
        else:
            page = int(request.GET["page"])

        filters = [
            {"name": "model", "model": "ModelId"},
            {"name": "year", "model": "Year"},
            {"name": "bantype", "model": "BanTypeId"},
            {"name": "speedbox", "model": "SpeedBoxId"},
            {"name": "brand", "model": "BrandId"},
        ]

        for fil in filters:
            if fil["name"] in self.request.GET.keys():
                key = fil["model"]
                value = self.request.GET[fil["name"]]
                filt = {key: value}
                cars = cars.filter(**filt)

        total_pages = math.ceil(cars.count() / 20)
        context["pages"] = self.get_page_buttons(total_pages, page)
        context["left_right_btns"] = self.get_left_right_buttons(total_pages, page)
        context["current_page"] = str(page)
        context["brands"] = Brand.objects.all()
        context["years"] = Car.objects.values('Year').annotate()
        context["models"] = Model.objects.all()
        context["bantype"] = BanType.objects.all()
        context["speedbox"] = SpeedBox.objects.all()
        context["current_lang"] = request.lang
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        context["recent_blogs"] = Blog.objects.all()[0:4]
        context["settings"] = Setting.objects.all()[0]
        context["about"] = About.objects.all()[0]
        cars = cars[((page - 1) * 20):((page * 20) - 1)]

        context["cars"] = extract_useful_data_from_cars(cars, request.lang)
        response = render(request, self.template_name, context)

        return response


class CarsDetailsView(TemplateView):
    template_name = 'home/cars-details-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["lang"] = languages[request.lang]
        context["current_lang"] = request.lang
        context["about"] = About.objects.all()[0]
        context["car"] = extract_useful_data_from_cars(Car.objects.filter(Id=self.kwargs["lotid"]), request.lang)[0]
        context["related_cars"] = extract_useful_data_from_cars(Car.objects.all()[1:4], request.lang)
        context["settings"] = Setting.objects.all()[0]
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()

        response = render(request, self.template_name, context)

        return response


class HomePageView(TemplateView):
    template_name = 'home/home-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["lang"] = languages[request.lang]
        cars = Car.objects.all()[0:10]
        cars = extract_useful_data_from_cars(cars, request.lang)
        context["cars"] = cars
        context["services"] = Service.objects.all()[0:4]
        context["current_lang"] = request.lang
        context["team"] = Team.objects.all()[0:4]
        context["testimonial"] = Testimonial.objects.all()[0]
        context["settings"] = Setting.objects.all()[0]
        context["partners"] = Partner.objects.all()
        context["blog"] = Blog.objects.all()[0:4]
        context["about"] = About.objects.all()[0]
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        response = render(request, self.template_name, context)

        return response


class ShopPageView(TemplateView):
    template_name = 'home/shop-page.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context["lang"] = languages[request.lang]
        context["about"] = About.objects.all()[0]
        context["social_media_accounts"] = SocialMediaAccounts.objects.all()
        context["current_lang"] = request.lang
        context["settings"] = Setting.objects.all()[0]
        response = render(request, self.template_name, context)
        return response


class PostMessage(APIView):

    def post(self, request):
        data = request.data

        recaptcha_service = RecaptchaService(settings.RECAPTCHA_SECRET)
        token_verified = recaptcha_service.verify_token(token=data['token'])

        if not token_verified:
            res = False
        else:
            res = True
            date = datetime.datetime.now()
            name = data["fullname"]
            contact = data["contact"]
            msg = data["message"]
            subject = data["subject"]
            model = Message(FullName=name, Subject=subject, Phone=contact, Email=contact, Content=msg, AddDate=date)
            model.save()

        return Response({
            "success": res
        })
