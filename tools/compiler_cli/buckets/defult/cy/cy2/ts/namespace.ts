// namespace.ts
import { Option, Selection, type NamespaceDef } from "./sdk.ts";

export const namespace = {

    download: Option({
        description: "how you want to download the binary",
        choices: ["http", "sftp", "ssh"],
    }),

    compiler: Option({
        description: "what compiler backend you want to use",
        choices: ["gcc", "llvm", "msvc"],
    }),

    languages: Selection({
        description: "what languages you want",
        choices: ["en", "fr", "ar", "jp"],
    }),

    extra: Selection({
        description: "what extra content you want",
        choices: ["patch-01", "patch-02", "patch-03", "patch-04"],
    }),

} satisfies NamespaceDef;