from .interface import MainAfterServiceInterface


class AfterService(MainAfterServiceInterface):

    def collect_keyword(self, req) -> None:
        category = req.form.get('category')
        keyword = req.form.get('search_keyword')

        if category != None or keyword != None:
            category = 'ALL' if category == None else category
            keyword = '' if keyword == None else keyword

            args = (category, keyword)

            self.after_dao.collect_keyword(args)
