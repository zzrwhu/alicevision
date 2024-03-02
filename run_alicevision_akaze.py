#Original file from http://filmicworlds.com/blog/command-line-photogrammetry-with-alicevision/
#Re-edited by Zurong ZHANG 
#Supervisor: Dr. Adam A. Stokes 
#Soft System Group / The School of Engineering / The University of Edinburgh
#Date: 22/11/2021
#Discription:
#This is the Meshroom command line test with akaze pipeline.
#With the properties of ThisIsAGoodPipeline.mg in DropBox.
#Tree file path has been setted well.
#Step00 not changed

import sys, os
import shutil


def SilentMkdir(theDir):
	try:
		os.mkdir(theDir)
	except:
		pass
	return 0

def Run_00_CameraInit(baseDir,binDir,srcImageDir):
	SilentMkdir(baseDir + "/00_CameraInit")

	binName = binDir + "\\aliceVision_cameraInit.exe"

	dstDir = baseDir + "/00_CameraInit/"
	cmdLine = binName
	cmdLine = cmdLine + " --defaultFieldOfView 45.0 --verboseLevel info --sensorDatabase \"\" --allowSingleView 1"
	#UI cmd
	

	cmdLine = cmdLine + " --imageFolder \"" + srcImageDir + "\""
	#UIcmd
	#cmdLine = cmdLine + " --input \"" + dstDir + "viewpoints.sfm\""
	cmdLine = cmdLine + " --output \"" + dstDir + "cameraInit.sfm\""
	print(cmdLine)
	os.system(cmdLine)

	return 0

def Run_01_FeatureExtraction(baseDir,binDir, numImages):
	SilentMkdir(baseDir + "/01_FeatureExtraction") #make dir for run01

	srcSfm = baseDir + "/00_CameraInit/cameraInit.sfm" # file source 

	binName = binDir + "\\aliceVision_featureExtraction.exe" #commandLine 

	dstDir = baseDir + "/01_FeatureExtraction/"# generated file destination 

	cmdLine = binName #commandLine
	#add options here
	
	#UI cmd
	cmdLine = cmdLine + " --describerTypes akaze"
	cmdLine = cmdLine + " --describerPreset high --maxNbFeatures 0 --describerQuality high --contrastFiltering GridSort --relativePeakThreshold 0.01 --gridFiltering True --forceCpuExtraction True --maxThreads 0 --verboseLevel info "
	#range size seems to be the limitation of photo number?
	#cmdLine = cmdLine + " --rangeStart 0 --rangeSize 20"  
	########### what will rangesize influece and how to decide it? 
	#original one
	#cmdLine = cmdLine + " --describerTypes sift --forceCpuExtraction True --verboseLevel info --describerPreset normal"
	#cmdLine = cmdLine + " --rangeStart 0 --rangeSize " + str(numImages)
	
	#change the file path by setting dstDir
	cmdLine = cmdLine + " --input \"" + srcSfm + "\"" # input cmd
	cmdLine = cmdLine + " --output \"" + dstDir + "\""# output cmd

	#UI cmd
	#generating log file

	print(cmdLine)
	os.system(cmdLine)

	return 0

def Run_02_ImageMatching(baseDir,binDir):
	SilentMkdir(baseDir + "/02_ImageMatching") #make dir for run01

	srcSfm = baseDir + "/00_CameraInit/cameraInit.sfm" # file source 
	srcFeatures = baseDir + "/01_FeatureExtraction/" # features folders
	dstMatches = baseDir + "/02_ImageMatching/imageMatches.txt"

	binName = binDir + "\\aliceVision_imageMatching.exe"

	cmdLine = binName

	#UI cmd   
	cmdLine = cmdLine + " --method VocabularyTree"
	cmdLine = cmdLine + " --tree aliceVision/share/aliceVision/vlfeat_K80L3.SIFT.tree" 
	cmdLine = cmdLine + " --minNbImages 200"
	cmdLine = cmdLine + " --maxDescriptors 500 --verboseLevel info --weights "" --nbMatches 50 --nbNeighbors 50"
	#original 
	#cmdLine = cmdLine + " --minNbImages 200 --tree "" --maxDescriptors 500 --verboseLevel info --weights "" --nbMatches 50"
	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --featuresFolder \"" + srcFeatures + "\""
	cmdLine = cmdLine + " --output \"" + dstMatches + "\""

	print(cmdLine)
	os.system(cmdLine)

	return 0

