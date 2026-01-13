#include "sample_loader.hpp"
#include <nlohmann/json.hpp>
#include <fstream>
#include <iostream>
#include <filesystem>

namespace fs = std::filesystem;
// Opens json files from the specified folder path, calculates score and
// prints out for each file. This is only meant for sample purposes and does
// not provide real data.
#ifdef USE_SAMPLES
void loadAndPrintSamples(const std::string& folderPath) {
    std::cout << "Loading sample strokes from folder: " << folderPath << "\n";

    for (const auto& entry : fs::directory_iterator(folderPath)) {
        if (entry.path().extension() == ".json") {
            StrokeFeatures stroke;

            // Open JSON file
            std::ifstream file(entry.path());
            if (!file.is_open()) {
                std::cerr << "Failed to open " << entry.path() << "\n";
                continue;
            }

            // Parse JSON
            nlohmann::json j;
            try {
                file >> j;
            } catch (const std::exception& e) {
                std::cerr << "Error parsing " << entry.path() << ": " << e.what() << "\n";
                continue;
            }

            // Load fields
            try {
                stroke.face_angle_deg    = j["face_angle_deg"];
                stroke.ang_vel_stability = j["ang_vel_stability"];
                stroke.tempo_ratio       = j["tempo_ratio"];
                stroke.path_deviation    = j["path_deviation"];
                stroke.is_set = true;
            } catch (const std::exception& e) {
                std::cerr << "Invalid/missing field in " << entry.path() << ": " << e.what() << "\n";
                continue;
            }

            // Calculate score
            double score = total_score(stroke);

            // Print results
            std::cout << entry.path().filename() << ":\n";
            std::cout << "  Face angle: " << stroke.face_angle_deg << "\n";
            std::cout << "  Angular velocity stability: " << stroke.ang_vel_stability << "\n";
            std::cout << "  Tempo ratio: " << stroke.tempo_ratio << "\n";
            std::cout << "  Path deviation: " << stroke.path_deviation << "\n";
            std::cout << "  Calculated score: " << score << "\n\n";
        }
    }
}
#endif
