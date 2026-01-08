#include "stroke_features.hpp"
#ifdef USE_SAMPLES
#include "sample_loader.hpp"
#endif
#include <iostream>

int main() {
#ifdef USE_SAMPLES
    std::cout << "Running in SAMPLE mode...\n";
    loadAndPrintSamples("samples/features");
#else
    std::cout << "Running in PRODUCTION mode. No sample strokes loaded.\n";
#endif

    return 0;
}
