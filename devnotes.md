# gameget — dev notes

## where it started

The original idea was simple: build a tool that can **search and download games from piracy sites**.

The first concept was straightforward:

-   scrape multiple download sites
    
-   fuzzy-match game names
    
-   extract download links
    

That was it.

### initial architecture idea

I planned to make the scraper **modular**. Each site would have its own module that tells the tool:

-   how to search the site
    
-   how to extract download links
    
-   how to resolve file hosters
    

Example structure:

```
sources/  
  steamunlocked.py  
  fitgirl.py  
  dodi.py  
  
resolvers/  
  megadb.py  
  gofile.py  
  pixeldrain.py
```

I built a quick **Python prototype using SteamUnlocked**, and it worked well.

But when I tried adding more sources, problems started appearing:

-   searching multiple sites was **slow**
    
-   results were **inconsistent**
    
-   fuzzy matching produced **mixed results**
    
-   scraping logic was fragile
    

That pushed me toward solving the **game identity problem** first.

---

# game metadata — the API rabbit hole

To search properly, I needed a **reliable way to resolve game names and metadata**, not just raw text searches.

I evaluated several APIs.

### RAWG

Pros:

-   free
    
-   simple API
    

Cons:

-   no good way to filter **base games vs editions**
    
-   would require **post-processing name filters**
    

Example problems:

```
Far Cry 5  
Far Cry 5 Gold Edition  
Far Cry 5 Deluxe Edition  
Far Cry 5 Season Pass
```

Not ideal.

---

### Steam Store API

Endpoint:

```
store.steampowered.com/api/storesearch/
```

Pros:

-   no API key
    
-   fast
    

Cons:

-   only Steam games
    
-   limited metadata
    

Useful but incomplete.

---

### IGDB (best option)

IGDB is owned by Twitch and requires OAuth, but it's **free and extremely comprehensive**.

Pros:

-   massive game database
    
-   accurate metadata
    
-   `slug` values often match piracy site URLs
    
-   useful fields like:
    

```
game\_type  
platforms  
first\_release\_date  
version\_parent
```

This turned out to be the best solution.

---

## IGDB pain points (learned the hard way)

Several quirks took a while to figure out:

-   `search` + `where` filters break if you use the **deprecated `category` field**
    
-   `category` has been replaced with **`game_type`**
    
-   `game_type = 0` (main game) is often stored as **null/missing**, not literal `0`
    
-   because of that, filtering by it can return unexpected results
    

Eventually I discovered the real issue:

The problem wasn't `game_type`.  
It was using the **deprecated `category` field**.

Once I switched to `game_type`, everything worked correctly.

Other useful filters:

```
version\_parent = null
```

Removes:

-   Gold editions
    
-   Deluxe editions
    
-   bundles
    

```
first\_release\_date < now
```

Removes unreleased games.

---

### one-liner IGDB query that works

```
search "far cry";  
fields name, slug, first\_release\_date;  
where platforms = (6)  
  & version\_parent = null  
  & game\_type = 0  
  & first\_release\_date != null  
  & first\_release\_date < {unix\_timestamp};  
limit 50;
```

Platform `6` = PC.

---

## filtering cracked games

Even with IGDB, another issue appeared:

Many games are:

-   online-only
    
-   free-to-play
    
-   not cracked yet
    

There is **no point searching download sources** for games that haven't been cracked.

So the search pipeline should look like this:

```
IGDB search  
    ↓  
cracked-game check  
    ↓  
download backends  
    ↓  
results
```

---

## crack status sources

### PreDB

Scene releases first appear on **private IRC topsites**, then spread to torrents and download sites.

We can't access private topsites, but **PreDB tracks scene releases publicly**.

Example API:

```
https://predb.ovh/api/v1/?q=far+cry+3
```

---

### CrackWatch

CrackWatch had an API:

```
https://crackwatch.com/api/games?slug={slug}
```

But it's now **deprecated**.

---

### IRC / SceneP2P

Another interesting option is **SceneP2P**, a public IRC network.

It isn't the private scene, but it hosts a **large library of releases**.

Connection details:

```
server: irc.scenep2p.net  
channel: #THE.LOUNGE
```

Search command:

```
!s <game name>
```

Bots respond with **XDCC download commands**.

The Python library `xdcc-dl` can automate the entire flow.

This could potentially be implemented as a **backend source**.

---

# the shift — from scraper tool to package manager

At some point it became clear:

**Scraping is fragile.**

Problems:

-   sites go down
    
-   layouts change
    
-   URLs break
    
-   results are inconsistent
    

The real problem is that there is **no structured way to define how a specific game should be installed from a specific source**.

---

## inspiration from package managers

Tools like:

-   Scoop
    
-   Homebrew
    
-   Winget
    

all follow the same model:

```
manifest + bucket
```

-   **manifest**: defines how to install a package
    
-   **bucket**: a git repository that hosts manifests
    

Communities contribute by **submitting pull requests**.

This model solves many problems.

Instead of scraping every time, the manifest already defines:

-   where to download the game
    
-   which version
    
-   how to install it
    

Scraping then becomes **a tool for generating manifests**, not the core functionality.

---

# backend system

Each source is implemented as a backend module.

Example:

```
backends/  
  steamunlocked.py  
  fitgirl.py  
  dodi.py  
  irc\_scenep2p.py
```

The core program can run them:

-   sequentially
    
-   or in parallel
    

---

# manifest system — current design

Package identity is defined as:

```
game + source + version
```

Example:

```
elden-ring fitgirl 1.3
```

is **not the same package** as

```
elden-ring steamunlocked 3.0.0.9
```

Updates only occur **within the same source**.

---

## bucket structure

```
bucket/  
  index.json  
  
  games/  
    el/  
      elden-ring/  
        index.json  
  
        fitgirl/  
          1.3/  
            manifest.json  
            post\_install.ps1  
            1.torrent  
  
          1.4/  
            manifest.json  
            post\_install.ps1  
  
        steamunlocked/  
          3.0.0.9/  
            manifest.json  
            post\_install.ps1  
  
  sources/  
    fitgirl.json  
    steamunlocked.json
```

Game folders use a **two-letter prefix** (similar to Git object storage) to prevent directories from becoming too large.

---

## manifest structure (draft)

### game index

`index.json`

Contains:

-   `id`
    
-   `name`
    
-   `igdb_id`
    
-   `default` (source + version)
    
-   list of packages with **stability tags**
    

---

### version manifest

`manifest.json`

Fields:

-   `size`
    
-   `release_date`
    
-   `updates_from`
    
-   `downloads`
    
-   `checksum`
    

Downloads can include:

-   torrent
    
-   direct download
    

One source can be marked as **preferred**.

---

### post-install script

`post_install.ps1`

Handles:

-   archive extraction
    
-   copying crack files
    
-   creating shortcuts
    
-   cleanup
    

Install logic is **version-specific and source-specific**.

For example:

-   FitGirl installs differently than SteamUnlocked.
    

---

## stability lifecycle

New packages follow a simple lifecycle:

```
new PR  
   ↓  
testing  
   ↓  
community confirmation  
   ↓  
stable  
   ↓  
set as default version
```

---

# open questions

Still unresolved:

-   final manifest schema
    
-   update mechanism (delta patches vs full reinstall)
    
-   bucket resolution when multiple buckets are added
    
-   GUI (planned with PySide6)
    
-   achievement tracking
    

For achievements, the **Goldberg Steam emulator** stores them in local JSON files, which could be parsed and resolved via the Steam API.

---
