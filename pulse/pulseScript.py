import os
import getpass



from pulse.pulseShapeDiscrim import doExtractAndSavePulseInfo, loadSavedGroupsOfPulses, removeOutlierPulses,\
    makeGroupHistograms, doFindHistPeaks, filterPulsesForGroups, makeCharacteristicFunction,\
    loadSavedPulseWithCharPulseData, calcSI, makeSIhistograms

if __name__ == '__main__':
    # Initial step for raw data conversion. This processed data ia then loaded in step2
    preformStep1 = True

    # Steps 3-7 require the data to be load from step 2.
    if True:
        preformStep2 = True # load the data
        preformStep3 = True # remove outliers from the data sets
        preformStep4 = True # histograms after outlier removal
        preformStep5 = True # filter the data
        preformStep6 = True # histograms after filter tool
        preformStep7 = True # make the characteristic functions from the remaining data
    else:
        preformStep2 = False
        preformStep3 = False
        preformStep4 = False
        preformStep5 = False
        preformStep6 = False
        preformStep7 = False
    # After running steps 1-7 once, you can start from step 8
    if True:
        preformStep8 = True
        preformStep9 = True
    else:
        preformStep8 = False
        preformStep9 = False

    # After running steps 1-9 once, you can start from step 10
    preformStep10 = True
    """
    Default is True. If 'False' the code will run without text output unless something unexpected happens.
    the definition of the word verbose (adjective) is 'using or expressed in more words than are needed.'
    """
    verbose = True

    ####################
    ####################
    ###### Step 1 ######
    ####################
    ####################
    """
    Process all and save the results for all pulse data in folders in folderList
    """
    # folderList = [
    #     'CHC alpha_gamma traces']
    folderList = ['CHC alpha traces',
                  'CHC alpha traces thrsh 180',
                  'CHC alpha_gamma traces',
                  'CHC gamma traces']

    """
    This is the location where the folders with pulse data should be stored on your computer.
    Enter your user name and where the data is located on you computer here.
    For a windows computer the use '\\' for a mac or unix machine use '/'.

    """
    if getpass.getuser() == "chw3k5": # Caleb Wheeler's User name on his own computer
        parentFolder = '/Users/chw3k5/Desktop/new CHC traces'
    elif getpass.getuser() == "youUserName":

        parentFolder = 'Where\\the\\data\\is\\on\\your\\windows\\computer'
    else:
        parentFolder = ''
        print getpass.getuser(), 'is your user name.'


    """
    The output folder is where the process data will be stored on you computer. The default process puts it
    within the 'parentFolder'.
    """
    outputFolder = os.path.join(parentFolder, 'output')
    # automatically create the output folder is it does not yet exist on your computer
    if not os.path.exists(outputFolder):
        os.mkdir(outputFolder)

    """
    This option lets you apply a box car convolution to smooth the pulse data before is it trimmed to the peak.
    smooth smoothChannels=1 DOES NOT apply a convolution and is the default
    """
    smoothChannels = 1


    """
    # When processing the data you can fit with a sum of exponent in the form
    # Amp1 * exp(- x / tau1) + Amp1 * exp(- x / tau1) + ...
    # these can be done currently with 1, 2, 3, or 4 exponential in the sum
    """
    numOfExponents = 2


    """
    These are the data types that will be saved in the output folder after processing.
    Current options include:
    'arrayData' the original array of Voltage data from read in
    'xData' the original array of time data from read in
    'rawDataFileName' the filename that the data was read in from, save as a string of text

    'smoothedData' a boxcar smoothed version of the original array
        (available only if smoothChannels > 1) saves an array of floats
    'keptData' the voltage data that has been trimmed to exclude the baseline data before the pulse
    'keptxData' the corresponding time data that has been trimmed to exclude the baseline data before the pulse

    'integral' the calculated integral of the pulse voltage * time, saves a single float value
    'fittedCost' This is the 'cost' of the fitting function, lower cost is a better fit, saves a single float value

    fittingFunction = Amp1 * exp(- x / tau1) + Amp2 * exp(- x / tau2) + Amp3 * exp(- x / tau3) + Amp4 * exp(- x / tau4)
    'fittedAmp1', amplitude of the first component in the sum of exponential fitting functions, saves a single float value
    'fittedTau1', the time constant of value of the first component in the sum of exponential fitting functions, saves a single float value
    'fittedAmp2', only available if numOfExponents >= 2
    'fittedTau2', only available if numOfExponents >= 2
    'fittedAmp3', only available if numOfExponents >= 3
    'fittedTau3', only available if numOfExponents >= 3
    'fittedAmp4', only available if numOfExponents >= 4
    'fittedTau4', only available if numOfExponents >= 4

    """
    pulseDataTypesToSave = ['integral', 'fittedCost', 'rawDataFileName', 'deltaX', 'keptData']
    for index in range(numOfExponents):
        pulseDataTypesToSave.extend(['fittedAmp' + str(index + 1), 'fittedTau' + str(index + 1)])
    if verbose:
        print 'The data types to save are:', pulseDataTypesToSave


    """
    Default should be False, as it will take too much time to look at a plot for each individual pulse.
    However this is a great way to visualize the individual pulse data, or test to see how changes in
    the pulse pipeline are being implements
    """
    showTestPlots_Pulses = False


    """
    default should be False. This will limit the number of file to be read in, currently limited to 13 pulse files.
    This can be useful when making changes to the read in, but you do not want to wait for the time it takes to read
    in 1000's of files.
    """
    testModeReadIn = False

    if preformStep1:
        if verbose:
            print "Preforming Step 1: Processing raw Pulse Data."
        groupDict = doExtractAndSavePulseInfo(parentFolder,
                                              folderList,
                                              outputFolder,
                                              pulseDataTypesToSave,
                                              smoothChannels=smoothChannels,
                                              numOfExponents=numOfExponents,
                                              showTestPlots_Pulses=showTestPlots_Pulses,
                                              testModeReadIn=testModeReadIn,
                                              verbose=verbose)
    ####################
    ####################
    ###### Step 2 ######
    ####################
    ####################
    """
    Load in the saved data. If you are not loading the whole pulse than this goes much faster then the pulse
    processing function.
    """



    """
    The option for pulseDataTypesToLoad are the same options as pulse data type to save.
    This data must be saved first before it can be loaded. So it can be set equal to
    'pulseDataTypesToSave' for most purposes.
    """
    pulseDataTypesToLoad = pulseDataTypesToSave
    if preformStep2:
        if verbose:
            print "Preforming Step 2: Loading processed pulse data."
        groupDict = loadSavedGroupsOfPulses(outputFolder,
                                            folderList,
                                            pulseDataTypesToLoad)

    ####################
    ####################
    ###### Step 3 ######
    ####################
    ####################
    """
    This is used to remove outliers from the data. This uses a method that is simple but effective for pulses that
    have astronomically high values. We use the standard deviation from the median instead of the mean to make us
    able to remove data the has values equal to inanity, float('inf), or that are so high they would skew the mean.
    Each data type is in a tuple with the name and the value of standard deviation from the median such as
    ('cost', 1.37)
    This is available only for things that are one entry per pulse such as
    'integral', 'fittedCost', 'fittedAmp1', 'fittedTau1', 'fittedAmp2' ...
    see the documentation for pulseDataTypesToSave for more information on these types.
    """
    pulseDataTypesToRemoveOutliers = [('integral', float(100)), ('fittedCost', float(4)),
                                      ('fittedAmp1', float(10)), ('fittedTau1', float(10)),
                                      ('fittedAmp2', float(10)), ('fittedTau2', float(10)),
                                      ('deltaX', float(10))]

    if preformStep3:
        if preformStep2:
            if verbose:
                print 'Preforming step 3: Removing outliers pulses from sets of pulse data. '
            groupDict = removeOutlierPulses(groupDict, pulseDataTypesToRemoveOutliers)
        else:
            print "The data needs to be loaded in step 2 before step 3 can be completed. Try again."



    ####################
    ####################
    ###### Step 4 ######
    ####################
    ####################
    """
    In this step we make histograms for the data types that are one value per pulse. This can help us to make
    choices about what the characteristic values for sets of pulses.
    """

    """
    pulseDataForHistogram, is list of the data type that are to be made into histograms.
    This is available only for things that are one entry per pulse such as
    'integral', 'fittedCost', 'fittedAmp1', 'fittedTau1', 'fittedAmp2' ...
    see the documentation for pulseDataTypesToSave for more information on these types.
    """
    pulseDataForHistogram = []
    for (pulseType, number) in  pulseDataTypesToRemoveOutliers:
        pulseDataForHistogram.append(pulseType)


    """
    This is the location of the folder where the histogram plots are stored. If it does not exist it will
    be made automatically at this point.
    """
    plotFolder = os.path.join(parentFolder, 'plots')
    if not os.path.exists(plotFolder):
        os.mkdir(plotFolder)

    """
    showHistPlots toggles is the histogram plots are to be shown in a pop up window.
    """
    showHistPlots = False


    """
    saveHistPlots toggles is the histogram plots save it the folder 'plotFolder'.
    """
    saveHistPlots = True


    """
    Specifies the number of bins for all histograms.
    """
    histBins = 20

    if preformStep4:
        if preformStep2:
            if verbose:
                print "Doin' step 4: Making histograms of the pulse data."
            outHistDict = makeGroupHistograms(groupDict,
                                              pulseDataForHistogram,
                                              plotFolder,
                                              histBins=histBins,
                                              saveHistPlots=saveHistPlots,
                                              showHistPlots=showHistPlots,
                                              verbose=verbose)
        else:
            print "The data needs to be loaded in step 2 before step 4 can be completed. Try again."



    ####################
    ####################
    ###### Step 5 ######
    ####################
    ####################
    """
    Filter the data based on one of the data types.
    pulseFilterDict is a dictionary for which each element is a list of tuples. {} denotes a dictionary.
    The keys of this dictionary must be the elements of folder list.
    These are the same keys that are use to access the lists of pulses for the dictionary

    The '[]' designate it a list. Each component tuple,
    ('pulseType', filterMin, filterMax) where 'pulseType' where is a string, filterMin is a float, and
    filterMax is a float. Separate the Tuples with a ','
    """
    pulseFilterDict = {}
    pulseFilterDict['CHC alpha traces'] = [('integral', float(-1.5e-6), float(-1.2e-6))]
    pulseFilterDict['CHC gamma traces'] = [('integral', float(-7.3e-7), float(-6.7e-7))]

    if preformStep5:
        if preformStep2:
            if verbose:
                print "Let's start Step 5: Filtering pulses."
            groupDict = filterPulsesForGroups(groupDict, pulseFilterDict)
        else:
            print "The data needs to be loaded in step 2 before step 5 can be completed. Try again."


    ####################
    ####################
    ###### Step 6 ######
    ####################
    ####################
    """
    Make a histogram for the filtered Pulses
    """
    if preformStep6:
        if preformStep2:
            if verbose:
                print 'Step 6: Making histograms of the pulse data after filtering in step 5.'
            outHistDict = makeGroupHistograms(groupDict,
                                              pulseDataForHistogram,
                                              plotFolder,
                                              histBins=histBins,
                                              saveHistPlots=saveHistPlots,
                                              showHistPlots=showHistPlots,
                                              verbose=verbose)
        else:
            print "The data needs to be loaded in step 2 before step 6 can be completed. Try again."

    ####################
    ####################
    ###### Step 7 ######
    ####################
    ####################
    """
    Make and characteristic function for the remaining pulses in the group.
    """
    characteristicFunctionFolders = pulseFilterDict.keys()
    if preformStep7:
        if preformStep2:
            if verbose:
                print 'Step 6: Calculating and saving the characteristic functions used calculate The shaping indicator (SI).'
            groupDict = makeCharacteristicFunction(groupDict,
                                                   characteristicFunctionFolders,
                                                   outputFolder,
                                                   verbose=verbose)
        else:
            print "The data needs to be loaded in step 2 before step 7 can be completed."
            print "Specifically you need the data type 'keptData' for this calculation."

    ####################
    ####################
    ###### Step 8 ######
    ####################
    ####################


    """
    Load Saved data and load the characteristic functions.
    This is a break point and does not need the previous step in the all the data you need has all ready be saved.
    This is where a fresh data read in occurs.
    """
    if preformStep8:
        if verbose:
            print "Oooo-wheeee Step 8: Load all the data back into memory (even what was previously filtered out)."
        groupDict = loadSavedPulseWithCharPulseData(outputFolder,
                                                    folderList,
                                                    pulseDataTypesToLoad,
                                                    characteristicFunctionFolders)



    ####################
    ####################
    ###### Step 9 ######
    ####################
    ####################


    """
    And test the shaping indicator (SI) on the alpha_gamma data.
    """


    """
    This toggles a test plot to look ar the two characteristic functions, there fitting (if use useFittedFunction
    is True) that goes into making the weighting function P(t).
     P(t) = (f1(t) - f2(t)) /  (f1(t) + f2(t))
    """
    charArrayTestPlots=False


    """
    This could totally be determined at another point in the code. For convenience (laziness) I am naming it here
    this the time spacing of the pulse data in seconds. Last I set it it was 10 nS
    """
    xStep=float(1.0e-8)


    """
    There can be a lot more time series data than is needed data can be far more that what is needed.
    Cut off the tail of the data for all the data past 'xTruncateAfter_s' seconds from the peak
    """
    xTruncateAfter_s = float(2.5e-4)


    """
    If True, then for the calculation of P(t), f1(t) and f2(t) will be the best fitted sum of exponential functions.
    The number of exponentials used for fitting the sum is determined by numOfExponents.
    """
    useFittedFunction=True

    if preformStep9:
        if verbose:
            print "Here are, step number 9: Calculate the Shape Indicator (SI) and save it to a file."
        groupDict, charPulseDict1, charPulseDict2 = calcSI(groupDict,
                                                           characteristicFunctionFolders,
                                                           outputFolder,
                                                           charArrayTestPlots=charArrayTestPlots,
                                                           xStep=xStep,
                                                           xTruncateAfter_s=xTruncateAfter_s,
                                                           useFittedFunction=useFittedFunction,
                                                           numOfExponents=numOfExponents,
                                                           verbose=verbose)



    #####################
    #####################
    ###### Step 10 ######
    #####################
    #####################
    """
    Make a histogram for the shaping index and see how well it preformed.
    """


    """
    SI_histBins is the number of bin for the SI histogram
    """
    SI_histBins = 200

    if preformStep10:
        if verbose:
            print 'Finally, Step 10: Making a histogram for each set of pulses showing the shaping indicator (SI)'
        groupDict = loadSavedGroupsOfPulses(outputFolder,
                                            folderList,
                                            ['SI'])
        histogramDict = makeSIhistograms(groupDict,
                                         plotFolder,
                                         histBins=SI_histBins,
                                         saveHistPlots=saveHistPlots,
                                         showHistPlots=showHistPlots,
                                         verbose=verbose)
