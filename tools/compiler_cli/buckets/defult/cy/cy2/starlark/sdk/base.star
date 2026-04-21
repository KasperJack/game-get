def make_namespace(*entries):
    result = {}

    for entry in entries:
        name, value = entry

        if value.type != "option" and value.type != "selection":
            fail("Invalid type for %s" % name)

        result[name] = value

    return result





def ns_option(name, description, flags):
    return (name, Option(description, flags))

def ns_selection(name, description, flags):
    return (name, Selection(description, flags))




def Option(description, flags):
    if type(description) != "string":
        fail("Option: description must be a string, got " + type(description))
    if type(flags) != "list":
        fail("Option: flags must be a list, got " + type(flags))
    if len(flags) == 0:
        fail("Option: flags cannot be empty")
    for c in flags:
        if type(c) != "string":
            fail("Option: all flags must be strings, got " + type(c))

    return struct(type="option", description=description, flags=flags)


def Selection(description, flags):
    if type(description) != "string":
        fail("Selection: description must be a string, got " + type(description))
    if type(flags) != "list":
        fail("Selection: flags must be a list, got " + type(flags))
    if len(flags) == 0:
        fail("Selection: flags cannot be empty")
    for c in flags:
        if type(c) != "string":
            fail("Selection: all flags must be strings, got " + type(c))

    return struct(type="selection", description=description, flags=flags)