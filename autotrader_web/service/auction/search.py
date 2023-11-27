from car_details.models import LotData, BidInformation, SaleInformation
from django.db.models import F, Q, Func
import random
from django.db.models import Count, Value
import datetime
from datetime import timedelta
from car_details.models import DamageType
from auction.models import AuctionCompany
import re
from random import sample


class AuctionSearchService:
    def __init__(self):
        self.text_filters = ["year", "model", "make", "bodyStyle", "locationName", "primaryDamage", "engineSize",
                             "color", "vehicleType"]
        self.custom_filters = [
            {
                "column": "odometer",
                "filter_function": self.odometer_filter
            },
            {
                "column": "newlyAddedLots",
                "filter_function": self.newly_added_lots_filter
            },
            {
                "column": "fromYear",
                "filter_function": self.from_year_filter
            },
            {
                "column": "toYear",
                "filter_function": self.to_year_filter
            },
            {
                "column": "damageType",
                "filter_function": self.damage_type_filter
            },
            {
                "column": "auctionCompany",
                "filter_function": self.auction_company_filter
            },
            {
                "column": "buyItNow",
                "filter_function": self.buy_it_now_filter
            }
        ]

    def buy_it_now_filter(self, query_set, values):
        return query_set.filter(buyItNow=1)

    def auction_company_filter(self, query_set, values):
        for value in values:
            auctionCompanyId = AuctionCompany.objects.get(Name=value).Id
            query_set = query_set.filter(auctionCompanyId=auctionCompanyId)
        return query_set

    def damage_type_filter(self, query_set, values):
        query_string = ""
        for value in values:
            query_string += f'Q (secondaryDamage__icontains="{value}") | Q(primaryDamage__icontains="{value}") |'
        query_string = query_string[0:len(query_string) - 2]
        query_set = query_set.filter(eval(query_string))
        return query_set

    def to_year_filter(self, query_set, values):
        return query_set.filter(year__lte=int(values[0]))

    def from_year_filter(self, query_set, values):
        return query_set.filter(year__gte=int(values[0]))

    def newly_added_lots_filter(self, query_set, values):
        result = query_set
        if "LAST 24 HOURS" in values:
            result = query_set.filter(dateCreated__gte=datetime.datetime.now() - timedelta(hours=24))
        if "LAST 7 DAYS" in values:
            result = query_set.filter(dateCreated__gte=datetime.datetime.now() - timedelta(days=7))
        if "ALL" in values:
            return query_set
        return result

    def odometer_filter(self, query_set, values):
        odometer_query = ""

        for value in values:
            if value == "LESS THAN 25,000":
                odometer_query += "Q(odometer__lte=25000) |"
            elif value == "25,001 TO 50,000":
                odometer_query += "Q(odometer__gte=25001, odometer__lte=50000) |"
            elif value == "50,001 TO 100,000":
                odometer_query += "Q(odometer__gte=50001, odometer__lte=100000) |"
            elif value == "100,001 TO 150,000":
                odometer_query += "Q(odometer__gte=100001, odometer__lte=150000) |"
            elif value == "150,000 TO 200,000":
                odometer_query += "Q(odometer__gte=150001, odometer__lte=200000) |"
            elif value == "Greater THAN 200,000":
                odometer_query += "Q(odometer__gte=200000) |"

        if "Q" in odometer_query:
            odometer_query = odometer_query[0:len(odometer_query) - 2]
            query_set = query_set.filter(eval(odometer_query))
        return query_set

    def apply_custom_filters(self, query_set, filters):
        for f in self.custom_filters:
            if f.get("column") in filters.keys():
                values = filters.getlist(f.get("column"))
                query_set = f.get("filter_function")(query_set, values)

        return query_set

    def search_lots_by_text(self, x):
        lot_data = LotData.objects.all()
        for text in x.split(" "):
            temp = lot_data.filter(
                Q(searchTerm__icontains=text) | Q(id__contains=text) | Q(lotId__icontains=text) | Q(
                    model__icontains=text) | Q(make__icontains=text))
            lot_data = temp

        return lot_data

    def apply_text_filters(self, query_set, filters):
        for input_filter in filters.keys():
            if input_filter in self.text_filters:
                query = ""
                for prop in filters.getlist(input_filter):
                    query += f'Q({input_filter}__icontains="{prop}") | '
                query = query[0:(len(query) - 2)]
                query_set = query_set.filter(eval(query))
        return query_set

    def search_lots(self, query_dict):
        results = self.search_lots_by_text(query_dict.get("q"))
        results = self.apply_text_filters(results, query_dict)
        results = self.apply_custom_filters(results, query_dict)
        results = results.order_by(F('saledate').asc(nulls_last=True))
        return results

    def get_page_from_search_results(self, results, page=1):
        sliced_results = []
        for i in range((page - 1) * 20, page * 20):
            if i < len(results):
                sliced_results.append(results[i])
        return sliced_results

    def get_active_filters(self, query_dict):
        active_filters = []
        for i in query_dict:
            if i in self.text_filters:
                for x in query_dict.getlist(i):
                    active_filters.append(x.upper())
        for i in self.custom_filters:
            if i.get("column") in query_dict.keys() and i.get("column") != "buyItNow":
                for x in query_dict.getlist(i.get("column")):
                    fil = x.upper()
                    if i.get("column") == "fromYear":
                        fil = "From Year: " + fil
                    if i.get("column") == "toYear":
                        fil = "To Year: " + fil
                    active_filters.append(fil)

        return active_filters

    def get_search_filters(self, search_results, active_filters, lang):

        def newly_added_lots_get(query_set, column):
            result = [
                {"total": len(query_set), "value": "ALL"},
                {"total": len(query_set.filter(dateCreated__gte=datetime.datetime.now() - timedelta(hours=24))),
                 "value": "LAST 24 HOURS"},
                {"total": len(query_set.filter(dateCreated__gte=datetime.datetime.now() - timedelta(days=7))),
                 "value": "LAST 7 DAYS"},
            ]
            for x in result:
                x["active"] = True if x.get("value") in active_filters else False
            return result

        def damage_type_get(query_set, column):
            result = []
            for x in DamageType.objects.all().order_by('Priority'):
                result.append({"total": len(
                    LotData.objects.filter(Q(secondaryDamage__icontains=x.Name) | Q(primaryDamage__icontains=x.Name))),
                               "value": x.Name})
            return result

        def odometer_get(query_set, column):
            result = [
                {"total": len(query_set.filter(odometer__lte=25000)), "value": "LESS THAN 25,000"},
                {"total": len(query_set.filter(odometer__gte=25001, odometer__lte=50000)), "value": "25,001 TO 50,000"},
                {"total": len(query_set.filter(odometer__gte=50001, odometer__lte=150000)),
                 "value": "50,001 TO 100,000"},
                {"total": len(query_set.filter(odometer__gte=100001, odometer__lte=150000)),
                 "value": "100,001 TO 150,000"},
                {"total": len(query_set.filter(odometer__gte=150000, odometer__lte=200000)),
                 "value": "150,000 TO 200,000"},
                {"total": len(query_set.filter(odometer__gte=200000)), "value": "GREATER THAN 200,000"},
            ]
            final = []
            for x in result:
                x["active"] = True if x.get("value").upper() in active_filters else False
                if x.get("total") > 0:
                    final.append(x)
            return final

        class EndNumeric(Func):
            function = 'REGEXP_MATCHES'
            template = "(\d\.(\d|\d\d))"

        def engine_size_get(queryset, column):
            result = []
            filters = queryset.values(column).annotate(total=Count(column))

            for i in filters:
                if i.get(column) is not None:
                    temp = {
                        "total": i.get("total"),
                        "active": False if str(i.get(column)).upper() not in active_filters else True,
                        "value": str(i.get(column)).upper()
                    }

                    try:
                        temp["value"] = re.search("(\d\.(\d|\d\d))", temp["value"])[0]
                    except:
                        temp["value"] = temp["value"][0:4]

                    if temp["value"] not in [value.get("value") for value in result]:
                        result.append(temp)
                    else:
                        for r in result:
                            if r["value"] == temp["value"]:
                                r["total"] += 1

            return result

        def default_get(queryset, column):
            result = []
            filters = queryset.values(column).annotate(total=Count(column))
            if column == "year":
                filters = filters.order_by("-year")
            else:
                filters = filters.order_by(column)

            for i in filters:
                if i.get(column) is not None:
                    temp = {
                        "total": i.get("total"),
                        "active": False if str(i.get(column)).upper() not in active_filters else True,
                        "value": str(i.get(column)).upper()
                    }

                    if temp["value"] not in [value.get("value") for value in result]:
                        result.append(temp)

            return result

        def auction_company_get(query_set, column):
            auction_companies = []
            for x in query_set.raw("SELECT 1 as id, ld.auctionCompanyId, COUNT(*) AS total FROM LotData ld GROUP BY ld.auctionCompanyId"):
                auction_name = AuctionCompany.objects.get(Id=x.auctionCompanyId).Name
                auction_companies.append({
                    "total": x.total,
                    "value": auction_name,
                    "active": False if auction_name.upper() not in active_filters else True
                })
            return auction_companies

        filters_input = [
            {"name": "Newly Added Lots", "column": "newlyAddedLots", "function": newly_added_lots_get},
            {"name": "Make", "column": "make", "function": default_get},
            {"name": "Model", "column": "model", "function": default_get},
            {"name": "Location", "column": "locationName", "function": default_get},
            {"name": "Body Style", "column": "bodyStyle", "function": default_get},
            {"name": "Vehicle Type", "column": "vehicleType", "function": default_get},
            {"name": "Color", "column": "color", "function": default_get},
            {"name": "Engine", "column": "engineSize", "function": engine_size_get},
            {"name": "Primary Damage", "column": "primaryDamage", "function": default_get},
            {"name": "Year", "column": "year", "function": default_get},
            {"name": "Odometer", "column": "odometer", "function": odometer_get},
            {"name": "Damage Type", "column": "damageType", "function": damage_type_get},
            {"name": "Auction Company", "column": "auctionCompany", "function": auction_company_get}
        ]

        filters = []
        i = 0
        for input_filter in filters_input:
            i += 1
            data = input_filter.get("function")(search_results, input_filter.get("column"))
            for x in data:
                if x.get("value") in lang and lang.get(x.get("value")) is not None:
                    x["value"] = lang.get(x.get("value"))
            if input_filter.get("name") != "Year":
                data = sorted(data, key=lambda x: x["value"])
            filters.append({"id": i, "data": data, "name": input_filter.get("name"), "column": input_filter.get("column")})

        return filters

    def get_popular_lots(self):
        popular_lots_filters_names = ['id', "saledate", "year", "model", "make", "secondaryDamage", "primaryDamage", 'imageFull']
        current_year = datetime.datetime.now().year

        # Create an array for the last 7 years
        last_7_years = [str(current_year - i) for i in range(7)]
        last_7_years = [int(i) for i in last_7_years]

        popular_lots_filters = [
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "BMW", "model__icontains": "528", "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "BMW", "model__icontains": "530", "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "BMW", "model__icontains": "328", "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "BMW", "model__icontains": "330",
             "year__in": last_7_years, "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "Hydai", "model__icontains": "elantra", "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "chevrolet", "model__icontains": "cruze", "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "toyota", "model__icontains": "prius", "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "mercedes", "model__icontains": "e 300", "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "kia", "model__icontains": "optima",
             "year__in": last_7_years, "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "chevrolet", "model__icontains": "malibu",
             "year__in": last_7_years, "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "hyundai", "model__icontains": "accent",
             "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "kia", "model__icontains": "forte",
             "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "toyota", "model__icontains": "camry",
             "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
            {"saledate__gte": datetime.datetime.now(), "saledate__lte": datetime.datetime.now() + timedelta(days=3),
             "make__icontains": "toyota", "model__icontains": "corolla",
             "year__in": last_7_years,
             "secondaryDamage": "Minor Dent/Scratches",
             "primaryDamage": "Rear end"},
        ]

        query_filters = Q()
        for filter_set in popular_lots_filters:
            query_filters |= Q(**filter_set)

        # Apply the combined filter to your model
        filtered_data = LotData.objects.filter(query_filters)

        # Get 5 random records from the filtered data
        random_lots = sample(list(filtered_data), min(5, filtered_data.count()))
        # lots = LotData.objects.all()
        # for filter_name in popular_lots_filters_names:
        #     for input_filter in popular_lots_filters:
        #         apply_filter = {}
        #         for k in input_filter.keys():
        #             if filter_name in k:
        #                 apply_filter[k] = input_filter[k]
        #         if filter_name == "year":
        #             year_query = ""
        #             for year in input_filter["year"]:
        #                 year_query += f"Q(year__contains={year}) | "
        #             year_query = year_query[0:(len(year_query) - 2)]
        #             new_lots = lots.filter(eval(year_query))
        #         else:
        #             new_lots = lots.filter(**apply_filter)
        #         if len(new_lots) >= 5:
        #             lots = new_lots
        # lots = [l for l in lots]
        # lots.extend((LotData.objects.filter(fuel__icontains="hybrid", saledate__gte=datetime.datetime.now(),
        #                                     saledate__lte=datetime.datetime.now() + timedelta(days=3))))

        new_random_lots = []
        for x in range(len(random_lots)):
            try:
                choosen_car = random_lots[x]
                details = {}
                details = SaleInformation.objects.filter(LotId = choosen_car)[0].__dict__
                details['BidInformation'] = BidInformation.objects.filter(LotId = choosen_car)[0].__dict__
                choosen_car.details = details
                new_random_lots.append(choosen_car.__dict__)
                # random_lots.pop(index)
            except Exception as e:
                pass

        return new_random_lots
