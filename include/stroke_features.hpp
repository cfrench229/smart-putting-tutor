#pragma once
#include <string>
// Putting stroke features. It may be wise to add
// zero intializers to this and then a timestamp or flag to signify 
// a stroke was made, so that "set" and a perfect stroke are not miscontrued. 
struct StrokeFeatures {
    double face_angle_deg;
    double ang_vel_stability;
    double tempo_ratio;
    double path_deviation;

    bool is_set = false;  // false by default
    
        // JSON helper functions
    bool saveToJsonFile(const std::string& filename) const;
};


// Scoring functions
double score_face_angle(double deg);
double score_stability(double s);
double score_tempo(double r);
double score_path(double d);
double total_score(const StrokeFeatures& f);
