#original file from http://filmicworlds.com/blog/command-line-photogrammetry-with-alicevision/
#re-edited by Zurong ZHANG 
#Supervisor : Dr. Adam A. Stokes
#Soft System Group / The School of Engineering / The University of Edinburgh
#date: 06/12/2021
#Discription : This is a meshroom command line test in sift mode with stl transformation.
#usage: python run_alicevision_sift_stl.py <baseDir> <imgDir> <numImages> <runStep>
#download python >= 3.6, pip3 and pymeshlab before running
import sys, os
import shutil
import pymeshlab

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
	cmdLine = cmdLine + " --describerTypes sift --forceCpuExtraction True --describerQuality normal --contrastFiltering GridSort --gridFiltering True --verboseLevel info --describerPreset normal --maxThreads 0"
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
	cmdLine = cmdLine + " --minNbImages 200 --method VocabularyTree --tree aliceVision/share/aliceVision/vlfeat_K80L3.SIFT.tree --maxDescriptors 500 --verboseLevel info --weights "" --nbMatches 50"
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
	cmdLine = cmdLine + " --verboseLevel info --describerTypes sift --maxMatches 0 --exportDebugFiles False --savePutativeMatches False --guidedMatching False"
	cmdLine = cmdLine + " --geometricEstimator acransac --geometricFilterType fundamental_matrix --maxIteration 2048 --distanceRatio 0.8"
	cmdLine = cmdLine + " --photometricMatchingMethod ANN_L2"
	
	#UI cmd
	cmdLine = cmdLine + " --geometricError 0.0 --knownPosesGeometricErrorMax 5.0 --crossMatching False --matchFromKnownCameraPoses False" 
	#cmdLine = cmdLine + " --rangeStart 0 --rangeSize 20"

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
	cmdLine = cmdLine + " --minAngleForLandmark 2.0 --minNumberOfObservationsForTriangulation 2 --maxAngleInitialPair 40.0 --maxNumberOfMatches 0 --localizerEstimator acransac --describerTypes sift --lockScenePreviouslyReconstructed False --localBAGraphDistance 1"
	#cmdLine = cmdLine + " --initialPairA "" --initialPairB "" --interFileExtension .ply --useLocalBA True"
	#cmdLine = cmdLine + "  " 
	cmdLine = cmdLine + ' --interFileExtension .abc --useLocalBA True --initialPairB ""'
	cmdLine = cmdLine + " --minInputTrackLength 2 --useOnlyMatchesFromInputFolder False --verboseLevel info --minAngleForTriangulation 3.0 --maxReprojectionError 4.0 --minAngleInitialPair 5.0"
	cmdLine = cmdLine + ' --initialPairA ""'
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
	cmdLine = cmdLine + " --outputFileType exr --saveMetadata True --saveMatricesTxtFiles False --evCorrection False --verboseLevel info --rangeStart 0 --rangeSize 40"
	cmdLine = cmdLine + " --input \"" + srcSfm + "\""
	cmdLine = cmdLine + " --output \"" + dstDir +"\""

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
	cmdLine = cmdLine + " --sgmGammaC 5.5 --minViewAngle 2.0 --sgmWSH 4 --refineGammaP 8.0 --refineSigma 15 --refineNSamplesHalf 150 --sgmMaxTCams 10 --refineWSH 3 --downscale 2 --refineMaxTCams 6 --verboseLevel info --refineGammaC 15.5 --sgmGammaP 8.0"
	cmdLine = cmdLine + " --maxViewAngle 70.0 --exportIntermediateResults False --nbGPUs 0"
	cmdLine = cmdLine + " --refineNiters 100 --refineNDepthsToRefine 31 --refineUseTcOrRcPixSize False"
	
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
	cmdLine = cmdLine + " --maxViewAngle 70.0 --minViewAngle 2.0 --minNumOfConsistentCamsWithLowSimilarity 4"
	cmdLine = cmdLine + " --minNumOfConsistentCams 3 --verboseLevel info --pixSizeBall 0"
	cmdLine = cmdLine + " --pixSizeBallWithLowSimilarity 0 --computeNormalMaps False --nNearestCams 10"
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

	cmdLine = binName
	cmdLine = cmdLine + " --simGaussianSizeInit 10.0 --maxInputPoints 50000000 --repartition multiResolution"
	cmdLine = cmdLine + " --simGaussianSize 10.0 --simFactor 15.0 --voteMarginFactor 4.0 --contributeMarginFactor 2.0 --minStep 2 --pixSizeMarginFinalCoef 4.0 --maxPoints 5000000 --maxPointsPerVoxel 1000000 --angleFactor 15.0 --partitioning singleBlock"
	cmdLine = cmdLine + " --minAngleThreshold 1.0 --pixSizeMarginInitCoef 2.0 --refineFuse True --verboseLevel info --colorizeOutput False"
	cmdLine = cmdLine + " --estimateSpaceFromSfM True --saveRawDensePointCloud False --exportDebugTetrahedralization False --seed 0"
	cmdLine = cmdLine + " --maxNbConnectedHelperPoints 50 --nbSolidAngleFilteringIterations 2 --estimateSpaceMinObservations 3 --minSolidAngleRatio 0.2"
	cmdLine = cmdLine + " --addLandmarksToTheDensePointCloud False --invertTetrahedronBasedOnNeighborsNbIterations 10 --helperPointsGridSize 10 --nPixelSizeBehind 4.0"
	cmdLine = cmdLine + " --fullWeight 1.0 --voteFilteringForWeaklySupportedSurfaces True --estimateSpaceMinObservationAngle 10"
	
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
	cmdLine = cmdLine + " --filterTrianglesRatio 0.0 --verboseLevel info  --smoothingIterations 5 --keepLargestMeshOnly True --smoothingSubset all"
	cmdLine = cmdLine + " --smoothingBoundariesNeighbours 0 --smoothingLambda 1.0 --filteringSubset all --filteringIterations 1"
	#--filterLargeTrianglesFactor 60.0 --removeLargeTrianglesFactor 60.0
	cmdLine = cmdLine + " --input \"" + srcMesh + "\""
	cmdLine = cmdLine + " --output \"" + dstMesh + "\""

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
	cmdLine = cmdLine + " --textureSide 8192 --useUDIM True --padding 5 --multiBandNbContrib 1 5 10 0"
	cmdLine = cmdLine + " --downscale 2 --verboseLevel info --multiBandDownscale 4 --useScore True"
	cmdLine = cmdLine + " --unwrapMethod Basic --outputTextureFileType png --flipNormals False --fillHoles False"
	cmdLine = cmdLine + " --bestScoreThreshold 0.1 --processColorspace sRGB --angleHardThreshold 90.0 --correctEV False"
	cmdLine = cmdLine + " --visibilityRemappingMethod PullPush --subdivisionTargetRatio 0.8 --forceVisibleByAllVertices False"