def Run_03_FeatureMatching(baseDir,binDir):
	SilentMkdir(baseDir + "/03_FeatureMatching")

	srcSfm = baseDir + "/00_CameraInit/cameraInit.sfm"
	srcFeatures = baseDir + "/01_FeatureExtraction/" #featuresfolders
	srcImageMatches = baseDir + "/02_ImageMatching/imageMatches.txt" #image pairs list
	dstMatches = baseDir + "/03_FeatureMatching/"

	binName = binDir + "\\aliceVision_featureMatching.exe"
	#changed --describerTypes from sift to akaze
	cmdLine = binName
	cmdLine = cmdLine + " --verboseLevel info --maxMatches 0 --exportDebugFiles False --savePutativeMatches False --guidedMatching False"
	cmdLine = cmdLine + " --geometricEstimator acransac --geometricFilterType fundamental_matrix --maxIteration 2048 --distanceRatio 0.8"
	cmdLine = cmdLine + " --photometricMatchingMethod ANN_L2"
	
	#UI cmd
	cmdLine = cmdLine + " --geometricError 0.0 --knownPosesGeometricErrorMax 5.0 --crossMatching False --matchFromKnownCameraPoses False" 
	#cmdLine = cmdLine + " --rangeStart 0 --rangeSize 20"

	cmdLine = cmdLine + " --describerTypes akaze"
	cmdLine = cmdLine + " --imagePairsList \"" + srcImageMatches + "\""
	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --featuresFolders \"" + srcFeatures + "\""
	cmdLine = cmdLine + " --output \"" + dstMatches + "\""

	print(cmdLine)
	os.system(cmdLine)
	return 0

def Run_04_StructureFromMotion(baseDir,binDir):
	SilentMkdir(baseDir + "/04_StructureFromMotion")

	srcSfm = baseDir + "/00_CameraInit/cameraInit.sfm"
	srcFeatures = baseDir + "/01_FeatureExtraction/" #featuresFolders
	#srcImageMatches = baseDir + "/02_ImageMatching/imageMatches.txt"
	srcMatches = baseDir + "/03_FeatureMatching"
	dstDir = baseDir + "/04_StructureFromMotion"

	binName = binDir + "\\aliceVision_incrementalSfm.exe"
 
	cmdLine = binName
	cmdLine = cmdLine + " --describerTypes akaze --localizerEstimator acransac"
	cmdLine = cmdLine + " --observationConstraint Basic --localizerEstimatorMaxIterations 4096"
	cmdLine = cmdLine + " --localizerEstimatorError 0.0 --lockScenePreviouslyReconstructed false"
	cmdLine = cmdLine + " --useLocalBA True --localBAGraphDistance 1"
	cmdLine = cmdLine + " --maxNumberOfMatches 0 --minNumberOfMatches 0"
	cmdLine = cmdLine + " --minInputTrackLength 2 --minNumberOfObservationsForTriangulation 2" 
	cmdLine = cmdLine + " --minAngleForTriangulation 3.0 --minAngleForLandmark 2.0"
	cmdLine = cmdLine + " --maxReprojectionError 4.0 --minAngleInitialPair 5.0"
	cmdLine = cmdLine + " --maxAngleInitialPair 40.0 --useOnlyMatchesFromInputFolder False"
	cmdLine = cmdLine + " --useRigConstraint true --lockAllIntrinsics false"
	cmdLine = cmdLine + " --filterTrackForks false" 

	cmdLine = cmdLine + ' --interFileExtension .abc --initialPairB ""'
	cmdLine = cmdLine + " --verboseLevel info"
	cmdLine = cmdLine + ' --initialPairA ""'
	#cmdLine = cmdLine + " --initialPairA "" --initialPairB "" --interFileExtension .ply --useLocalBA True"
	#UI cmd   --initialPairB ""
	#cmdLine = cmdLine + " --observationConstraint Basic --localizerEstimatorMaxIterations 4096 --localizerEstimatorError 0.0 --minNumberOfMatches 0 --useRigConstraint True --lockAllIntrinsics False"
	#cmdLine = cmdLine + " --filterTrackForks False --interFileExtension .abc --initialPairA "" --useLocalBA True"

	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --featuresFolders \"" + srcFeatures + "\""
	cmdLine = cmdLine + " --matchesFolders \"" + srcMatches + "\""
	cmdLine = cmdLine + " --outputViewsAndPoses \"" + dstDir + "/cameras.sfm\""
	cmdLine = cmdLine + " --extraInfoFolder \"" + dstDir + "\""
	
	#cmdLine = cmdLine + " --output \"" + dstDir + "/bundle.sfm\""
	#UI cmd
	cmdLine = cmdLine + " --output \"" + dstDir + "/sfm.abc\""
	print(cmdLine)
	os.system(cmdLine)
	return 0

