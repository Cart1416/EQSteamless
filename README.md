# EpicQuest steamless
Play **EpicQuest** without **Steam**!  
This works by using a web auth token to log into the game instead of getting one with Steam  
The login script does **not** have the option to create an account, please make an account on another device or ask a friend.  
Note: you may be randomly logged out every few hours (idk the exact time) just run login.py again if the game is stuck in a loop  
This also works with [Goldberg](https://mr_goldberg.gitlab.io/goldberg_emulator/)  
## How to use
**First time setup:**  
Download repo (green code btn -> download zip)  
Extract zip  
Put these files into EpicQuest game folder (replace existing files)  
Run login.py with python3 to generate auth token (do not share auth.txt!)  
<br>
**Play**  
You need Steam open unless using Goldberg.  
Start EpicQuest (RecRoom.exe)  
Wait for game to show login screen  
On Windows: run startAuthProxy.bat  
On Linux: run startAuthProxy.sh in terminal  
In game press F1 to reload the login screen (or any other way to reload it)  
## Requirements
Python3  
login.py will install the modules for you  
## AI
Only part made with AI was LoginScreenReload because C# sucks  
Everything else is human slop  
## Links
[Mitmproxy](https://www.mitmproxy.org/)  
[Goldberg](https://mr_goldberg.gitlab.io/goldberg_emulator/)  
[EpicQuest](https://epicquest.app)  
LoginScreenReload  
