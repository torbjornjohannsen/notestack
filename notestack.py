#!/home/tb/dev/notestack/bin/python3
import argparse
import pickle
import heapq
import os 
appdatapath = os.path.expanduser('~/.notestack/data')

class note: 
    def __init__(self, link : str, priority: int, message: str=None):
        self.link = link 
        self.priority = priority
        self.message = message 
    
    def __repr__(self):
        return f"{self.link} {{ {self.message} }}" if self.message != None else f"{self.link}"
    
    def __lt__(self, other: "note") -> bool: 
        return self.priority > other.priority
 
# import data


def saveNotes(notesHeap : list[note]): 
    with open(appdatapath, 'wb+') as file: 
        pickle.dump(notesHeap, file)

def loadNotesHeap() -> list[note]: 
    if not os.path.exists(appdatapath): 
        
        return []
    with open(appdatapath, 'rb') as file: 
        notes = pickle.load(file)
    if notes == None: 
        return []
    return notes 


def add(args): 
    newNote = note(args['l'], args['p'], args['m'])
    
    allNotes = loadNotesHeap()
    heapq.heappush(allNotes, newNote)

    saveNotes(allNotes)

def top(args):
    allNotes = loadNotesHeap()

    if(len(allNotes) < 1): 
        print("No available notes")
        return

    print(allNotes[0])
    if args['pop'] and len(allNotes) > 0: 
        heapq.heappop(allNotes)
        saveNotes(allNotes)
    

def many(args):
    allNotes = loadNotesHeap() 

    if(len(allNotes) < 1): 
        print("No available notes")
        return

    if args['all']:
        for note in allNotes: 
            print(note) 
        allNotes = []
    else: 
        for i in range(len(heapq.nsmallest(args['n'], allNotes))): 
            print(heapq.heappop(allNotes))
    
    if args['pop']: 
        saveNotes(allNotes)
    

parser = argparse.ArgumentParser(
    prog="Note Stack",
    description="A priority queue of notes, who consist of a link as well as a message(and possible priority)"
)

ourputParent = argparse.ArgumentParser(add_help=False)
ourputParent.add_argument('--pop',action='store_true', help="Remove the top level")

subparsers = parser.add_subparsers()

addParser = subparsers.add_parser(name="add")
topParser = subparsers.add_parser(name="top", parents=[ourputParent])
manyParser = subparsers.add_parser(name="many", parents=[ourputParent])

addParser.add_argument('-l', type=str, help="Link, the required top level attribute of a note in the stack", required=True)
addParser.add_argument('-p', type=int, default=1, help="priority, by defauly 1. Priority is sorted high to low")
addParser.add_argument('-m', type=str, help="Message, an optional message to add to the entry")
addParser.set_defaults(func=add)

topParser.set_defaults(func=top)

manyParser.add_argument('--all', action='store_true', help="return all the notes")
manyParser.add_argument('-n', default=10, type=int,  help="How many values to return. Note that this is overriden by --all")
manyParser.set_defaults(func=many)



args = parser.parse_args()
args.func(vars(args))