def Run_05_PrepareDenseScene(baseDir,binDir):
	SilentMkdir(baseDir + "/05_PrepareDenseScene")


	#srcSfm = baseDir + "/04_StructureFromMotion/cameras.sfm"
	#UI cmd
	srcSfm = baseDir + "/04_StructureFromMotion/sfm.abc"
	#srcSfm = baseDir + "/04_StructureFromMotion/bundle.sfm"
	dstDir = baseDir + "/05_PrepareDenseScene"

	binName = binDir + "\\aliceVision_prepareDenseScene.exe"

	cmdLine = binName
	cmdLine = cmdLine + " --outputFileType exr --saveMetadata True --saveMatricesTxtFiles False --evCorrection False --verboseLevel info"
	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --output \"" + dstDir +"\""
	#--rangeStart 0 --rangeSize 40
	print(cmdLine)
	os.system(cmdLine)
	return 0

def Run_06_CameraConnection(baseDir,binDir):
	SilentMkdir(baseDir + "/06_CameraConnection")

	srcIni = baseDir + "/05_PrepareDenseScene/mvs.ini"

	# This step kindof breaks the directory structure. Tt creates
	# a camsPairsMatrixFromSeeds.bin file in in the same file as mvs.ini
	binName = binDir + "\\aliceVision_cameraConnection.exe"

	cmdLine = binName
	cmdLine = cmdLine + " --verboseLevel info"
	cmdLine = cmdLine + " --ini \"" + srcIni + "\""

	print(cmdLine)
	os.system(cmdLine)
	return 0

