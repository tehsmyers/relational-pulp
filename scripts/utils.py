import time


class Timer:
    def __enter__(self):
        self.start = time.time()
        return self
            
    def __exit__(self, *args):
        elapsed = time.time() - self.start
        print('time: {} seconds'.format(elapsed))

timer = Timer()
