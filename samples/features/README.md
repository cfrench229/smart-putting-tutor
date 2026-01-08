# Stroke Feature Samples

This folder contains example stroke feature data for the Putting Tutor project. These JSON files are **hard-coded sample strokes** used for testing and validating the scoring logic of the system.  

They are **not real IMU data**, but represent simplified, idealized feature values for three categories of stroke quality.

## File Overview

- `great_stroke.json`  
  Represents a **high-quality putt**.  
  Features:
  - Face angle near impact: very stable
  - Angular velocity: smooth
  - Tempo: balanced (backswing : forward swing ≈ 2:1)
  - Path deviation: minimal  
  Use this as a reference for “great stroke” scoring.

- `average_stroke.json`  
  Represents a **moderate putt**.  
  Features:
  - Slight face angle variation
  - Tempo slightly off from ideal
  - Angular velocity and path deviations noticeable but acceptable  
  Useful for testing borderline cases.

- `bad_stroke.json`  
  Represents a **poor stroke**.  
  Features:
  - Face angle significantly off
  - Tempo highly inconsistent
  - High angular velocity variability and path deviation  
  Use this for testing scoring penalties and weighting.

## Purpose

These samples are used to:

1. **Validate scoring logic** – ensure weighting prioritizes face angle, tempo, and path appropriately.  
2. **Test randomization scripts** – generate synthetic stroke variations around each baseline.  
3. **Serve as a ground truth** – initial labeled data for manual tests before using real IMU data.

## Notes

- Each JSON file corresponds to a `StrokeFeatures` object in the source code.
- Fields in each JSON:
  - `face_angle_deg` – absolute rotation near impact in degrees
  - `ang_vel_stability` – normalized standard deviation of angular velocity (0–1)
  - `tempo_ratio` – backswing / forward swing
  - `path_deviation` – normalized deviation from stroke plane (0–1)
- Randomized variations should be generated using the `generate_samples` tool in the `tools/` folder.