def Run_07_DepthMap(baseDir,binDir,numImages,groupSize):
	SilentMkdir(baseDir + "/07_DepthMap")

	numGroups = int((numImages + (groupSize-1))/groupSize)
	#UI cmd
	srcIni = baseDir + "/04_StructureFromMotion/sfm.abc"
	imgDir = baseDir + "/05_PrepareDenseScene"
	#srcIni = baseDir + "/05_PrepareDenseScene/mvs.ini"
	binName = binDir + "\\aliceVision_depthMapEstimation.exe"
	dstDir = baseDir + "/07_DepthMap"
      
	cmdLine = binName
	cmdLine = cmdLine + " --downscale 2 --minViewAngle 2.0"
	cmdLine = cmdLine + " --maxViewAngle 70.0 --sgmMaxTCams 10"
	cmdLine = cmdLine + " --sgmWSH 4 --sgmGammaC 5.5"
	cmdLine = cmdLine + " --refineGammaP 8.0 --refineMaxTCams 6"
	cmdLine = cmdLine + " --refineNSamplesHalf 150 --refineNDepthsToRefine 31" 
	cmdLine = cmdLine + " --refineNiters 100 --refineWSH 3"
	cmdLine = cmdLine + " --refineSigma 15 --refineGammaC 15.5"
	cmdLine = cmdLine + " --refineUseTcOrRcPixSize False"
	cmdLine = cmdLine + " --exportIntermediateResults False --nbGPUs 0 --verboseLevel info"
	
	#--minNumOfConsistentCams 3 --minNumOfConsistentCamsWithLowSimilarity 4 --pixSizeBall 0 --pixSizeBallWithLowSimilarity 0 --computeNormalMaps false"
	
	cmdLine = cmdLine + " --input \"" + srcIni + "\""
	cmdLine = cmdLine + " --imagesFolder \"" + imgDir + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "\""


	for groupIter in range(numGroups):
		groupStart = groupSize * groupIter
		groupSize = min(groupSize,numImages - groupStart)
		print("DepthMap Group %d/%d: %d, %d" % (groupIter, numGroups, groupStart, groupSize))

		cmd = cmdLine + (" --rangeStart %d --rangeSize %d" % (groupStart,groupSize))
		print(cmd)
		os.system(cmd)


	#cmd = "aliceVision_depthMapEstimation  --sgmGammaC 5.5 --sgmWSH 4 --refineGammaP 8.0 --refineSigma 15 --refineNSamplesHalf 150 --sgmMaxTCams 10 --refineWSH 3 --downscale 2 --refineMaxTCams 6 --verboseLevel info --refineGammaC 15.5 --sgmGammaP 8.0 --ini \"c:/users/geforce/appdata/local/temp/MeshroomCache/PrepareDenseScene/4f0d6d9f9d072ed05337fd7c670811b1daa00e62/mvs.ini\" --refineNiters 100 --refineNDepthsToRefine 31 --refineUseTcOrRcPixSize False --output \"c:/users/geforce/appdata/local/temp/MeshroomCache/DepthMap/18f3bd0a90931bd749b5eda20c8bf9f6dab63af9\" --rangeStart 0 --rangeSize 3"
	#cmd = binName + " --sgmGammaC 5.5 --sgmWSH 4 --refineGammaP 8.0 --refineSigma 15 --refineNSamplesHalf 150 --sgmMaxTCams 10 --refineWSH 3 --downscale 2 --refineMaxTCams 6 --verboseLevel info --refineGammaC 15.5 --sgmGammaP 8.0 --ini \"c:/users/geforce/appdata/local/temp/MeshroomCache/PrepareDenseScene/4f0d6d9f9d072ed05337fd7c670811b1daa00e62/mvs.ini\" --refineNiters 100 --refineNDepthsToRefine 31 --refineUseTcOrRcPixSize False --output \"build_files/07_DepthMap/\" --rangeStart 0 --rangeSize 3"
	#cmd = binName + " --sgmGammaC 5.5 --sgmWSH 4 --refineGammaP 8.0 --refineSigma 15 --refineNSamplesHalf 150 --sgmMaxTCams 10 --refineWSH 3 --downscale 2 --refineMaxTCams 6 --verboseLevel info --refineGammaC 15.5 --sgmGammaP 8.0 --ini \"" + srcIni + "\" --refineNiters 100 --refineNDepthsToRefine 31 --refineUseTcOrRcPixSize False --output \"build_files/07_DepthMap/\" --rangeStart 0 --rangeSize 3"
	#print(cmd)
	#os.system(cmd)


	return 0

