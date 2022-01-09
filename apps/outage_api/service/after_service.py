from .interface import OutageAfterServiceInterface


class AfterService(OutageAfterServiceInterface):

    def up_view_cnt(self, req):
        company_id = req.args.get('company_id')

        res = self.after_dao.up_view_cnt(company_id)
        return res
