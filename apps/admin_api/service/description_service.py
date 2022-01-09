from core.handler.exceptions import ResponseHandler
from .interface import AdminServiceInterface


class AdminDescriptionService(AdminServiceInterface):
    def get_description(self, company_id: int) -> dict:
        args = company_id
        rs = self.admin_page_dao.get_one_description(args)
        return rs

    def add_description(self, company_id: int, text: str) -> dict:
        args = (company_id, text)
        try:
            rs = self.admin_page_dao.add_description(args)
        except Exception as e:
            return ResponseHandler(500).response()
        return rs

    def update_description(self, company_id: int, text: str) -> str:
        if self.get_description(company_id) == ():
            return 404
        else:
            args = (text, company_id)
            rs = self.admin_page_dao.update_description(args)
        return 200

    def delete_description(self, company_id: int) -> int:
        if self.get_description(company_id) == ():
            return 404
        else:
            self.admin_page_dao.delete_description(company_id)
            return 200
