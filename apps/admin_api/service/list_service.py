from .interface import AdminServiceInterface


class AdminListService(AdminServiceInterface):

    def get_home_list(self, start_page: int, per_page: int, search_keyword: str) -> dict:
        if search_keyword == None:
            rs = self.get_homepage(start_page, per_page)
        else:
            rs = self.get_homepage_search(start_page, per_page, search_keyword)
        return rs

    def get_homepage_search(self, start_page: int, per_page: int, search_keyword: str) -> dict:
        rs = {'home_page_list': None, 'total_count': None}

        args = ('%%' + search_keyword + '%%', (start_page * per_page), per_page)

        home_res = self.admin_page_dao.homepage_search_list(args)
        home_cnt = self.admin_page_dao.homepage_search_list_cnt('%%' + search_keyword + '%%')

        rs['home_page_list'] = home_res
        rs['total_count'] = home_cnt['total_count']
        return rs

    def get_homepage(self, start_page: int, per_page: int) -> dict:
        rs = {'home_page_list': None, 'total_count': None}

        args = ((start_page * per_page), per_page)

        home_count = self.admin_page_dao.homepage_total_count()
        home_res = self.admin_page_dao.homepage_list(args)

        rs['home_page_list'] = home_res
        rs['total_count'] = home_count['total_count']
        return rs

    def get_api_list(self, start_page: int, per_page: int, search_keyword: str) -> dict:
        if search_keyword == None:
            rs = self.get_api(start_page, per_page)
        else:
            rs = self.get_api_search(start_page, per_page, search_keyword)
        return rs

    def get_api_search(self, start_page: int, per_page: int, search_keyword: str) -> dict:
        rs = {'api_list': None, 'total_count': None}

        args = ('%%' + search_keyword + '%%', (start_page * per_page), per_page)

        api_res = self.admin_page_dao.api_search_list(args)
        api_cnt = self.admin_page_dao.api_search_list_cnt('%%' + search_keyword + '%%')

        rs['home_page_list'] = api_res
        rs['total_count'] = api_cnt['total_count']
        return rs

    def get_api(self, start_page: int, per_page: int) -> dict:
        rs = {'api_list': None, 'total_count': None}

        args = ((start_page * per_page), per_page)
        api_count = self.admin_page_dao.api_total_count()
        api_res = self.admin_page_dao.api_list(args)

        rs['api_list'] = api_res
        rs['total_count'] = api_count
        return rs

    def s_keyword_list(self, start_page: int, per_page: int) -> dict:
        res = {'keyword_list': None, 'total_count': self.admin_page_dao.search_keyword_list_cnt()['count']}

        k_res = self.admin_page_dao.search_keyword_list(((start_page * per_page), per_page))
        res['keyword_list'] = k_res
        return res

    def get_news_list(self, start_page: int, per_page: int, search_keyword: str) -> dict:
        if search_keyword != None:
            res = self.news_search_list(start_page, per_page, search_keyword)
        else:
            res = self.news_list(start_page, per_page)
        return res

    def news_search_list(self, start_page: int, per_page: int, search_keyword: str) -> dict:
        res = {'news_info': None,
               'total_count': self.admin_page_dao.news_search_count('%%' + search_keyword + '%%')['count']}

        args = ('%%' + search_keyword + '%%', (start_page * per_page), per_page)

        news_res = self.admin_page_dao.news_search_data(args)
        res['news_info'] = news_res
        return res

    def news_list(self, start_page: int, per_page: int) -> dict:
        res = {'news_info': None, 'total_count': self.admin_page_dao.news_data_cnt()['count']}
        args = ((start_page * per_page), per_page)

        news_res = self.admin_page_dao.news_data(args)
        res['news_info'] = news_res

        return res

    def delete_news_list(self, rowid: int) -> dict:
        res = self.admin_page_dao.delete_news_data(rowid)
        return res
