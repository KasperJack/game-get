//schema.cue
package main

import "list"

// ---- Namespace types ----
#Option: {
    type:           "option"
    description:    string
    reserved_flags: list.MinItems(1) & [...string]
}

#Selection: {
    type:           "selection"
    description:    string
    reserved_flags: list.MinItems(1) & [...string]
}

namespace: [string]: #Option | #Selection

// ---- Duplicate flag check across namespace ----
_allFlags:     [ for _, v in namespace for f in v.reserved_flags { f } ]
_noDuplicates: list.UniqueItems & _allFlags

// ---- Type hints ----
// tags
#OptionTag:    list.MinItems(1) & list.MaxItems(1) & [...string]  // exactly 1
#SelectionTag: list.MinItems(1) & [...string]                     // 1+

// public
#Pick: {
    flags:    list.MinItems(1) & [...string]
    default?: list.MinItems(1) & list.MaxItems(1) & [...string]   // exactly 1
}
#Set: {
    flags:    list.MinItems(1) & [...string]
    default?: list.MinItems(1) & [...string]                      // 1+
}

// ---- Release schema ----
#Release: {
    tags?: {
        for k, v in namespace if v.type == "option" {
            "\(k)"?: #OptionTag & [or(v.reserved_flags)]          // len 1, must be in reserved_flags
        }
        for k, v in namespace if v.type == "selection" {
            "\(k)"?: #SelectionTag & [...or(v.reserved_flags)]    // len 1+, each in reserved_flags
        }
    }
    public?: {
        for k, v in namespace if v.type == "option" {
            "\(k)"?: [string]: #Pick & {
                flags:    [...or(v.reserved_flags)]               // subset of reserved_flags
                default?: [or(v.reserved_flags)]                  // len 1, in reserved_flags
            }
        }
        for k, v in namespace if v.type == "selection" {
            "\(k)"?: [string]: #Set & {
                flags:    [...or(v.reserved_flags)]               // subset of reserved_flags
                default?: [...or(v.reserved_flags)]               // 1+, in reserved_flags
            }
        }
    }
}

release: #Release