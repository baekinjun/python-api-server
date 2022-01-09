from .interface import MainServiceInterface


class MainStaticsService(MainServiceInterface):
    def country_statistics(self) -> dict:
        country_stat = self.main_page_dao.country_statics()
        rs = {'labels': list(map(lambda label: label['org_country_code'], country_stat)),
              'count': list(map(lambda count: count['count'], country_stat))}
        return rs

    def country_asn_count(self, country_code, asn_code):
        if country_code:
            res = self.main_page_dao.country_search_count(country_code)['count']
        elif asn_code:
            res = self.main_page_dao.asn_search_count(asn_code)['count']
        return res

    def country_info(self, **kwargs: dict) -> dict:
        args = (kwargs['country_code'], (kwargs['start_page'] * kwargs['per_page']), kwargs['per_page'])
        res_dao = self.main_page_dao.country_search(args)

        res = self.main_utils.make_list_graph(res_dao, kwargs['now'])

        return res

    def asn_statistics(self) -> dict:
        asn_stat = self.main_page_dao.asn_statics()

        rs = {'labels': list(map(lambda label: label['asn_name'], asn_stat)),
              'count': list(map(lambda count: count['count'], asn_stat))}

        return rs

    def asn_info(self, **kwargs: dict) -> dict:
        args = (kwargs['asn_name'], (kwargs['start_page'] * kwargs['per_page']), kwargs['per_page'])
        res_dao = self.main_page_dao.asn_search(args)

        res = self.main_utils.make_list_graph(res_dao, kwargs['now'])

        return res
