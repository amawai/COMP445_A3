from filemanager import FileManager
from urllib.parse import urlsplit
import json

REQUEST_QUERY = 1
class RequestHandler:
    def __init__(self, request_params, directory, request_body):
        self.file_manager = FileManager(directory)
        self.request_params = request_params
        self.request_body = request_body
    
    def process_get(self):
        params = self.request_params
        request_query = params[REQUEST_QUERY]
        if (request_query == '/'):
            accepted_file_types = self.get_request_parameter('Accept')
            accepted_file_types = ['json','xml','txt', 'html'] if accepted_file_types == '*/*' else [accepted_file_types]
            return self.file_manager.get_all_files_in_dir(accepted_file_types)    
        elif ('?' in request_query):
            arg_array = urlsplit(request_query).query.split('&')
            arg_dict = {}
            for arg in arg_array:
                arg_key = arg[:arg.index('=')]
                arg_value = arg[arg.index('=') + 1:]
                arg_dict[arg_key] = arg_value
            return {
                'content': json.dumps({'args': arg_dict}),
                'status': 200,
                'mimetype': 'application/json'
            }
        else:
            file_path = request_query[1:]
            return self.file_manager.get_file_content(file_path)
        
    def process_post(self):
        params = self.request_params
        request_query = params[REQUEST_QUERY]
        if ('post' in request_query):
            if ('?' in request_query):\
            arg_array = urlsplit(request_query).query.split('&')
            arg_dict = {}
            for arg in arg_array:
                arg_key = arg[:arg.index('=')]
                arg_value = arg[arg.index('=') + 1:]
                arg_dict[arg_key] = arg_value
            return {
                'content': json.dumps({"data": self.request_body, "args": arg_dict}),
                'status': 200,
                'mimetype': 'application/json'
            }
        else:
            file_path = params[REQUEST_QUERY][1:]
            overwrite = False if self.get_request_parameter('Overwrite').lower() == 'false' else True
            return self.file_manager.post_file_content(file_path, self.request_body, overwrite)
        
    def get_request_parameter(self, header):
        header_value = header + ":"
        if (header_value in self.request_params):
            return self.request_params[self.request_params.index(header_value) + 1]
        return ""