def Run_08_DepthMapFilter(baseDir,binDir):
	SilentMkdir(baseDir + "/08_DepthMapFilter")

	binName = binDir + "\\aliceVision_depthMapFiltering.exe"
	dstDir = baseDir + "/08_DepthMapFilter"
	#UI cmd
	srcIni = baseDir + "/04_StructureFromMotion/sfm.abc"
	#srcIni = baseDir + "/05_PrepareDenseScene/mvs.ini"
	srcDepthDir = baseDir + "/07_DepthMap"

	cmdLine = binName
	cmdLine = cmdLine + " --maxViewAngle 70.0 --minViewAngle 2.0"
	cmdLine = cmdLine + " --nNearestCams 10 --minNumOfConsistentCams 3"
	cmdLine = cmdLine + " --minNumOfConsistentCamsWithLowSimilarity 4"
	cmdLine = cmdLine + " --pixSizeBall 0 --pixSizeBallWithLowSimilarity 0"
	cmdLine = cmdLine + " --computeNormalMaps False --verboseLevel info"

	#cmdLine = cmdLine + " --rangeStart 0 --rangeSize 10"
	cmdLine = cmdLine + " --input \"" + srcIni + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "\""
	cmdLine = cmdLine + " --depthMapsFolder \"" + srcDepthDir + "\""

	print(cmdLine)
	os.system(cmdLine)
	return 0

def Run_09_Meshing(baseDir,binDir):
	SilentMkdir(baseDir + "/09_Meshing")

	binName = binDir + "\\aliceVision_meshing.exe"
	srcIni = baseDir + "/04_StructureFromMotion/sfm.abc"
	#srcIni = baseDir + "/05_PrepareDenseScene/mvs.ini"
	#srcDepthFilterDir = baseDir + "/08_DepthMapFilter"
	#srcDepthMapDir = baseDir + "/07_DepthMap"
	srcDepthMapDir = baseDir + "/08_DepthMapFilter"
	dstDir = baseDir + "/09_Meshing"  
	#--boundingBox not added###################################
	#--useBoundingBox false is not recogonized in the test
	#--densify false is ambiguous and matches '--densifyNbBack', '--densifyNbFront', and '--densifyScale'
	#--useBoundingBox and  --densify are not in the usage
	#--addMaskHelperPoints false  unrecognised option '--addMaskHelperPoints'
	cmdLine = binName
	cmdLine = cmdLine + " --estimateSpaceFromSfM True"
	cmdLine = cmdLine + " --estimateSpaceMinObservations 3 --estimateSpaceMinObservationAngle 10"
	cmdLine = cmdLine + " --maxInputPoints 50000000 --maxPoints 5000000"
	cmdLine = cmdLine + " --maxPointsPerVoxel 1000000 --minStep 2"
	cmdLine = cmdLine + " --partitioning singleBlock --repartition multiResolution"
	cmdLine = cmdLine + " --angleFactor 15.0 --simFactor 15.0"
	cmdLine = cmdLine + " --pixSizeMarginInitCoef 2.0 --pixSizeMarginFinalCoef 4.0"
	cmdLine = cmdLine + " --voteMarginFactor 4.0 --contributeMarginFactor 2.0"
	cmdLine = cmdLine + " --simGaussianSizeInit 10.0 --simGaussianSize 10.0"
	cmdLine = cmdLine + " --minAngleThreshold 1.0  --refineFuse True" 
	cmdLine = cmdLine + " --helperPointsGridSize 10"
	cmdLine = cmdLine + " --densifyNbFront 1 --densifyNbBack 1 --nPixelSizeBehind 4.0"
	cmdLine = cmdLine + " --fullWeight 1.0 --voteFilteringForWeaklySupportedSurfaces True"
	cmdLine = cmdLine + " --addLandmarksToTheDensePointCloud False --invertTetrahedronBasedOnNeighborsNbIterations 10"
	cmdLine = cmdLine + " --minSolidAngleRatio 0.2 --nbSolidAngleFilteringIterations 2"
	cmdLine = cmdLine + " --verboseLevel info --colorizeOutput False"
	cmdLine = cmdLine + " --maskHelperPointsWeight 1.0" 
	cmdLine = cmdLine + " --maskBorderSize 4 --maxNbConnectedHelperPoints 50"
	cmdLine = cmdLine + " --saveRawDensePointCloud False --exportDebugTetrahedralization False --seed 0"
	
	cmdLine = cmdLine + " --input \"" + srcIni + "\""
	cmdLine = cmdLine + " --depthMapsFolder \"" + srcDepthMapDir + "\""
	#cmdLine = cmdLine + " --depthMapFilterFolder \"" + srcDepthFilterDir + "\""
	#cmdLine = cmdLine + " --depthMapsFolder \"" + srcDepthMapDir + "\""
	#UI cmd

	cmdLine = cmdLine + " --outputMesh \"" + dstDir + "/mesh.obj\""
	cmdLine = cmdLine + " --output \"" + dstDir + "/densePointCloud.abc\""
	#cmdLine = cmdLine + " --output \"" + dstDir + "/mesh.obj\""
	
	print(cmdLine)
	os.system(cmdLine)
	return 0

