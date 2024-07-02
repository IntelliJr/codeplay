#include <iostream>
#include <cassert>
#include "CPP_HelloWorld.cpp"

// Function to test
std::string helloWorld();

int main() {
    assert(helloWorld() == "Hello World" && "Test case failed: helloWorld() must return\"Hello World\"!");
    std::cout << "All tests passed successfully! Ready to submit solution.\n";

    return 0;
}