# --padding 15
	#cmdLine = cmdLine + " --inputDenseReconstruction \"" + srcRecon + "\""
	cmdLine = cmdLine + " --inputMesh \"" + srcMesh + "\""
	cmdLine = cmdLine + " --input \"" + srcIni + "\""
	cmdLine = cmdLine + " --imagesFolder \"" + imgDir + "\""
	cmdLine = cmdLine + " --output \"" + dstDir + "\""

	print(cmdLine)
	os.system(cmdLine)

	return 0

def Run_to_Stl(baseDir,binDir):
	ms = pymeshlab.MeshSet()
	ms.load_new_mesh(baseDir + "/10_MeshFiltering/mesh.obj")
	ms.save_current_mesh(baseDir + "/10_MeshFiltering/mesh.stl")

	return 0

def main():
	print("Prepping Scan, v2.")

	print(sys.argv)
    
	print (len(sys.argv))
	if (len(sys.argv) != 5):
		print("usage: python run_alicevision_sift.py <baseDir> <imgDir> <numImages> <runStep>")
		print("Must pass 5 arguments.")
		sys.exit(0)
	baseDir = sys.argv[1]
	srcImageDir = sys.argv[2]
	binDir = "alicevision\\bin"
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
		Run_to_Stl(baseDir,binDir)

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
	elif runStep == "runstl":
		Run_to_Stl(baseDir,binDir)
	
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



