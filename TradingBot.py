from main import *

def main():
    # firstly, check if the market has closed
    # we enter on the close of the day

    hasExited = False
    account = login()

    while not hasExited:
        inp = input("Press S to run strategy, P to see performance, Q to quit: ")

        if inp == "Q":
            hasExited = True
            continue

        if inp == "P":
            seePerformance(account)
            continue

        if inp == "S":
            runStrategyAtClose(account)
            



if __name__ == "__main__":
    main()
