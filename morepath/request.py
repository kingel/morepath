from werkzeug.wrappers import BaseRequest, BaseResponse

class Request(BaseRequest):
    def __init__(self, environ, populate_request=True, shallow=False):
        super(Request, self).__init__(environ, populate_request, shallow)
        self._resolver_info = None
        
    def set_resolver_info(self, info):
        self._resolver_info = info

    def resolver_info(self):
        return self._resolver_info 

class Response(BaseResponse):
    pass

    # def render(self, model, name, **predicates):
    #     predicate_lookup = IResource.component(self, model)
    #     if predicate_lookup is None:
    #         raise HttpNotFound()
    #     resource = predicate_lookup.get(get_predicates(
    #             request, model, predicates))
    #     if resource is none:
    #         raise HttpNotFound()
    #     return resource(self, model, **get_parameters(self))
    
    # def link(self, model, name):
    #     pass