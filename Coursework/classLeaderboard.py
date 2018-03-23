import merge_sort,radix_sort,csv

class MyLeaderboard():
    def __init__(self,file):
        self.save_file = file
        self.leaderboard = None
        self.sort_list = None
        
    def loadLeaderboard(self):
        scores_file = open(self.save_file)
        scores = csv.reader(scores_file,delimiter=',')
        lb = []
        for score in scores:
            lb.append(score)
        scores_file.close()
        self.leaderboard = lb

    def appendScore(self,fn,ln,sc):
        scores = open(self.save_file,'a',newline="")
        writer=csv.writer(scores)
        writer.writerow([fn,ln,sc])
        scores.close()

    def firstname(self):
        self.sort_list = merge_sort.mergesort(self.leaderboard,0)
    def surname(self):
        self.sort_list = merge_sort.mergesort(self.leaderboard,1)
    def score(self):
        self.sort_list = radix_sort.radix(self.leaderboard)[::-1]
    def recent(self):
        self.sort_list = self.leaderboard

    def getSortedList(self,sort_by):
        if sort_by == 1: self.firstname()
        elif sort_by == 2: self.surname()
        elif sort_by == 3: self.score()
        elif sort_by == 4: self.recent()
        return self.sort_list
        
