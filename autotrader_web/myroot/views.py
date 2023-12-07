from django.views.generic.base import TemplateView
from car_details.models import LotData
from django.db.models import Count
from rest_framework.response import Response
from auction.models import *
from rest_framework.views import APIView
from rest_framework import status
from myroot.languages import languages
from django.shortcuts import render
from myroot.models import OrderNow as OrderNowModel
from django.conf import settings
from service.auction.calculator import AuctionCalculatorService
from service.validator import ValidatorService
from service.recaptcha import RecaptchaService
from service.auction.search import AuctionSearchService
from car_details.models import KoreanLot

class HomeView(TemplateView):
    template_name = 'auction/home.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        response = render(request, self.template_name, context)
        return response

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context["lang"] = languages[self.request.lang]
        print(self.request.lang)

        context["allMakes"] = LotData.objects.values("make").annotate(total=Count('make')).order_by('make')
        context["allModels"] = LotData.objects.raw("""SELECT DISTINCT a.model, b.make, 1 AS id
                                                        FROM (
                                                            SELECT model, COUNT('model') AS total
                                                            FROM LotData
                                                            GROUP BY model
                                                        ) a
                                                        INNER JOIN (
                                                            SELECT model, make
                                                            FROM LotData
                                                        ) b ON a.model = b.model;""")
        context["allLocations"] = LotData.objects.values("locationName").annotate(total=Count('locationName'))
        context["allYears"] = LotData.objects.values("year").annotate(total=Count('year')).order_by('-year')
        context["popularMakes"] = LotData.objects.values("make").annotate(total=Count('model')).order_by('total').order_by('make')
        context["vehicleTypes"] = LotData.objects.values("vehicleType").annotate(total=Count('vehicleType'))
        context["bodyStyles"] = LotData.objects.values("bodyStyle").annotate(total=Count('bodyStyle'))
        context["primaryDamage"] = LotData.objects.values("primaryDamage").annotate(total=Count('primaryDamage'))
        context["cities"] = Cities.objects.filter(Country="US")
        context["auctions"] = AuctionCompany.objects.all()
        auction_lots_service = AuctionSearchService()
        context["cars"] = auction_lots_service.get_popular_lots()

        for bodyStyle in context["bodyStyles"]:
            if bodyStyle.get('bodyStyle') in context["lang"]:
                bodyStyle['bodyStyle'] = context["lang"][bodyStyle.get('bodyStyle')]

        for primaryDamage in context["primaryDamage"]:
            if primaryDamage.get('primaryDamage') in context["lang"]:
                primaryDamage['primaryDamage'] = context["lang"][primaryDamage.get('primaryDamage')]

        context["bodyStyles"] = context["bodyStyles"].order_by('bodyStyle')
        context["primaryDamage"] = context["primaryDamage"].order_by('primaryDamage')

        cars_with_count = []
        for car in range(len(context["cars"])):
            cars_with_count.append({"count": car, "details": context["cars"][car]})
        context["cars"] = cars_with_count

        return context


class AdminCalculatorView(TemplateView):
    template_name = 'admin-calculator.html'


class OrderNow(APIView):

    def post(self, request):

        try:
            token = request.data["token"] if "token" in request.data.keys() else None

            recaptcha_service = RecaptchaService(settings.RECAPTCHA_SECRET)
            token_verified = recaptcha_service.verify_token(token=token)

            if token_verified:
                phone = request.data["phone"] if "phone" in request.data.keys() else None
                email = request.data["email"] if "email" in request.data.keys() else None
                message = request.data["message"] if "message" in request.data.keys() else None
                lotid = request.data["lotid"] if "lotid" in request.data.keys() else None
                first_name = request.data["first_name"] if "first_name" in request.data.keys() else None
                last_name = request.data["last_name"] if "last_name" in request.data.keys() else None

                if ValidatorService.validate_email(email) or ValidatorService.validate_international_phone(phone):
                    data = OrderNowModel(FirstName=first_name,LastName=last_name,Phone=phone,Email=email, Message=message, LotId=lotid)
                    data.save()
                    return Response({},status=status.HTTP_200_OK)
                else:
                    return Response({},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e, request.data)
            return Response({}, status=status.HTTP_200_OK)


class GetCity(APIView):

    def get(self, request):
        try:
            location_id = request.GET.get("location")
            city = Cities.objects.get(Id=location_id)
            return Response({
                "country": city.Country,
                "city": city.Name,
                "state": city.State,
                "port": city.Port
            })
        except Exception as e:
            return Response({"country": "", "city": "", "state": "", "port": ""})

class Calculator(APIView):

    def get(self, request):
        lot_id = request.GET.get("lot_id")
        to_country = request.GET.get("to_country")
        bid = request.GET.get("bid")
        auction_calculator = AuctionCalculatorService()
        auction_calculator.calculate_by_lotid(lot_id, bid, to_country)
        response = auction_calculator.json()
        return Response(response)

class KoreanListView(TemplateView):
    template_name = 'auction/korean-list.html'

    def get(self, request):
        context = self.get_context_data()
        context["lang"] = languages[request.lang]
        context["korean_lots"] = KoreanLot.objects.all()
        response = render(request, self.template_name, context)
        return response
