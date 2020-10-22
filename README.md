# MagiReco NA Private Server

This is the code for kávézó's MagiReco private server.

---
### Installation and running

On Windows x64, just download the zip in releases and run runServer.bat. (At least I think. Haven't tested this on an 
x32 machine so it might only work on x64...) You can close the browser window that pops up but not the command line
that does.

On any other system,
1. Make sure you have python3, either in a separate env (recommended because system-wide Python dependency graphs are 
gross) or on your system
2. Run `pip install -r requirements.txt` in a command line
3. Run `mitmproxy -s server.py` or `mitmweb -s server.py` in a command line, and do not close this command line. (If you
run mitmweb though, you can close the browser window.)

### Connecting to the private server

1. Make sure MagiReco is already installed on your device. I've only tested it on when it's past the tutorial, so no 
guarantees it'll work for a fresh install.
2. Find the IP address of the computer you're running the server on
3. Configure a proxy on your device with the server address as your computer's IP address, and the port as 8080
4. Open mitm.it, and download and enable a certificate for your device
5. If you can load google.com through the proxy, then you can open the app and everything will be through the private
server.

I had a horrible time getting mitmproxy to work on some of my devices; specifically, I never got it to work with my Mac
running mitmproxy and my iPhone 6 trying to get through it. Try googling any errors you have with mitmproxy; it may or
may not help. In the future I might move off of mitmproxy and find a different solution.

---
### Porting over your existing data

On Windows, run getUserData.bat. You can close the browser window that pops up, but not the command line. 

On another system, follow steps 1 and 2 in the Installation and Running section, then run
`mitmproxy -s getUserData.py` or `mitmweb -s getUserData.py` in a command line without closing it.

Follow the instructions for connecting to the private server to get your device connected to the script. Then, get to the
title screen (the one that has the MagiReco logo on it, and from which you can see the ToS and transfer your account).
You should now see the command line print a lot of lines saying "writing to ------". Once the command line says it's done,
close the command line. You can run the private server now, and it will serve your your own data.

User data is stored in the files in data/user. When you run getUserData.py, the data is backed up to in data/userBackup.
You can change the data in the data/user folder and the data displayed in the game will change as well.

The default user is a level 999 account with only Iroha and no memoria but 999 of every material, including summon tickets.

---

### Currently supported functions:
- displaying any page in the app (api/page.py)
    + as well as displaying anything in the archive
    + and listing memoria
- improving magical girls (api/userCard.py)
    - level up
    - magia level up
    - awaken
    - limit break
- managing memoria (api/userPiece.py and api/userPieceSet.py)
    - level up
    - limit break
    - making memoria sets
    - putting memoria into the vault and taking them out
- gacha (api/gacha.py)
    - pull premium, x1 and x10, using stones and tickets
    - pull normal
    - view history
- changing user settings (api/gameUser.py, api/user.py, api/userChara.py)
    - set name
    - set comment
    - set leader
    - set background (only two backgrounds are available, but...)

### Currently missing functions:
- can't customize magical girls' looks (e.g. in disks)
- can't recover AP
- can't lock or sell memoria
- you can't clear any missions or accept their rewards
- mirrors, quests, and team-making are entirely nonfunctional
- can't buy anything from shop

### What's next?
I coded very fast, and very not well, because I wanted to get as many features out before the 30th. Code quality is still
important to me, though, and I really don't want to get anything done outside of the basics before improving it enough
that maintenance will not be horrendous. But before the 30th, my priority is to get all the basic functions implemented
so that we won't have to rely on hitting the real server to figure out what it does for some important thing like 
battles.

The features are in order of the most overlap with the knowledge I have currently, to the least, because when I 
implement a new feature I don't know much about at least half of the time is spent researching how it fits in with all 
the user's data.

- implement shop
- implement team-making
- implement quests
- implement mirrors
- implement missions
- implement random things I left off, like AP recovering
- add unit tests
- refactor
    - put all the data reading and writing into a util module to avoid race conditions with 50 different functions 
    writing/reading to a file at the same time
    - improve response headers, perhaps add compression
    - maybe make a class each API has to extend that removes repeated code?
    - maybe make classes that represent each type of object used in the game (e.g. item, card, userCard)?
- add support for events
- add support for multiple users (using a database like S3)
- add support for finding other users, following and using supports
- move server to the cloud
- hack app to call the server's address rather than having to rely on mitmproxy

### Structure of this package
As you can tell from the instructions, server.py is the main event handler. It intercepts requests from the app thanks
to mitmproxy, and decides what to do.

Most resources are going to be retrieved from an archive. For now that's en.rika.ren, but I don't know anything about
rika.ren other than that it stores assets, and I might switch to my own archive later if we want to have custom assets 
(like if we want to bring JP events in).

The exception is website assets (html, js, css, and the like). These are stored locally because they're small in size,
not likely to change, storing them speeds up loading, and we might want to edit them later to support new features like
setting a bunch of awaken mats at once, or SE. These are stored in the assets folder.

User data right now is stored locally as well, in the data/user directory. You can actually modify the files in here to
change which megucas or memes or items you have. Just be careful or the app will error if you messed up on a line or 
something.

All the support for different API endpoints is stored in the api directory; each endpoint has its own file. They all
take a request from the app, and generate the response. They edit the user data files directly, and also access the
general data files in the data directory that store things like a list of all the megucas in the game.

The page endpoint handles all of the info that the app needs to display different views, like the "Magical Girls"
screen or the different shops. None of the other endpoints are called until you actually try to change the user's
game data.

----
If you have suggestions or want to help (you can help even if you don't know how to code!), please contact me at
threethirtyseven111@gmail.com, u/rhyme_or_rationale, or rinsfouriertransform#2303. And feel free to send a pull request 
anytime~
