class Singleton(type):
    _instances = {}

    def __init__(self, name, bases, mmbs):
        super(Singleton, self).__init__(name, bases, mmbs)
        self._instances = super(Singleton, self).__call__()

    def __call__(self, *args, **kwargs):
        return self._instances
