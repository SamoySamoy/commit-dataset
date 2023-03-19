from typing import List
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        res = []
        tie = False
        start = 10001
        end = -1
        l = len(intervals)
        intervals.append([10001, 10001]) # add this to index i + 1 in the loop
        for i in range(0, l):
            if intervals[i][0] < start:
                start = intervals[i][0]
            if intervals[i][1] > end:
                end = intervals[i][1]
            if tie == True:
                if end < intervals[i + 1][0] or start > intervals[i + 1][1]:
                    res.append([start, end])
                    start = 10001
                    end = -1
                    tie = False
            else:
                if end < intervals[i + 1][0] or start > intervals[i + 1][1]:
                    res.append(intervals[i])
                else:
                    tie = true

        return res
    intervals = [[2,3],[4,5],[6,7],[8,9],[1,10]]
    print(merge(self=0, intervals=intervals))

class Sol:
    def merge(self, intr: List[List[int]]) -> List[List[int]]:
        i=0
        intr.sort()
        if len(intr)==0:
            return []
        elif len(intr)==1:
            return list(intr)
        else:
            while i<len(intr)-1:
                if(intr[i][1]>=intr[i+1][0] and intr[i][1]>=intr[i+1][1]):
                    intr.append([intr[i][0],intr[i][1]])
                    intr.remove(intr[i])
                    intr.remove(intr[i])
                    intr.sort()

                elif(intr[i][1]>=intr[i+1][0] and intr[i][1]<intr[i+1][1]):
                    intr.append([intr[i][0],intr[i+1][1]])
                    intr.remove(intr[i])
                    intr.remove(intr[i])
                    intr.sort()
                else:
                    i+=1
            return intr