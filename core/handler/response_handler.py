from ast import literal_eval


class ResponseHandler(Exception):
    status_code = 500

    def __init__(self, status_code=None):
        Exception.__init__(self)
        if status_code is not None:
            self.status_code = status_code

    def payload(self, payload):
        res = payload
        return res, self.status_code

    def response(self):
        return self.status_code.description, self.status_code

    def validator_response(self, error):
        res = {'error_message': None}

        res['error_message'] = literal_eval(error)
        return res, self.status_code
