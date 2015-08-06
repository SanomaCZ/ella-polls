

def get_model_name_from_class(cls):
    opts = cls._meta
    return hasattr(opts, 'model_name') and opts.model_name or opts.module_name
