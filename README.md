# DeadInternetTheory

## 🧠 Concept

This project is inspired by the [Dead Internet Theory](https://en.wikipedia.org/wiki/Dead_Internet_theory), a conspiracy theory suggesting that most of the internet is now generated and controlled by bots.

While there are many types of bots, this project focuses on **Group III**, the disruptive ones. Think spammy repost bots flooding social media platforms with generated content.

> ⚠️ **Note**  
> This repository is not a research paper on DIT.  
> If you're curious about the theory itself, go do your own homework.  
> This is about building the bot, not debating its origins.

---

### 🧩 Project Thinking

Originally, I just wanted to mess around with building a repost bot for TikTok.  
**Problem?** Simply downloading and re-uploading videos doesn’t work, they get flagged or struck almost immediately.

So I tried another approach: **generate idle games with Pygame** and post screen recordings. Technically it worked… but honestly? It was tedious, low-impact, and time-consuming.

**Now:**  
I'm generating short videos using AI, then posting them. It’s fast, fun, and doesn’t trigger content violations. This seems like the most promising path, we’ll see where it leads.

[//]: # (---)

[//]: # ()
[//]: # (## 🧪 Current State)

[//]: # ()
[//]: # (Here’s what’s implemented so far and what needs improvement:)

[//]: # ()
[//]: # (| Feature        | Status                                | Notes                                                  |)

[//]: # (|----------------|----------------------------------------|--------------------------------------------------------|)

[//]: # (| `--load-json`  | ✅ Working                             | Loads prompts/metadata into the DB                     |)

[//]: # (| `--pix-credit` | ✅ Working                             | Retrieves free daily generation credits                |)

[//]: # (| `--post`       | ⚠️ Was working, needs review          | Posting logic needs polish / maintenance               |)

[//]: # (| `--create`     | ⚠️ Not fully tested, seems functional | Needs robustness checks                                |)

[//]: # (| `--register`   | ✅ Working                             | Saves session cookies via manual login in browser      |)

[//]: # ()
[//]: # (---)

## 🚀 Getting Started

Thanks to Python’s simplicity (and chaos), you can run this project in just a few steps:

```bash
git clone git@github.com:dolvui/DeadInternetTheory.git
cd DeadInternetTheory
pip install -r requirements.txt
```

## ⚙️ Available Parameters

### `--sessions-path`

Load all necessary data, paths, sites, and JSON files for the script

```bash
python main.py --sessions-path="path/to/file.json"
```

**Expected JSON format:**

```json
{
  "main" : "<path of the main session .dat>",
  "pix_account" : ["<List of path to others accounts .dat>",...], 
  "chrome_path" : "path\\to\\chrome.exe",
  "links" : {
    "HOME_STUDIO" : "<home of the website>",
    "STUDIO" : "<creation page of the website>"
  },
  "database" : "path\\to\\database.db"
}
```
> [!IMPORTANT]  
> This is the only required parameter.  
> Without it, nothing works, so make sure to specify it on every launch.

---

### `--load-json`

Load a list of prompts/videos into the internal database.

```bash
python main.py --load-json="path/to/file.json"
```

**Expected JSON format:**

```json
[
  {
    "prompt": "<prompt for the IA>",
    "voix": "<spoken text for the IA to be added>",
    "description": "<description for social network>"
  },
  ...
]
```

---

### `--pix-credit`

Collect daily free image generation credits from a third-party service.

```bash
python main.py --pix-credit=True
```

---

### `--create`

Generate a video using an account and save it in the given path for future posting.

```bash
python main.py --create="path\\to\\videos\\directory"
```

---

### `--post`

Post a previously generated video on social media.

```bash
python main.py --post=True
```

---

### `--register`

Open a browser window to manually log in and save a session cookie.

```bash
python main.py --register="session_cookie.dat"
```

You’ll have 2 minutes to log into your account. After that, the session cookie is saved to the file you specify.

> 🎯 **Why this matters**  
> Modern sites make automated login a nightmare. But once you're logged in manually, we can re-use the saved session for future actions, one cookie file per account.

---

## 🧪 Current State

Here’s what’s implemented so far and what needs improvement:

| Feature                | Status     | Notes                                             | Require |
|------------------------|------------|---------------------------------------------------|---------|
| `--load-json`          | ✅ Working  | Loads prompts/metadata into the DB                |   ❌     |
| `--pix-credit`         | ✅ Working  | Retrieves free daily generation credits           |   ❌     |
| `--post`               | ✅ Working  | Seems good for me, post on tiktok                 |    ❌    |
| `--create`             | ✅ Working  | create and download in a directory 'videos'       |   ❌     |
| `--register`           | ✅ Working  | Saves session cookies via manual login in browser |   ❌     |
| `--sessions-path`      | ✅ Working  | Path to the json file                             |   ✔️     |

---

## 💡 Usage Advise

To automate, so no human action is needed :

### 🐧 Linux

```bash
#!/bin/bash

echo "Hello world !" 
```

### 🖥️ Windows

Here the base action needed, adapt to your case

Retrieve credit is the example chosen

#### Step 1

Prepare your Environment, open a Powershell in `C:\...\...\DeadInternetTheory\`

```Powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

#### Step 2

Create a file `auto.bat` in `C:\...\...\DeadInternetTheory\`

so
`C:\...\...\DeadInternetTheory\auto.bat`

```bat
@echo off
cd /d C:\...\...\DeadInternetTheory\
call venv\Scripts\activate.bat
python main.py --sessions-path="sessions.json" --load-json="./idea.json"
```

#### Step 3

- Press `Win` + `S`, search Task Scheduler.
- Click Create Basic Task.
- Name: Run Script at 9AM.
- Trigger: Daily, time: 09:00.
- Action: Start a program → Browse to your auto.bat.

Finish.

### 🍎 Apple

throw your mac to the trash

---

## 🐞 Bugs  🤨

> [!WARNING]  
> When creating a video, the page switches to fullscreen.  
> **However**, if you're on a laptop with a small screen, some elements might not be visible, which can cause the script to fail (`element is of type None`).  
> On a larger screen, everything works fine.  
>  
> I could patch this by calling `scroll_into_view()` on each element...  
> But honestly? *Too lazy for now.*


---

## 💬 Final Note

This project is a playground for automation, scraping, content generation, and platform interaction.  
It’s designed for experimentation, not abuse, use responsibly.

---

🛠 Built with Python • By [@dolvui](https://github.com/dolvui)
