import inspect
from mini_asgi.models.request import Request


class Route:
    def __init__(self, method, path, func):
        self.method = method
        self.path = path
        self.func = func
        try:
            self.expectedRequestParameter = self._ExpectedRequest(func)
        except ValueError as e:
            raise ValueError(f"Error in route path : {path}, method {method}: {str(e)}")
        
    def _ExpectedRequest(self, function):
        """
        Helper method to check if the function expects only one parameter of type Request.
        """
        functionParameters = inspect.signature(function).parameters
        returnParameter = None
        for parameter in functionParameters.values():
            if parameter.annotation == Request:
                if returnParameter is None:
                    returnParameter = parameter
                else:
                    raise ValueError("Function should not have more than one parameter of type Request.")
        return returnParameter