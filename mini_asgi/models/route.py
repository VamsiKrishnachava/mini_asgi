import inspect
from mini_asgi.models.request import Request
from mini_asgi.models.response import Response


class Route:
    def __init__(self, method, path, func):
        self._method = method
        self._path = path
        self.func = func
        try:
            self.expectedRequestParameter = self._ExpectedRequest(func)
            self._isAsync = self._isAsync(func)
        except ValueError as e:
            raise ValueError(f"Error in route path : {path}, method {method}: {str(e)}")

    @property
    def path(self):
        return self._path

    @property
    def method(self):
        return self._method

    @property
    def isAsync(self):
        return self._isAsync
        
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


    def _isAsync(self, function):
        """ 
            This is a helper function to determine if a function is asynchronous.
        """
        if function is None:
            raise ValueError("Function is not defined correctly.")

        if not callable(function):
            raise TypeError("Expected a callable.")
        
        return inspect.iscoroutinefunction(function)