# gameget

A package manager for games. Manifests define where to get a game, 
which version, and how to install it. Buckets are git repos that host manifests.

gameget handles the full lifecycle — search, install, update, and manage games across multiple sources. Install directly from a manifest file, pull from remote community buckets, or build your own. Multiple sources and versions for the same game are supported out of the box.



## install a game
```powershell
gameget install ion-fury
gameget install ion-fury --source steamrip
gameget install ion-fury --version 2.0.0.1 --method torrent
```

## status

Early development — core manifest system, loader, and resolver are being built. Not usable yet.

## contributing

Adding a game means adding the folder structure and TOML files. 
Tooling to scaffold manifests coming soon.