import inspect
import re
from mini_asgi.models.request import Request
from mini_asgi.models.response import Response


class Route:
    def __init__(self, method, path, func):
        self._method = method
        self._path = self._normalize_path(path)
        self.path_parameters = self._extract_path_parameters(path)
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

    def match_path(self, path):
        if path is None:
            return None

        if not path.startswith("/"):
            path = "/" + path

        pattern_parts = [part for part in self._path.split("/") if part]
        actual_parts = [part for part in path.split("/") if part]

        if len(pattern_parts) != len(actual_parts):
            return None

        values = {}
        for index, pattern_part in enumerate(pattern_parts):
            actual_part = actual_parts[index]
            normalized_actual_part = actual_part
            if actual_part.startswith("{") and actual_part.endswith("}"):
                normalized_actual_part = actual_part[1:-1]

            if pattern_part == "{}":
                values[self.path_parameters[len(values)]] = normalized_actual_part
            elif pattern_part != actual_part:
                return None

        return values

    def _normalize_path(self, path):
        if path is None:
            raise ValueError("Path must be provided.")
        return re.sub(r"\{[^{}]+\}", "{}", path)

    def _extract_path_parameters(self, path):
        if path is None:
            return []
        return re.findall(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}", path)

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
            if parameter.annotation == Request or parameter.name == "request":
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