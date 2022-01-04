class RouteError(Exception):
    '''
    This Exception is used to identify Route Errors and handle them.
    '''
    @property
    def message(self):
        return self.args[0]
    
    @property
    def status_code(self):
        return self.args[1]