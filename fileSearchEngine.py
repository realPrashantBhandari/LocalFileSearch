import os
import pickle
import PySimpleGUI as sg 

class Gui:
    def __init__(self):
        self.layout = [
                        [
                            sg.Text('Search Term',size=(10,1)), 
                            sg.Input(size=(40,1), focus=True, key = "TERM"),
                            sg.Radio('Contains', group_id='searchType', key = "CONTAINS",default=True),
                            sg.Radio('Starts With', group_id='searchType', key = "STARTSWITH"),
                            sg.Radio('Ends With', group_id='searchType', key = "ENDSWITH")
                        ],
                        [
                            sg.Text('Search Path',size=(10,1)),
                            sg.Input('D:/',size=(40,1), key = "PATH"),
                            sg.FolderBrowse('Browse',size=(10,1)),
                            sg.Button('Re-Index',size=(10,1), key = "REINDEX"),
                            sg.Button('Search',size=(10,1), bind_return_key=True, key = "SEARCH")
                        ],
                        [
                            sg.Output(size=(100,30), key='OUTPUT')
                        ]
                    ]
        # Create the window
        self.window = sg.Window('Local File Search').Layout(self.layout)

class SearchEngine:
    def __init__(self):
        self.fileIndex = []
        self.results = []
        self.totalMatches = 0
        self.totalFilesSearched = 0

    def createNewIndex(self, values):
        #create new Index with the selected root directory
        self.fileIndex.clear()
        rootPath = values['PATH']
        for root, dirs, files in os.walk(rootPath):
            if files:
                self.fileIndex.append([root, files])

        #saving the new index
        with open ('fileIndex.pkl','wb') as f:
            pickle.dump(self.fileIndex, f)


    def loadIndex(self):
        # load already created index
        try:
            with open('fileIndex.pkl','rb') as f:
                self.fileIndex=pickle.load(f)
        except:
            self.fileIndex = []


    def search(self,values):
        # search the index for the term
        self.results.clear()
        self.totalFilesSearched = 0
        self.totalMatches = 0
        term = values['TERM']

        #search function
        for path, files in self.fileIndex:
            for xfile  in files:
                self.totalFilesSearched +=1
                if (values['CONTAINS'] and term.lower() in xfile.lower() or 
                   values['STARTSWITH'] and xfile.lower().startswith(term.lower()) or
                   values['ENDSWITH'] and xfile.lower().endswith(term.lower())):

                   resultPath = path.replace('\\','/') +'/'+ xfile
                   self.results.append(resultPath)
                   self.totalMatches +=1

                else:
                    continue
        
        #saving the results to a text file
        with open ('searchResults.txt','w') as f:
            for entry in self.results:
                f.write(entry+ '\n')

         
def main():
    g=Gui()
    se = SearchEngine()
    se.loadIndex()

    while True:
        event, values = g.window.Read()
        
        if event is None:
            break

        if event == 'REINDEX':
            se.createNewIndex(values)
            print()
            print(' New Index has been created')
            print()
             
        if event == 'SEARCH':
            
            se.search(values)

            for result in se.results:
                print(result)
            
            print()
            print(">> Searched {:,d} records and found {:,d} matches".format(se.totalFilesSearched, se.totalMatches))
            print(">> Results saved in working directory as searchResults.txt.")
            print()


if __name__ == '__main__':
    print('Starting program...')
    main()