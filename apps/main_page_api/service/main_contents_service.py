from datetime import datetime, timedelta
from .interface import MainServiceInterface


class MainContentsService(MainServiceInterface):
    def type_search(self, **kwargs) -> dict:
        category, search_keyword = kwargs['category'], kwargs['search_keyword']
        if category != None and search_keyword != None:
            res_dao = self.both_search(kwargs)
        elif category != None and search_keyword == None:
            res_dao = self.category_search(kwargs)
        elif search_keyword != None and category == None:
            res_dao = self.keyword_search(kwargs)
        else:
            res_dao = self.total_search(kwargs)
        res = self.main_utils.make_list_graph(res_dao, kwargs['now'])

        return res

    def type_search_count(self, **kwargs) -> dict:
        category, search_keyword = kwargs['category'], kwargs['search_keyword']

        if category != None and search_keyword != None:
            res = self.both_total(kwargs)["count"]
        elif category != None and search_keyword == None:
            res = self.category_count(kwargs)["COUNT(*)"]
        elif search_keyword != None and category == None:
            res = self.keyword_count(kwargs)["count"]
        else:
            res = self.total_count()["COUNT(*)"]

        if res == None:
            res = 0

        return res

    def both_search(self, kwargs: dict) -> dict:
        args = (
            '%%' + kwargs['search_keyword'] + '%%', '%%' + kwargs['search_keyword'] + '%%',
            '%%' + kwargs['search_keyword'] + '%%', kwargs['category'], (kwargs['start_page'] * kwargs['per_page']),
            kwargs['per_page'])

        product = self.main_page_dao.keyword_category_search(args)
        return product

    def both_total(self, kwargs: dict) -> dict:
        t_args = (
            '%%' + kwargs['search_keyword'] + '%%', '%%' + kwargs['search_keyword'] + '%%',
            '%%' + kwargs['search_keyword'] + '%%', kwargs['category'])
        count = self.main_page_dao.keyword_category_search_count(t_args)

        return count

    def keyword_search(self, kwargs: dict) -> dict:
        args = (
            '%%' + kwargs['search_keyword'] + '%%', '%%' + kwargs['search_keyword'] + '%%',
            '%%' + kwargs['search_keyword'] + '%%', (kwargs['start_page'] * kwargs['per_page']), kwargs['per_page'])
        product = self.main_page_dao.keyword_search(args)
        return product

    def keyword_count(self, kwargs: dict) -> dict:
        t_args = (
            '%%' + kwargs['search_keyword'] + '%%', '%%' + kwargs['search_keyword'] + '%%',
            '%%' + kwargs['search_keyword'] + '%%')

        count = self.main_page_dao.keyword_search_count(t_args)
        return count

    def category_search(self, kwargs: dict) -> dict:
        args = (kwargs['category'], (kwargs['start_page'] * kwargs['per_page']), kwargs['per_page'])
        product = self.main_page_dao.category_search(args)
        return product

    def category_count(self, kwargs: dict) -> dict:
        count = self.main_page_dao.category_search_count(kwargs['category'])
        return count

    def total_search(self, kwargs: dict) -> dict:
        args = ((kwargs['start_page'] * kwargs['per_page']), kwargs['per_page'])
        product = self.main_page_dao.total_search(args)
        return product

    def total_count(self) -> dict:
        count = self.main_page_dao.total_search_count()
        return count

    def total_pid(self) -> dict:

        res = {'total': self.total_count()["COUNT(*)"],
               'product_id': list(map(lambda pid: pid['product_id'], self.main_page_dao.total_pid()))}

        return res

    def category_list(self) -> list:
        cate_list = self.main_page_dao.category_list()
        res = (list(map(lambda cate: cate['category'], cate_list)))

        return res

    def popular_keyword(self, now: str) -> dict:
        month_date = datetime.strptime(now[0:10], '%Y-%m-%d') - timedelta(days=30)
        rs = self.main_page_dao.popular_keyword(month_date)

        return rs
