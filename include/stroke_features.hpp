#pragma once
#include <string>

struct StrokeFeatures {
    double face_angle_deg;
    double ang_vel_stability;
    double tempo_ratio;
    double path_deviation;

    // JSON helper functions
    bool loadFromJsonFile(const std::string& filename);
    bool saveToJsonFile(const std::string& filename) const;
};

// Scoring functions
double score_face_angle(double deg);
double score_stability(double s);
double score_tempo(double r);
double score_path(double d);
double total_score(const StrokeFeatures& f);
