ok let's try to break to simple steps so i can make sence where each peace goes 


first im loading a file should be named "namespace.conf" in an expected path using 


def load_hocon_file(path: Path) -> dict[str,Any]:
        config = pyhocon.ConfigFactory.parse_file(path) 
        return  json.loads(json.dumps(config))



file may not exist -> error 

parcing probelms -> error 

now the the actual file contnet 

it should look like this  



namespace: {
    
    download: {
        kind = "Option"  
        description =  "what compiler backend you want to use"
        reserved_flags = ["tedst", "tgest", "test"]
    }

    compiler: {
        kind =  "Option"  # Same here
        description =  "what compiler backend you want to use"
        reserved_flags =  ["gcc", "llvm", "msvc"]
    }

    languages: {
        kind = "Selection" 
        description =  "what languages you want"
        reserved_flags = ["en", "fr", "ar", "jp"]
    
    }

    extra: {
        kind =  "Selection"
        description = "what extra content you want"
        reserved_flags =  ["patch-01", "patch-02", "patch-03", "patch-04"]
    }

}

no top defention "namespace" -> error 

 defention of wrong type ex:

 namespace: 5 -> error 
 namespace: "wtf" -> error

 empty is fine namespace: {}


 each sub key must be a  dict must look like this 

     extra: {
        kind =  "Selection" -- > Literal in "Selection" or "Option" requred
        description = "what extra content you want" -> str requred 
        reserved_flags =  ["patch-01", "patch-02", "patch-03", "patch-04"] list[str] requred len>2 unique itmes 
    }


must ensure gloabl uniqeness of all reserved_flags