# CUE

Tired of writing error checking code, I wanted a smart configuration language that could hold the validation logic itself. The idea was to move all the checks into CUE's type system and use it to write manifests — CUE evaluates and enforces the schema, the Python side just runs the evaluation and gets back already validated data. No more manual validation loops.

The user facing side of the manifests looked clean:

```cue
release: {
    tags: {
        compiler:  #SelectionTag & ["gcc"]
        languages: #SelectionTag & ["en", "fr"]
    }

    public: {
        compiler: {
            backend: #Pick & {
                flags:   ["gcc", "llvm"]
                default: ["gcc"]
            }
        }
    }

    private: {}
}
```

## Why it broke down

**CUE is complex (skill issue)** CUE is a powerful language but it has a steep learning curve. The moment I needed custom cross-struct validation — checking flag collisions across namespaces from multiple files — it got complex fast. The logic I was trying to express was not unreasonable but CUE's way of expressing it was hard to follow and harder to debug:

```cue
_all_flags: [for ns in namespace for f in ns.reserved_flags {f}]

Validation: {
    for i, a in _all_flags {
        for j, b in _all_flags if i < j {
            if a.flag == b.flag {
                "\(a.flag)": _|_ & "Duplicate flag in \(a.origin) and \(b.origin)"
            }
        }
    }
}
```


```cue

// this  is a validation rule 
#Release: {
    [K in namespace]: {

        "_"?: {
            flags: string & (namespace[K].reserved_flags[_])
        }

        [Name != "_"]?: {
            if namespace[K].type == "option" {
                flags: string & (namespace[K].reserved_flags[_])
                default?: string & (namespace[K].reserved_flags[_])
            }

            if namespace[K].type == "selection" {
                flags: [...string] & [ for f in _ { f & namespace[K].reserved_flags[_] } ]
                default?: [...string] & [ for f in _ { f & namespace[K].reserved_flags[_] } ]
            }
        }
    }
}
```
Even with help I could not make sense of what I was writing. CUE rewards deep familiarity with its evaluation model — without that, complex constraints become unreadable quickly.

**Errors were not friendly.** CUE's error messages for constraint violations are not easy to wrap or reformat. I had no way to turn a CUE evaluation error into a clean, human readable message for a package manager.

**No Python integration.** There is no native CUE library for Python. Evaluating CUE required shelling out to an external binary, which added a dependency and a point of failure I did not want.

CUE was the right idea — move validation into the schema language itself — but the wrong tool for where I was. It is a serious language that requires serious investment to use effectively.










