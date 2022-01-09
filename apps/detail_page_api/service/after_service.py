from .interface import DetailAfterServiceInterface


class AfterService(DetailAfterServiceInterface):

    def up_view_cnt(self, req) -> None:
        company_id = req.args.get('company_id')
        res = self.after_dao.up_view_cnt(int(company_id))
        return res
