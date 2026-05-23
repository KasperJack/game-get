# Pact

A package manager.

## Status

**The Python prototype in this repo represents an early design direction.**
 
Pact is currently being rewritten in Go. The new implementation is designed as a single self-contained binary with zero external dependencies, targeting native support for Windows first, followed by Linux.

Package manifests are currently written in Lua.

Before the package manager itself, the [CI tool](https://github.com/KasperJack/pact-tools) is being developed first. Its role is to validate, build, and publish manifests into the registry. Once the manifest format and workflow are stable, the package manager will be built on top of that foundation.

This repository exists mainly to preserve the [original design](./0.4.md ) and ideas behind Pact.

## Goals

-   Simple and reproducible package definitions
    
-   Cross-platform support 🤣
    
-   Single binary distribution
    
-   Declarative manifests
    
-   Fast local and CI workflows
    
-   Minimal dependencies
    

## Current Direction

Pact is evolving into a system built around:

-   A Lua-based manifest format
    
-   A standalone CI/build toolchain
    
-   Registry publishing workflows
    
-   Reproducible package builds
    
-   Native Go implementation
    

The long-term goal is to create a practical package management ecosystem that stays lightweight, transparent, and easy to understand.