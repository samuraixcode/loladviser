# loladviser or in other words League of legends adviser.

Artificial Intelligence collects ranked games data and advises in what hour you have more chance to win.
This program is using riot's api to download the data for the AI.

Instructions:
1. Install Anaconda python (https://www.continuum.io/downloads) as administrator, accept all defaults.
2. Download the source code.
3. Extract the code into folder.
4. Get your API key from riot.
5. Edin Main.py, in the beginning of the file there are User configuration settings.
6. Enter your summoner name btw '' of playerName =. example: playerName = 'shagi'
7. Edit RiotConsts.py, see the regions and copy the full name of your region.
8. Go back in Main.py and enter your region full name btw '' of Consts.REGIONS[]. example: Consts.REGIONS['europe_nordic_and_east']
9. Enter your api in '' of the apikey=. example: apikey = 'asdf-asdf-asdf-asdf'
10. Save file.
11. Start cmd.exe, go to the source code folder and type python Main.py
