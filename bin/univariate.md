 To keep them in T1, instead of moving an MNI or the subject's T1w image into the lower level feat reg folder (before running the higher level analysis), 
 you'll need to move the mean_func.nii.gz image found in the feat folder into the reg directory (and move the identity matrix into the reg folder also like you have before). 
The lab previously used each subject's T1w image to do so, but that was resulting in some weird transformations into a completely different space.
