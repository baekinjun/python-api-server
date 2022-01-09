from apps.login_api.repository import LoginApiDao


class LoginApiService:
    def __init__(self):
        self.login_api_dao = LoginApiDao()

    def duplication_check(self, email: str, types: str) -> bool:
        if self.login_api_dao.check_email((email, types)) == ():
            return False

        return True

    def find_email_in_db(self, email: str, types: str) -> bool:
        if self.login_api_dao.check_email((email, types)) == ():
            return True

        return False

    def sign_up(self, **kwargs):
        res = self.login_api_dao.sign_up(**kwargs)
        return res
