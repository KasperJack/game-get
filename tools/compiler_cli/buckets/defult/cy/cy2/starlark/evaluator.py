import starlark

GLOBALS = starlark.Globals.extended_by([starlark.LibraryExtension.StructType])

def load_file(path: str) -> starlark.FrozenModule:
    path = path.lstrip("//")
    with open(path) as f:
        source = f.read()

    ast = starlark.parse(path, source, starlark.Dialect.standard())
    module = starlark.Module()
    starlark.eval(module, ast, GLOBALS)
    return module.freeze()


def evaluate(config_path: str):
    with open(config_path) as f:
        source = f.read()

    try:
        ast = starlark.parse(config_path, source, starlark.Dialect.standard())
        module = starlark.Module()
        file_loader = starlark.FileLoader(load_file)
        starlark.eval(module, ast, GLOBALS, file_loader)
        return module

    except starlark.StarlarkError as e:
        print(f"Config error:\n  {e}")
        exit(1)


if __name__ == "__main__":
    config = evaluate("namespace.star")
    print(config["libtree_namespace"])
 