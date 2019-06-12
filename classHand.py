class Hand:
    def __init__(self,raw):
        self.raw=raw
        self.split=raw.splitlines
        self.processOnInit()

    def __hash__(self):
        return hash(self.split[0])

    def __eq__(self,other):
        return self.split[0]==other.split[0]  
    
    def processOnInit(self):
        return None