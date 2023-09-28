class ValidatorService:

    @staticmethod
    def validate_international_phone(phone):
        response = False if phone == "" else True
        response = False if phone[0] != "+" else True
        return response

    @staticmethod
    def validate_email(email):
        response = False if email == "" else True
        response = False if "@" not in email or "." not in email else True
        return response
