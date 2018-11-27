import datetime

class ResponseCreator:
    @staticmethod
    def create_response(status_code, body, mimetype):
        response = "HTTP/1.0 " + str(status_code) + " " + ResponseCreator.get_status_phrase(status_code) + "\r\n"
        response += "Connection: close\r\n"
        response += "Server: httpfs/1.0.0\r\n"
        response += "Date: " + datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S %Z\r\n")
        response += "Content-Type: " + mimetype + "\r\n"
        response += "Content-Length " + str(len(body.encode('utf-8'))) + "\r\n"
        response += "\r\n\r\n" + body
        return response

    @staticmethod
    def get_status_phrase(status_code):
        return {
            200: 'OK',
            201: 'CREATED',
            403: 'ACCESS FORBIDDEN',
            404: 'FILE NOT FOUND',
            409: 'CONFLICT: CANNOT OVERWRITE EXISTING FILE',
            500: 'INTERNAL SERVER ERROR'
        }.get(status_code, 'UNKNOWN')