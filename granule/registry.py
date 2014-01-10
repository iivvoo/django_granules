class Registry(object):
    """ Simple registry, allows registry to be replaced in-place.
        Taken from wheelcms_axle.registry.py
    """
    def __init__(self, wrapped):
        self.wrapped = wrapped

    def set(self, wrapped):
        self.wrapped = wrapped

    #def __getattr__(self, k):
    #    return getattr(self.wrapped, k)
    def __iter__(self):
        return self.wrapped.__iter__()

    def __getattr__(self, name):
        return getattr(self.wrapped, name)

class GranulesRegistry(dict):
    def register(self, name, template, priority=100):
        if name not in self:
            self[name] = []
        self[name].append((priority, template))

granules_registry = Registry(GranulesRegistry())
