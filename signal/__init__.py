class Signal(): #Subclass this, you fool
    pass

class MetaSignal(type): #More than a MetaSignal
    def __new__(cls, action, arg_names=list(), arg_types=list(), *, parent=Signal):
        #Defining the class. I love this shit
        def __init__(obj, *args, **kwargs):
            parent.__init__(obj)
            assert len(arg_names)==len(args)
            for index, item in enumerate(args):
                assert isinstance(item, arg_types[index])
            obj._args = args
        def __getattr__(obj, key):
            if key in obj.arg_names:
                return obj.args[obj.arg_names.index(key)]
            else:
                raise AttributeError()
        dct = dict()
        dct["__init__"] = __init__
        dct["__getattr__"] = __getattr__
        dct["args"] = property(lambda self: self._args)
        dct["action"] = property(lambda self: self.__class__.__name__.lower())
        dct["bytearray"] = property(lambda self:
                bytearray(
                        "{}:\n".format(action.lower())+"\n".join([str(arg) for arg in self.args]),
                        "utf-8"
                        )
               ) #To virtualGPIO
        return type.__new__(cls, action, (parent, ), dct)

    def __init__(cls, action, arg_names=list(), arg_types=list(), *, parent=Signal):
        type.__init__(cls, action, (parent, ), {})
        try:
            assert len(arg_names)==len(arg_types)
        except:
            raise
        cls.arg_names = arg_names
        cls.arg_types = arg_types
        cls.action = action.lower()
