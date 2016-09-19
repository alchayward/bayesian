from collections import deque
event_queue = deque()

# This is dumb. where do the events come in?
if __name__ == '__main__':
    while True:
        try:
            event_queue.pop(0)()
        except:
            pass


