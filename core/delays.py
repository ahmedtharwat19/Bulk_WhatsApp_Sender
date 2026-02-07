import random, time

def smart_delay(base=3):
    delay = random.uniform(base, base + 4)
    time.sleep(delay)
