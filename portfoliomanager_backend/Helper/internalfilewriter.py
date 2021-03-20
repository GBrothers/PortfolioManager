

def write(key, content, postfix=".json", replace=True):

    filename = "PortfolioManager_Backend/outputfiles/" + key + postfix
    result_file = open(filename, "w" if replace else "a")
    result_file.write(str(content))
    result_file.close()
    print(filename + (" replaced by " if replace else " appendend with ") + "new Data!")
