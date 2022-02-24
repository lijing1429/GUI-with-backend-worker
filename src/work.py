import threading
import time

class MyWork:

    def __init__(self, maxvalue, setprogress, setresult):
        '''maxvalue is given by the GUI
        setprogress/ setresult is a function. calling these functions will add an event to the main loop, and update the value.
        '''
        self.maxvalue = maxvalue
        self.setprogress = setprogress
        self.setresult = setresult
        
        self.interrupt = False
        self.workstarted = False

    def start(self):
        '''start working. if the application has started, then do nothing.'''
        if self.workstarted:
            pass
        else:
            self.workthread = threading.Thread(target=self.dowork)
            self.workthread.start()
            self.workstarted = True

    def stop(self):
        '''interrupt work: if work starting and interrupt is true, then the this thread should be closed once the main thread has been closed.'''
        if self.workstarted:
            self.interrupt = True
            self.workthread.join()

    def dowork(self):
        '''caculate the data and return the result.'''
        print('work starts...')
        result = 0
        for i in range(self.maxvalue + 1):
            result += i
            self.setprogress(int(100 * i / self.maxvalue + 0.5))
            time.sleep(0.1)
            if self.interrupt:
                print('work interrupted...')
                return
        self.setresult(result)
        print('work ends...')

