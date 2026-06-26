# HOCON

After TOML, I moved to HOCON. It looked promising — the syntax was nicer and more readable, it supported `include` for importing other files which meant I could load a package as a single file instead of correlating multiple files manually, and editors gave some basic autocomplete.

The validation problems were still there — I still had to check types, validate namespace collisions, and enforce the contract system manually. But the structure was less painful to work with than raw nested dicts, and the single file load was a real improvement.



```HOCON
namespace: {
    

    compiler: {
        kind =  "Option"  
        description =  "what compiler backend you want to use"
        reserved_flags =  ["gcc", "llvm", "msvc"]
    }

    languages: {
        kind = "Selectdsion" 
        description =  "what languages you want"
        reserved_flags = ["en", "fr", "ar", "jp"]
    
    }

    extra: {
        kind =  "Selection"
        description = "what extra content you want"
        reserved_flags =  ["patch-01", "patch-02", "patch-03", "patch-04"]
    }

}
```








## Why it broke down

**The Python parser was not reliable.** The only Python HOCON parser, `pyhocon`, was not stable enough for what I needed. HOCON is a flexible format — it allows multiple syntax styles for the same construct:

```
key: value

key = value

name = "foo"

name = foo

arr: [5, "5", foo]
```

I was sticking to one consistent style in my manifests but still hitting cryptic parsing and JSON conversion errors. The parser output had to be round-tripped through JSON just to get a usable dict:

```python
def load_hocon(path: Path) -> dict[str, Any]:
    try:
        config = pyhocon.ConfigFactory.parse_file(path)
    except Exception as e:
        raise ParseError(str(e)) from e

    try:
        return json.loads(json.dumps(config))
    except Exception as e:
        raise ConfigConversionError(str(e)) from e
```

The flexibility of HOCON is also its cost. A format that accepts that many ways to write the same thing is hard to parse correctly and hard to validate consistently. I did not like the two points of failure — parsing and then converting to JSON — any step could silently produce wrong output or throw a cryptic error. There is a possibility I did not explore it deeply enough or test enough cases, but the errors I was hitting were enough to lose confidence in the parser for anything serious.

**Still no line numbers.** Pyhocon did report line numbers for parse errors, but that did not help with my own validation errors. Once the file loaded successfully, pyhocon did not preserve source locations — so I could tell a package author their file failed to parse and where, but I had no way to point to a specific value in the file when my own validation logic caught a problem. Parse errors had locations