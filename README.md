# Data Augmentation of Engineering Drawings for Data-driven Component Segmentation
Created by Wentai Zhang, Quan Chen, Can Koz, Liuyue Xie, Amit Regmi, Soji Yamakawa, Tomotake Furuhata, Kenji Shimada, Levent Burak Kara from Carnegie Mellon University.

![teaser](teaser.png)

### Abstract
We present a new data generation method to facilitate an automatic machine interpretation of 2D engineering part drawings. While such drawings are a common medium for clients to encode design and manufacturing requirements, a lack of computer support to automatically interpret these drawings necessitates part manufacturers to resort to laborious manual approaches for interpretation which, in turn, severely limits processing capacity.  Although recent advances in trainable computer vision methods may enable automatic machine interpretation, it remains challenging to apply such methods to engineering drawings due to a lack of labeled training data. As one step toward this challenge, we propose a constrained data synthesis method to  generate an arbitrarily large set of synthetic training drawings using only a handful of labeled examples. Our method is based on the randomization of the dimension sets subject to two major constraints to ensure the validity of the synthetic drawings. The effectiveness of our method is demonstrated in the context of a  binary component segmentation task with a proposed list of descriptors. An evaluation of several image segmentation methods trained on our synthetic dataset shows that our approach to new data generation can boost the segmentation accuracy and the generalizability of the machine learning models to unseen drawings.

### Citation
If you find our work useful in your research, please consider citing us:
```
@inproceedings{zhang2022data,
  title={Data Augmentation of Engineering Drawings for Data-driven Component Segmentation},
  author={Zhang, Wentai and Chen, Quan and Koz, Can and Xie, Liuyue and Regmi, Amit and Yamakawa, Soji and Furuhata Tomotake and Shimada, Kenji and Kara, Levent Burak},
  booktitle={ASME 2022 International Design Engineering Technical Conferences and Computers and Information in Engineering Conference},
  pages={},
  year={2022},
  organization={American Society of Mechanical Engineers}
 }
```

### Dependencies
```
 dxfgrabber==1.0.1 
 ezdxf==0.11.1 
 matplotlib==3.1.1 
 multiprocess==0.70.9 
 numpy==1.17.2 
 pandas==0.25.3 
 python-dateutil==2.8.0 
 python-utils==2.3.0 
 scikit-learn==1.0.2   
```

### Usage
1. Prepare part drawings in DXF format. Some sample drawings are provided in `/raw_data` folder. Note that the outer frames, symbols for geometric tolerances and surface roughness are not considered in the current scope of work. The layers need to follow the same style as the given examples.
2. Open `dxfRunner.py`. The variable `num` controls the number of synthetic drawings generated from each given examples in `/raw_data`.
3. Install all required dependencies. Run `dxfRunner.py` file until it shows `Draw File DONE!!! Copy File DONE!!!` in the command line.
4. The synthesized dxf files are saved in a newly created folder named `generated_dxf`. The parameters in JSON format corresponding to each synthetic drawing are saved in `generated_json`.

### Aknowledgement
The authors would like to thank MiSUMi Corporation for their provision of a contemporary engineering problem, guidance on the applicability of developed methods, and financial support.