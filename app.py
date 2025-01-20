

import os
from src.getCommitSchedule import getCommitSchedule
from src.getReport import getReport


def main():
    if not os.path.exists("src/output"):
     os.makedirs("src/output")
    getCommitSchedule()
    getReport()

if __name__ == "__main__":
    main()