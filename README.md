# Pact
 
> A package manager where `install libtree --gcc --channel=stable` is a query, not a command.
 
Most package managers ask **"does this package exist?"**  
Pact asks **"does a package exist that satisfies these contracts?"**
 
---
 
## The Problem
 
Traditional package managers are lookup tables — you ask for a package by name and either get it or don't. There's no way to express *what you need from a package*, and no way for a package to *declare what it supports*. Flag conflicts between packages are resolved by convention, not enforcement.
 
---
 
## How Pact Works
 
Every package in Pact is built around a **contract system**:
 
### 1. Packages declare their vocabulary
```toml
# libtree/namespaces.toml
[namespace.compiler]
type = "bool"
description = "Which compiler backend to use"
reserved_flags = ["gcc", "llvm", "msvc"]
 
[namespace.channel]
type = "enum"
description = "Release stability channel"
```
 
### 2. Releases declare what they support
```toml
# libtree/entities/release_1.6/entity.toml
id = "release_off_16"
package = "libtree"
version = "1.6"
released = 2022-08-19
source = "official"
 
[interface.compiler.backend]
flags = ["gcc", "llvm"]
default = "gcc"
 
[interface.channel.stability]
keys = ["stable", "dev"]
default = "stable"
```
 
### 3. You query, Pact resolves
```bash
pact install libtree --gcc --channel=stable
```
 
Pact finds the **best matching release** that satisfies your query — not just any release, the right one.
 

 
---
 
## Namespace Scoping
 
Namespaces are **package-scoped**. `libtree` and `ffmpeg` can both have a `compiler` namespace with completely different flags — no conflicts, ever.
 
```
libtree/namespaces.toml   →   libtree's vocabulary
ffmpeg/namespaces.toml    →   ffmpeg's vocabulary, independent
```
 
A release that declares a public flag outside its package's namespace is a **hard error** at compile time, not a runtime surprise.
 
---
 
## The Compiler
 
Pact ships with a compiler that validates every package before it enters the index:
 
```
TOML files   →   Parser   →   Checker   →   list[Entity]   →   SQLite Index
```
 
- **Parser** — loads and validates TOML syntax
- **Checker** — enforces contracts: namespace conformance, flag and key validation, schema correctness, cross-release consistency
- **Index** — a SQLite database you can query, inspect, and ship anywhere
 
The compiler guarantees that if a package is in the index, it is valid. No bad data, no surprises at install time.
 
---
 
## Install Modes
 
### Query mode
```bash
pact install libtree --gcc --channel=stable
```
Find the latest release of `libtree` that supports `gcc` and `stable`. If no release matches, `PackageNotFound`.
 
### Exact mode
```bash
pact install libtree@release_off_16 --gcc
```
Pin a specific release. Flags are verified against what that release declared.
 
### With private config
```bash
pact install libtree --gcc ::port=5432 ::db_path=/home/user/data
```
Private interface values are matched against the pinned release after query resolution. Unknown keys are ignored. Missing required values without defaults trigger a prompt.
 
---
 
## Why SQLite
 
The index is a plain SQLite database. No proprietary format, no lock-in. Any tool can read it, inspect it, or query it directly:
 
```sql
SELECT * FROM releases
WHERE package = 'libtree'
AND supports_gcc = 1
AND channel = 'stable'
ORDER BY version DESC
LIMIT 1
```
 
---
 
## Roadmap

### Core
- [x] Namespace registry
- [x] Entity model  
- [x] Public interface checker
- [ ] Private interfaces
- [ ] SQLite indexer
- [ ] CLI query engine
- [ ] Installer

### Buckets
- [ ] Multiple bucket support
- [ ] Bucket priority resolution

### Build System
- [ ] Dependency trees
- [ ] Build manifest handler
- [ ] Build hashes 


### Tooling
- [ ] Syntax checker (standalone, no install needed)
- [ ] Package linter

### Download System
- [ ] Download manifest handler
- [ ] Protocol support (https)
- [ ] Custom download handlers via Python plugins


### Plugin System
- [ ] Python plugin API
- [ ] Custom handler interface
- [ ] Plugin discovery and loading