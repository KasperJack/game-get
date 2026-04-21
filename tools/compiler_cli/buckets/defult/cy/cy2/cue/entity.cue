release: {


tags: {
        compiler: #SelectionTag    & ["gcc"]         
        languages: #SelectionTag  & ["en", "fr"]
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