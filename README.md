# loladviser or in other words League of legends adviser.

Artificial Intelligence collects ranked games data and advises you in what hour you have more chance to win.
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
12. After the program is finished you will have an image for your daily win rate.
Next time you run the program it will use the already
downloaded files to calculate for the day's winrate.
12. When you want new AI calculations just delete w.txt.
13. When you want to include in the AI's database the new played games just delete the old data: xdata.npy and ydata.npy.

contacts: ivodwvio@mail.bg
