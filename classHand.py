import re

class Hand:
    # for regexing the button.
    btnProg=re.compile(r'^The button is in seat')

    # a result line is removed from the string.
    rmResultProg=re.compile(r'\D:|shows|wins|mucks')

    # modifies uncalled bet to ps type.
    uncalledBetProg=re.compile(r'^Uncalled bet of (\$[\d.\.]+)')

    # changes the blind posting lines
    blindProg=re.compile(r'posts the (small|big) blind of')

    # gets the money on the table
    moneyProg=re.compile(r'^(Seat \d: \S+ \(\S+)(\))')
    prog6=re.compile(r'^(\S+) ')

    # checks if the seats are top and summary
    seatCheckProg=re.compile(r'^Seat (\d)') 

    #prog8=re.compile('Bluff Avenue Game #\d+: (.+), Table \d+ - (\$[\d\.]+/\$[\d\.]+) - (\S+ Limit) (\S+) - (\d+:\d+:\d+) \S+ \S+ - (\d+)/(\d+)/(\d+)')
    titleProg=re.compile(r'Bluff Avenue Game #\d+: (.+, Table \d+) - (\$[\d\.]+/\$[\d\.]+) - (\S+ Limit) (\S+) - (\d+:\d+:\d+ \S+) \S+ - (\d+)/(\d+)/(\d+)')

    # for double blind post warning
    doubleBlindProg=re.compile(r'^(\S+): posts') 

    def __init__(self,raw):
        self.raw=raw
        self.split=raw.splitlines()
        self.processOnInit()

    def __hash__(self):
        return hash(self.split[0])

    def __eq__(self,other):
        return self.split[0]==other.split[0]  
    
    def processOnInit(self):
        #mod is a copy of split we should modify.
        mod=self.split.copy()
        #if we find a line to remove from the split raw, remove it in the mod.
        for line in self.split:
            if Hand.rmResultProg.search(line):
                mod.remove(line)
        # TODO: figure out what button is for.
        button="-1"

        for line in self.split:
            if Hand.btnProg.match(line):
                #print(line.find('#'))
                button=line[line.find('#')+1:]
                #print(button)
                mod.remove(line)
                break