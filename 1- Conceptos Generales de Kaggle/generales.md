The challenge uses the standard PASCAL VOC 2010 mean Average Precision (mAP) at IoU > 0.5. Note that the linked document describes VOC 2012, which differs in some minor ways (e.g. there is no concept of "difficult" classes in VOC 2010). The P/R curve and AP calculations remain the same.

In this competition, we are making predictions at both a study (multi-image) and image level.

Study-level labels
Studies in the test set may contain more than one label. They are as follows:

"negative", "typical", "indeterminate", "atypical"

Please see the Data page for further details.

For each study in the test set, you should predict at least one of the above labels. The format for a given label's prediction would be a class ID from the above list, a confidence score, and 0 0 1 1 is a one-pixel bounding box.

Image-level labels
Images in the test set may contain more than one object. For each object in a given test image, you must predict a class ID of "opacity", a confidence score, and bounding box in format xmin ymin xmax ymax. If you predict that there are NO objects in a given image, you should predict none 1.0 0 0 1 1, where none is the class ID for "No finding", 1.0 is the confidence, and 0 0 1 1 is a one-pixel bounding box.

Submission File
The submission file should contain a header and have the following format:

Id,PredictionString
2b95d54e4be65_study,negative 1 0 0 1 1
2b95d54e4be66_study,typical 1 0 0 1 1
2b95d54e4be67_study,indeterminate 1 0 0 1 1 atypical 1 0 0 1 1
2b95d54e4be68_image,none 1 0 0 1 1
2b95d54e4be69_image,opacity 0.5 100 100 200 200 opacity 0.7 10 10 20 20
etc.