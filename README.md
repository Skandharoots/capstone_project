# CapstoneCode

## Currently on `master` branch:

![Alt text](/images/1.png)

![Alt text](/images/2.png)

![Alt text](/images/3.png)

Images of the application before introducing the dynamic triangle mesh generation and visualization method.

![Alt text](/images/4.png)

![Alt text](/images/5.png)

Images of the application after introducing the dynamic triangle mesh generation and visualization method.

## Our modifications to KISS-ICP

### - Robot movement visual representation
### - Origin gizmo + moving and rotating gizmo (with robot's movement)
### - Line connecting both positions
### - Ability to not clear the visited path (along with the position and rotation gizmo)
### - ROSBAG conventer
### - CMake and Makefile scripts improvements (also for Windows!)
### - Dynamic triangle mesh generation and visualization method (BIG one)

## Setup guide:
- set the `${KISS_ICP_SOURCE_PATH}` CMAKE environment variable to: `path_to_the_repository/src/cpp/kiss_icp` folder
- run `make install` from the repository root folder

Example:
```bash
set(KISS_ICP_SOURCE_PATH "E:/capstonecode/src/cpp/kiss_icp")
```

---

## Running the program:
- set values of:
    - `DataPath` - path to the data file (`.bag`)
    - `ConfigPath` - path to the config file (`.yaml`)
    - `Topic` - topic name from the data file
- run `python ./main.py` from the repository root folder (for linux use `python3`)

## Repository structure:

 ```
📦 - configs - contains the exemplary config file used by kiss-icp implementation modified by us
 ┣ 📜 - config.yaml

📦 - images - contains images used in this README.md

📦 - mod - contains the initial modified kiss-icp visualizer
 ┣ 📜 - visualizer.py - only the modified parts of the visualizer that should be placed in the original kiss-icp visualizer

📦 - src - contains the whole modified kiss-icp source code that can be compiled and run

📦 - utils - utility scripts
┣ 📜 - rosbag_converter.py - script that converts plain data to the rosbag file format used by kiss-icp
┣ 📜 - remove_commas.py - script that removes commas from the data file
┣ 📜 - create_point_cloud_lite.py - script that creates a smaller point cloud from the data file to test stuff on smaller data sets

📜 main.py - main script that runs the whole modified program

📜 Makefile - main makefile script to compile the source code and install this as a python package
 ```
