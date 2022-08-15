def plotGraph(noOfHeads, listTime):
    # Import matplotlib to plot and save graphs
    import matplotlib.pyplot as plt
    
    # plots the number of heads against time
    plt.plot(listTime, noOfHeads, linewidth=2.0)
    plt.xlabel("Time")
    plt.ylabel("Number Of Heads")
    plt.show()
