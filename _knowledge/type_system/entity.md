to simplify the type system for entities  everything must be any array , defluts and flags should be an array
 the checker will enforce the array len depneding on the used struct type 



# OptionTag and SelectionTag
```cue
tags: {
        compiler: #OptionTag    & ["gcc"]         
        languages: #SelectionTag  & ["en", "fr"]
    }

```

#OptionTag --> expecting an array of len 1 

#SelectionTag  -->  expecting an array of len 1+


the used struct type (OptionTag | SelectionTag) must match the parent type as in the above case 

compiler is of type "Option" and languages of type "Selection" defineind in the pacakge manespace like this:

```cue
    compiler: #Option & {
        ...
    }

    languages: #Selection & {
        ...
    }


```
so:

compiler: #SelectionTag is a type  miss match  error , cheker will eforse that these types (OptionTag | SelectionTag) must meatch parent types.

OptionTag and  SelectionTag exist to make the defntions more readable and make the cheker job easy:

```cue
        compiler: #OptionTag    & ["gcc"]         

```

 i check if "compiler" is defined in the namespace 

 i check if "compiler" is of type "Option" 
i check if the input matches what "OptionTag" must look like 





```cue
tags: {
        compiler: #OptionTag    & ["gcc"] 
        //↑ must be equal to an array of 1 since this a option of ["gcc", "llvm", "msvc"]  
        // if this pcakge has more than one build option it must be defined in a controlable way buy the user 

        languages: #SelectionTag  & ["en", "fr"]
    }

```

// package.ts
import { Package, BuildContext, Dependency } from "pm_sdk";

export default new Package({
  name: "nginx",
  version: "1.24.0",