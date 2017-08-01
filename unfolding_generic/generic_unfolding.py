'''
This code will use my unfoldingTools to create the necessary files to use maxed
and gravel for unfolding a spectrum using generic bonner response functions.
'''

from unfoldingTools import BonnerSphereTools

unfold = BonnerSphereTools()

unfold.sphereIDs = []


unfold.sphereSizes = sphereSizes
unfold.responseData = responseData
unfold.responseError = responseError
unfold.extraError = extraError
unfold.correctionFactor = correctFactor



unfold.rfErgEdges = rfErgEdges
unfold.responses = responses
unfold.rfErgUnits = rfErgUnits



unfold.mode = mode
unfold.dsErgUnits = dsErgUnits
unfold.dS = defaultSpectrum
unfold.dsErr = defaultSpectrumError
unfold.dsErgEdges = dsErgEdges



unfold.ibuName = ibuName
unfold.fmtName = fmtName
unfold.fluName = fluName
unfold.outName = outName
unfold.finalChiSqr = finalChiSqr
unfold.temp = temp
unfold.solnStructure = solnStructure
unfold.solnRepresentation = solnRepresentation
unfold.scaling = scaling


