from myroot.languages import languages

def language_middleware(get_response):

    def middleware(request):

        request.lang = request.COOKIES.get("lang")
        if request.lang not in languages.keys():
            request.lang = "ENG"

        response = get_response(request)

        return response

    return middleware