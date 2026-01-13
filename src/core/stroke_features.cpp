#include "stroke_features.hpp"
#include <nlohmann/json.hpp>
#include <fstream>

using json = nlohmann::json;

// ---------------- JSON ----------------

bool StrokeFeatures::saveToJsonFile(const std::string& filename) const {
    std::ofstream f(filename);
    if (!f.is_open()) return false;

    json j;
    j["face_angle_deg"]    = face_angle_deg;
    j["ang_vel_stability"] = ang_vel_stability;
    j["tempo_ratio"]       = tempo_ratio;
    j["path_deviation"]    = path_deviation;

    f << j.dump(4); // pretty print with 4-space indent
    return true;
}

// ---------------- Scoring ----------------

double score_face_angle(double face_angle_deg) {
    // Example: smaller is better
    return std::max(0.0, 1.0 - std::abs(face_angle_deg));  // returns double
}

double score_stability(double ang_vel_stability) {
    return std::max(0.0, 1.0 - ang_vel_stability);  // double
}

double score_tempo(double tempo_ratio) {
    return std::max(0.0, 1.0 - std::abs(tempo_ratio - 2.0) / 2.0);  // double division
}

double score_path(double path_deviation) {
    return std::max(0.0, 1.0 - path_deviation);  // double
}


double total_score(const StrokeFeatures& f) {
    if (!f.is_set) return 0.0;  // blank stroke
    
    return 0.40 * score_face_angle(f.face_angle_deg) +
           0.20 * score_stability(f.ang_vel_stability) +
           0.20 * score_tempo(f.tempo_ratio) +
           0.20 * score_path(f.path_deviation);
}

