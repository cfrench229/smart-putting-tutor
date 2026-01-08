# Smart Putting Tutor

A work-in-progress embedded system designed to analyze golf putting mechanics using an IMU sensor and embedded Linux. The system captures high-frequency motion data, calculates stroke scores, and supports both sample testing and real-world data.

## Project Goals

- Capture high-frequency motion data from an IMU  
- Process and analyze putting stroke characteristics  
- Provide meaningful feedback for improving consistency  
- Practice real-world embedded, C++, Python, and ML workflows  

## Tech Stack

- Embedded Linux (Raspberry Pi)  
- C / C++  
- Python (data analysis, scripts, and ML)  
- IMU sensors  
- GitHub Actions (CI)  
- Unit testing (GTest)  

## Current Status

- `StrokeFeatures` struct implemented with scoring logic for **face angle**, **tempo**, **angular velocity stability**, and **path deviation**  
- JSON load/save functionality using **nlohmann/json** for both sample and real strokes  
- Sample strokes created in `samples/features/` (`great`, `average`, `bad`) for testing scoring  
- Build system updated to optionally include sample strokes via a compile-time flag  
- Python setup script (`setup.py`) downloads `nlohmann/json` automatically  
- Python build script (`build.py`) handles building the binary in **production** or **sample mode**

## Next steps

- Revisit StrokeFeature struct. It may make more sense to create a class and move methods into the class. 
- Introduce a logger, which will capture and log the putting strokes to a buffer. This should be its own class.
- Go through and comment everything
- Try to get actual data from hardware


## How to Build

### 1. Install dependencies

Run the setup script:

`
python3 scripts/setup.py
`

### 2. Build the project

Use the build script to compile the binary:

Production build (no sample strokes):

`python3 scripts/build.py --build`


Sample build (loads all JSON sample strokes):

`python3 scripts/build.py -S`


The script automatically:

Compiles all C++ source files

Adds the USE_SAMPLES macro for sample builds

Outputs the binary to `bin/putting_tutor`


## Run the binary

To run, execute `./bin/putting_tutor` from within the root directory.

Here is example code of samples being run: 

```
Running in SAMPLE mode...
Loading sample strokes from folder: samples/features
"average_stroke.json":
  Face angle: 0.8
  Angular velocity stability: 0.14
  Tempo ratio: 2.35
  Path deviation: 0.08
  Calculated score: 0.601

"bad_stroke.json":
  Face angle: 1.6
  Angular velocity stability: 0.28
  Tempo ratio: 1.4
  Path deviation: 0.18
  Calculated score: 0.448

"great_stroke.json":
  Face angle: 0.3
  Angular velocity stability: 0.06
  Tempo ratio: 2
  Path deviation: 0.04
  Calculated score: 0.86
  ```