#include <gtest/gtest.h>
#include "stroke_features.hpp"

TEST(StrokeFeaturesTest, DefaultStrokeScoresZero) {
    StrokeFeatures f{};
std::cout << "face angle score: " << score_face_angle(f.face_angle_deg) << "\n";
std::cout << "stability score: " << score_stability(f.ang_vel_stability) << "\n";
std::cout << "tempo score: " << score_tempo(f.tempo_ratio) << "\n";
std::cout << "path score: " << score_path(f.path_deviation) << "\n";
std::cout << "total score: " << total_score(f) << "\n";

    EXPECT_DOUBLE_EQ(total_score(f), 0.0);
}
