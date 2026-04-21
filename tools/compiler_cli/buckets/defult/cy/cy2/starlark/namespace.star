load("//sdk/base.star", "make_namespace" ,"ns_selection", "ns_option")


libtree_namespace = make_namespace(
    ns_option("download", "how you want to download", ["http", "sftp", "ssh"]),
    ns_option("compiler", "compiler backend", ["gcc", "llvm", "msvc"]),
    ns_selection("languages", "languages", ["en", "fr", "ar", "jp"]),
)


