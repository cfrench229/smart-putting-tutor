#include <gtest/gtest.h>
#include "stroke_features.hpp"

TEST(StrokeFeaturesTest, DefaultStrokeScoresZero) {
    StrokeFeatures f{};

    EXPECT_DOUBLE_EQ(total_score(f), 0.0);
}
