#re is the regex import
import re, random
import sys
from classHand import Hand
from platform import system

def modifySplitList(splitList):
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

    #TODO: collect player names proper
    playerNameProg=re.compile(r'^(Seat \d: (\S+) \(\S+)(\))')
    prog6=re.compile(r'^(\S+) ')

    # checks if the seats are top and summary
    seatCheckProg=re.compile(r'^Seat (\d)') 

    #prog8=re.compile('Bluff Avenue Game #\d+: (.+), Table \d+ - (\$[\d\.]+/\$[\d\.]+) - (\S+ Limit) (\S+) - (\d+:\d+:\d+) \S+ \S+ - (\d+)/(\d+)/(\d+)')
    titleProg=re.compile(r'Bluff Avenue Game #\d+: (.+, Table \d+) - (\$[\d\.]+/\$[\d\.]+) - (\S+ Limit) (\S+) - (\d+:\d+:\d+ \S+) \S+ - (\d+)/(\d+)/(\d+)')

    # for double blind post warning
    doubleBlindProg=re.compile(r'^(\S+): posts') 

    #for time duplication checking, now with gamename too
    gametimeStorage=[] 
    for split in splitList:
        # for the print of the straddle
        # straddleFlag=True 

        for line in list(split):

            if rmResultProg.search(line):
                split.remove(line)
        
        button="-1"
        # for line in list(split):
        #     if line.find('CMU Brandon')!=-1:
        #         line=line.replace('CMU Brandon','CMUBrandon')
        #         # print line

            
        
        for line in list(split):
            if btnProg.match(line):
                #print(line.find('#'))
                button=line[line.find('#')+1:]
                # print(button)
                split.remove(line)
                break
        
        first_re=titleProg.match(split[0]) #what does this do fuck
        gamename=first_re.group(1) #name of the game's table, with table number
        
        #print(gamename)
        
        stake=first_re.group(2)
        gametype=first_re.group(4)+" "+first_re.group(3)
        
        #gametime=first_re.group(5)
        
        temptime=first_re.group(5)
        hour=int(temptime[:temptime.index(':')])
        if temptime[-2:]=="AM":
            
            if hour==12:
                hour=0
        elif temptime[-2:]=="PM":
            if hour!=12:
                hour+=12
        gametime=str(hour)+temptime[temptime.index(':'):-3]
        #print(gametime)
            
        gamedate="20"+first_re.group(8)+"/"+first_re.group(6).zfill(2)+"/"+first_re.group(7).zfill(2)
        hash=0
        for stri in split:
            for chrc in stri:
                hash=(ord(chrc)*13+hash)%9973
        gamenumber=gamedate.replace("/","")+gametime.replace(":","").zfill(6)+str(hash%10000).zfill(4)
        
        split[0]="PokerStars Hand #"+gamenumber+":  "+gametype+" ("+stake+" USD) - "+gamedate+" "+gametime+" ET"
        #split[0]="PokerStars Hand #"+str(random.randint(1,1000000000000))+":  Omaha Pot Limit ($0.10/$0.20 USD) - 2017/07/19 4:59:02 ET"
        split.insert(1,"Table '"+gamename+"' 9-max Seat #"+button+" is the button")
        
        state=0
        seatStringStorage=[] # for seat number storage
        blindStringStorage=[] # for blind storage
        blindDeletion=[]
        
        gamenametime=gamename+gametime
        
        if gamenametime in gametimeStorage:
            print("duplicate gametime at "+gamenametime)
        else:
            gametimeStorage.append(gamenametime)
        
        for i,line in enumerate(split):
            
            
            
            if line.find("Side pot")!=-1: #winner of side pot needs to be "won ($XX.xx)"  not "lost"
                print("Side pot on "+gametime)
            
            # currently this program cannot handle names with spaces...
            line=line.replace('CMU Brandon','CMUBrandon')
            line=line.replace('Princess Blossom','PrincessBlossom')
            
            if state<2:
                state+=1
            elif state==2:
                #print('state is 2')
                if uncalledBetProg.match(line):
                    #print('line matched')
                    line=uncalledBetProg.sub(r'Uncalled bet (\1)',line)
                    #print(line)
                elif line=='*** SUMMARY ***':
                    state=3
                elif line.find('***')==-1:
                    line=line.replace(', and is all in','')
                    line=line.replace('posts $','posts big blind $')
                    line=blindProg.sub(r'posts \1 blind',line)
                    line=moneyProg.sub(r'\1 in chips\2',line)
                    line=line.replace('straddles for','posts straddle')
                    
                    '''if line.find('straddle') and straddleFlag:
                        print("Straddle on "+gametime)
                        straddleFlag=False'''
                    
                    if line.find(':')==-1 and line.find('Dealt to')==-1:
                        #print('found no : ')
                        #if prog6.search(line):
                            #print(prog6.search(line).group(1))
                        line=prog6.sub(r'\1: ',line)
                        
                    if seatCheckProg.match(line):
                        tempString=seatCheckProg.match(line).group(1)
                        #print(tempString)
                        seatStringStorage.append(tempString) #append seat to storage
                        
                    if doubleBlindProg.match(line):
                        tempString=doubleBlindProg.match(line).group(1)
                        #print(tempString)
                        if tempString in blindStringStorage:
                            print('double blind post '+tempString+" "+gametime)
                            blindDeletion.append(tempString)
                            
                        else:
                            blindStringStorage.append(tempString)
                        
                        
                        
            # code to eliminate any people who left their seat.
            elif state==3:
                if seatCheckProg.match(line):
                    line=seatCheckProg.sub(r'Seat '+str((int(seatCheckProg.match(line).group(1))+1)),line)
                    
                if seatCheckProg.match(line):
                    try:
                        tempString=seatCheckProg.match(line).group(1)
                        #print(tempString)
                        seatStringStorage.remove(tempString)
                    except:
                        print("possible issue with new player added on gametime "+gametime)
            
            split[i]=line #put lines into the splits
            
            
            
        if len(seatStringStorage)!=0:
            #print("DO X-1! players not removed: "+str(seatStringStorage)+" "+gametime)
            for num in seatStringStorage:
                progNotRemoved=re.compile(r'^(Seat '+num+r': \S+ \(\$\S+ in chips\))') # find the players sitting out
                #progNotRemoved=re.compile('^(Seat '+num+': \S+ \(.*in chips.*)') # find the players sitting out
                for line in list(split):
                    if progNotRemoved.search(line):
                        split.remove(line)
        if len(blindDeletion)!=0:
            for string in blindDeletion:
                progDelete=re.compile('^'+string+': posts')
                for line in list(split):
                    if progDelete.search(line):
                        split.remove(line)
                        break
            
        #print(blindStringStorage)
    return splitList

if __name__ =='__main__':

    # the name of the file to process.
    fileName=sys.argv[1]

    #open the file to extract text.
    file = open(fileName)
    delim="Bluff Avenue Game"

    #the list of hands, delimited.
    rawList = [delim+e for e in file.read().split("\n"+delim) if e]
    file.close()

    #hack for the rawList, extra delim removed
    rawList[0]=str(rawList[0]).replace(delim,"",1) 

    handList=set()
    for raw in rawList:
        handList.add(Hand(raw))
    # print(len(handList))

    splitList=[]
    for hand in rawList:
        splitList.append(hand.splitlines()) #split_list is a list of lists: each hand split into lines.
    #print(split_list[0])

    splitList=modifySplitList(splitList)
                
    #print(split_list)
    directory=[]
    output=None
    if system().lower() == 'windows':
        directory = fileName.split("\\")
        fileName=directory[len(directory)-1]
        output=open(r'out\out'+fileName,'w')
    else:
        directory = fileName.split("/")
        fileName=directory[len(directory)-1]
        output=open(r'out/out'+fileName,'w')

    #output2=open('..\..\Desktop\PS_HH\Nicholas\out'+filename,'w')
    for split in splitList:
        for line in split:
            output.write(line+'\n')
    output.close()
       
