class MyStack():
    def __init__(self):
        self.size = 5
        self.stack = [0 for i in range(self.size)]
        self.front = -1
        self.inStack = 0

    def add(self,item):
        if self.front != self.size-1:
            if self.inStack < 5:
                self.inStack+=1
            self.front = (self.front+1) % self.size
            self.stack[self.front] = item
        else:
            self.inStack-=1
            self.front = -1
            self.add(item)
            
    def remove(self):
        empty = self.isEmpty()
        if not empty:
            self.inStack-=1
            self.front = (self.front-1) % self.size
            return self.stack[(self.front+1) % self.size]
        else:
            return False

    def isEmpty(self):
        return (self.inStack == 0)

