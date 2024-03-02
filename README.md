# alicevision_stl
README Author : Zurong ZHANG 
Supervisor : Dr. Adam A. Stokes
Soft Systems Group / The School of Engineering / The University of Edinburgh
Date : 06/12/2021
Latest edited by Zurong ZHANG 06/12/2021

Discription : This is a test folder for Meshroom running in alicevision command line in sift mode (version 2.0) - transfer the .obj to .stl.
The folder includes: run_alicevision_sift_stl.py (in sift); alicevision folder; command_test1 photo set;
baseDir result folder; lisence; README file. 

Usage： python run_alicevision_sift_stl.py baseDir command_test1 6 runall
              python run_alicevision_sift_stl.py baseDir command_test1 6 runstl   (with mesh.obj generated successfully in step 10)

NOTE: Keep all these files under the same folder.
NOTE: Use an empty result folder.
NOTE: 06 is not exacuted in UI so run06 is commented in main, please do not run06 in command line.
NOTE: Meshlabserver is dismissed. For meshlab 2021.05 use PyMeshLab for filters in command lines.

More information on Meshroom,
please reference http://filmicworlds.com/blog/command-line-photogrammetry-with-alicevision/
More information on PyMeshLab,
please reference https://github.com/cnr-isti-vclab/PyMeshLab

To run the files, please read this firstly.

1. Download pip: 
Windows check if pip downloaded:
cmd:    python -m pip --version

2. cmd:    pip3 install pymeshlab  
https://pymeshlab.readthedocs.io/en/latest/installation.html
Note: if the installation fails, please double check that you are running a 64bit Python version.
PyMeshLab requires Python >= 3.6 (64 bit), and numpy.

3. Test if pymeshlab is installed successfully. 
python
>>> import pymeshlab
>>> ms = pymeshlab.MeshSet()
>>> ms.load_new_mesh('mesh.obj')
>>> ms.save_current_mesh('mesh.stl')

Once pymeshlab can run successfully, the .py script can generate both .obj and .stl with the same usage as before (version 1.0). 
4. Set up an empty folder to put all the results. For example, in this test baseDir is the destination place for all results.
 (To avoide the influence of the history files, please set up an empty folder or delete the history records.)
5. Set up the folder of your photos. For example, in this test command_test_mini is the photo folder including 6 photos from
the online test set.
6. Use cmd to enter run_alicevision, and use python command line as followed 

python run_alicevision_sift_stl.py <baseDir> <imgDir> <numImages> <runStep>

For example, * keep the order right in this step; 

E:\Codes test\run_alicevision_sift>python run_alicevision_sift_stl.py baseDir command_test1 6 runall

<baseDir> can be set to the destination path as you want, but the it should be the same path as where you set your baseDir 
<imgDir> is the path of your set your photo folder
<numImages> is the number of the photos in your photo folder
<runStep> choose the step you want to run, such as runall, or run00

4. Wait the process to be finished. 
Can check the system process in the task manager of the computer - to see if .exe runs.
5. Get your .obj from baseDir\11_Texturing\texturedMesh.obj
6. Get your .stl from baseDir\10_MeshFiltering\mesh.stl

The test set is from Meshroom online https://github.com/alicevision/dataset_monstree
and photos from the user
command_test1 (online test 6 photos tree)
command_test2 (user taken 5 photos face model)
command_test3 (41 photos) not available for this version yet

If errors happen: 
Check if RAM is >= 8GB.
Check if the alicevision folder is included -- which has the .exe and .tree files. 
Check if the errors caused by the faulse format of the proporties. 
