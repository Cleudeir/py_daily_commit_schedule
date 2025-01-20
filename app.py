

import os
from scr.getCommitSchedule import getCommitSchedule
from scr.getReport import getReport


def main():
    if not os.path.exists("output"):
     os.makedirs("output")
    getCommitSchedule()
    getReport()

if __name__ == "__main__":
    main()