def Run_10_MeshFiltering(baseDir,binDir):
	SilentMkdir(baseDir + "/10_MeshFiltering")

	binName = binDir + "\\aliceVision_meshFiltering.exe"

	srcMesh = baseDir + "/09_Meshing/mesh.obj"
	dstMesh = baseDir + "/10_MeshFiltering/mesh.obj"
  
    
 
	cmdLine = binName
	cmdLine = cmdLine + " --keepLargestMeshOnly True --smoothingSubset all"
	cmdLine = cmdLine + " --smoothingBoundariesNeighbours 0 --smoothingIterations 5"
	cmdLine = cmdLine + " --smoothingLambda 1.0 --filteringSubset all"
	cmdLine = cmdLine + " --filteringIterations 1 --filterLargeTrianglesFactor 60.0"
	cmdLine = cmdLine + " --filterTrianglesRatio 0.0 --verboseLevel info"  

	cmdLine = cmdLine + " --inputMesh \"" + srcMesh + "\""
	cmdLine = cmdLine + " --outputMesh \"" + dstMesh + "\""

	print(cmdLine)
	os.system(cmdLine)

	return 0

def Run_11_Texturing(baseDir,binDir):
	SilentMkdir(baseDir + "/11_Texturing")

	binName = binDir + "\\aliceVision_texturing.exe"

	srcMesh = baseDir + "/10_MeshFiltering/mesh.obj"
	srcRecon = baseDir + "/09_Meshing/denseReconstruction.bin"
	srcIni = baseDir + "/09_Meshing/densePointCloud.abc"
	#srcIni = baseDir + "/05_PrepareDenseScene/mvs.ini"
	dstDir = baseDir + "/11_Texturing"
	imgDir = baseDir + "/05_PrepareDenseScene"

	cmdLine = binName
	cmdLine = cmdLine + " --textureSide 8192 --downscale 2"
	cmdLine = cmdLine + " --outputTextureFileType png --unwrapMethod Basic"
	cmdLine = cmdLine + " --useUDIM True --fillHoles False"
	cmdLine = cmdLine + " --padding 5 --multiBandDownscale 4"
	cmdLine = cmdLine + " --multiBandNbContrib 1 5 10 0 --useScore True" 
	cmdLine = cmdLine + " --bestScoreThreshold 0.1 --angleHardThreshold 90.0"
	cmdLine = cmdLine + " --processColorspace sRGB --correctEV False"
	cmdLine = cmdLine + " --forceVisibleByAllVertices False --flipNormals False"
	cmdLine = cmdLine + " --visibilityRemappingMethod PullPush --subdivisionTargetRatio 0.8 --verboseLevel info"

	#cmdLine = cmdLine + " --inputDenseReconstruction \"" + srcRecon + "\""
	cmdLine = cmdLine + " --inputMesh \"" + srcMesh + "\""
	cmdLine = cmdLine + " --input \"" + srcIni + "\""
	cmdLine = cmdLine + " --imagesFolder \"" + imgDir + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "\""

	print(cmdLine)
	os.system(cmdLine)

	return 0

