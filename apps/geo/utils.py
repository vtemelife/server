def get_name(obj, locale):
    if locale == "en":
        return obj.name
    names = obj.alternate_names.split(";")
    name = names[-1]
    return name or obj.name
