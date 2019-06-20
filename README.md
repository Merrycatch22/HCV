#HCV - hand history notifier*, grabber, and converter.

### Description
A poker suite for a certain Flash based poker site.
Currently, AHK is used to grab hand histories one at a time from the flash application
 and copypasted every 60 millseconds into a notepad.
handconvert.py takes in a file of hand histories and converts them into a Pokerstars-like format.
sel.py - coming soon, upgrading from bash notification system, and hopefully the AHK system too.

### Prerequisites
Install python imports via *pip3*:

    pip3 install -r requirements.txt

fill the file .creds with the first line being the site username, the second being the site password. (Temp)

chromedriver.exe needs to be on the path.

something.reg is a jank way of allowing flash to run. Sadly, Chrome is just that insufferable.

### Usage

    python3 handconvert.py <fileName>

    output will go in the "out" folder with the name "out"+fileName.

    python3 sel.py

    will open all games listed, assuming it follows the pattern.
    Soon dupes will be removed.