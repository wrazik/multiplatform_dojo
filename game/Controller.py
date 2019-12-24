# COMMUNICATION (MAIN LOOP FROM SERVER POV)
# 1. send current state to all players
# 2. animate current state
# 3. read inputs from all players
# 4. update internal state
# Notes:
# * between steps 1 and 3 clients have under 1 second to respond
# * assumption is that internal state and updated state broadcast (steps 1 and 3)
#   can be done in under a frame (16ms) - this way animation is smoots with tanks
#   taking a second to perform any move
# * bullets require special consideration as they can't be hit-scan (TBD)
#
# GAME STATE REPRESENTATION (comments start with --)
# 0 -- whether game is running or not (0 = idle, 1 = running)
# 16 16 -- map dimensions (w h; currently always 16x16)
# 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 -- h lines with trees (1 = obstacle)
# ...
# 0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 1
# 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1 1
# you 1 4 left -- receivers position (x y) and direction (up down left right)
# enemy 10 5 left -- first enemy
# enemy 3 14 left -- another enemy (up to 4 in total)
#
# Note: if enemy is dead it won't show up in the state message

# moves are: left, right, forward, backward, idle, fire
class Controller(object):
    def __init__(self):
        pass

    def next(self):
        return "idle"


class DummyController(Controller):
    def __init__(self):
        super().__init__()
        self.index = 0

    def next(self):
        sequence = ["forward","right","forward","right","forward","left","backward","left"]
        move = sequence[self.index % len(sequence)]
        self.index += 1
        return move
