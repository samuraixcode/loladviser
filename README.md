# loladviser aka League of legends adviser

Artificial Intelligence collects ranked data from riot, and advises in what hour you are more likely to win. The AI helps you dodge low players like feeders and trolls, and helps you focus on your best gaming experience with the good players. This project is far from complete, and there are a lot of features waiting to be implemented. Helping with donation for this project will give the programmers the resource to continue developing. Read the README.md file for instructions how to use.

Instructions:
1. Install Anaconda python (https://www.continuum.io/downloads) as administrator, accept all defaults.
2. Download the source code.
3. Extract the code into folder.
4. Get your API key from riot. (https://developer.riotgames.com/)
5. Edin UserConfiguration.py file.
6. Replace type_your_summoner_name_here with your summoner name.
7. Edit RiotConsts.py, see the regions and copy the full name of your region.
8. Go back in UserConfiguration.py file and replace type_your_region_full_name_here with your region full name.
9. Replace type_your_apikey_here with your apikey.
10. In the end the UserConfiguration.py file must look like this: (but filled with your own data)

USER = {
	'name': 'glvio',
	'region': 'europe_nordic_and_east',
	'api': 'CGAPI-962397d3-c9b4-4cbc-a7ca-94ae9b599a43'
}

10. Save file.
11. Start cmd.exe, go to the source code folder and type: python loladviser.py
12. After the program is finished you will have an image for your daily win chance (x scale - hours, y scale - % win chance).
13. If you like this program and you want further development,
please consider donation, in the Donation folder is the Bitcoin
address and QR code.

contacts: ivodwvio@mail.bg
