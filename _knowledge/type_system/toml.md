# TOML

TOML was the first manifest format for Pact. The schema looked promising — nested keys mapped naturally to the contract system Pact was built around:

```toml
[interface.compiler.backend]
flags = ["gcc", "llvm"]
default = "gcc"

[interface.channel.stability]
keys = ["stable", "dev"]
default = "stable"
```

## Why it broke down

**Validation was a nightmare.** TOML in Python loads into plain dicts. The moment you have nested structures with semantics — public vs private interfaces, typed flags, reserved keys — you are writing the schema validator yourself. The validation code became deeply nested for loops with chains of conditionals just to traverse and check the structure. There was no schema, no contract, just raw dict access at every level.

I found myself writing validation code more than anything else. Pydantic helped a little but introduced its own problems — every check had to be written as a custom validator function, and I had to maintain a parallel set of Pydantic types mirroring the manifest structure. Error messages were another problem: Pydantic's validation errors are not meaningful out of the box for a package manifest, so I had to write custom error classes and formatting just to turn Pydantic's output into something a package author could understand. More code, more cases, further from the actual problem.
  

**Cross file validation made it worse.** Pact's contract system required two files per package — a namespace file defining the package's vocabulary, and one or more release files that had to conform to it:

```toml
# namespaces.toml — defines what keys are valid for this package
[namespace.compiler]
type = "bool"
reserved_flags = ["gcc", "llvm", "msvc"]
```

Every release had to be validated against its package's namespace. That meant loading the namespace file, parsing it into a dict, then loading each release file and checking every key against what the namespace declared — that the key existed, that the type matched, that there were no collisions between public and private interfaces. Correlating and validating across multiple files with plain dicts was painful and error prone. The internal representation was built by constructing dicts from dicts, transforming them into objects so they could eventually be compiled into a SQLite index.

**No line numbers.** Python's TOML parser does not preserve source locations. Validation errors had no line numbers. An error like `package libtree uses unknown key "llvm"` with no location is useless to a package author — they have no idea where in the file the mistake is. The error could point to the namespace file, the release file, or nowhere at all.

**No IDE support.** Writing a manifest gave you nothing — no autocomplete, no inline errors, no way to know what keys were valid in the current scope or what the global namespace had defined. Package authors were writing blind.

TOML works well for simple flat configuration. It does not work for a structured format that needs cross-file validation, type checking, meaningful error reporting, and a clear schema for tooling to reason about.