def main():
	#baseDir = input ("baseDir: ")
	#imgDir = input ("imgDir: ")
	#numImages = input ("Number of the photos: ")
	#runStep = input ("Runstep: ")
	print("Prepping Scan, v2.")

	print(sys.argv)
    
	print (len(sys.argv))
	if (len(sys.argv) != 5):
		print("usage: python run_alicevision_akaze.py <baseDir> <imgDir> <numImages> <runStep>")
		print("Must pass 5 arguments.")
		sys.exit(0)
	baseDir = sys.argv[1]
	srcImageDir = sys.argv[2]
	binDir = "aliceVision\\bin"
	numImages = int(sys.argv[3])
	runStep = sys.argv[4]
	

	print("Base dir  : %s" % baseDir)
	print("Image dir : %s" % srcImageDir)
	print("Bin dir   : %s" % binDir)
	print("Num images: %d" % numImages)
	print("Step      : %s" % runStep)




	SilentMkdir(baseDir)

	if runStep == "runall":
		Run_00_CameraInit(baseDir,binDir,srcImageDir)
		Run_01_FeatureExtraction(baseDir,binDir,numImages)
		Run_02_ImageMatching(baseDir,binDir)
		Run_03_FeatureMatching(baseDir,binDir)
		Run_04_StructureFromMotion(baseDir,binDir)
		Run_05_PrepareDenseScene(baseDir,binDir)

		#Run_06_CameraConnection(baseDir,binDir)

		Run_07_DepthMap(baseDir,binDir,numImages,3)
		Run_08_DepthMapFilter(baseDir,binDir)
		Run_09_Meshing(baseDir,binDir)
		Run_10_MeshFiltering(baseDir,binDir)
	
		Run_11_Texturing(baseDir,binDir)
	elif runStep == "run00":
		Run_00_CameraInit(baseDir,binDir,srcImageDir)

	elif runStep == "run01":
		Run_01_FeatureExtraction(baseDir,binDir,numImages)
	elif runStep == "run02":
		Run_02_ImageMatching(baseDir,binDir)
	elif runStep == "run03":
		Run_03_FeatureMatching(baseDir,binDir)
	elif runStep == "run04":
		Run_04_StructureFromMotion(baseDir,binDir)
	elif runStep == "run05":
		Run_05_PrepareDenseScene(baseDir,binDir)

	elif runStep == "run06":
		Run_06_CameraConnection(baseDir,binDir)

	elif runStep == "run07":
		Run_07_DepthMap(baseDir,binDir,numImages,3)
	elif runStep == "run08":
		Run_08_DepthMapFilter(baseDir,binDir)
	elif runStep == "run09":
		Run_09_Meshing(baseDir,binDir)
	elif runStep == "run10":
		Run_10_MeshFiltering(baseDir,binDir)
	
	elif runStep == "run11":
		Run_11_Texturing(baseDir,binDir)

	else:
		print("Invalid Step: %s" % runStep)



	

	#print("running")
	#Run_00_CameraInit(baseDir,binDir,srcImageDir)
	#Run_01_FeatureExtraction(baseDir,binDir,numImages)
	#Run_02_ImageMatching(baseDir,binDir)
	#Run_03_FeatureMatching(baseDir,binDir)
	#Run_04_StructureFromMotion(baseDir,binDir)
	#Run_05_PrepareDenseScene(baseDir,binDir)

	#Run_06_CameraConnection(baseDir,binDir)

	#Run_07_DepthMap(baseDir,binDir,numImages,3)
	#Run_08_DepthMapFilter(baseDir,binDir)
	#Run_09_Meshing(baseDir,binDir)
	#Run_10_MeshFiltering(baseDir,binDir)
	
	#Run_11_Texturing(baseDir,binDir)
	return 0



main()



