#include <iostream>
#include <cassert>
#include "CPP_OddInteger.cpp"

int main() {
    std::vector<int> arr1 = {0};
    std::vector<int> arr2 = {1};
    std::vector<int> arr3 = {1, 1, 2};
    std::vector<int> arr4 = {1, 2, 1, 2, 1};
    std::vector<int> arr5 = {1, 2, 2, 3, 3, 3, 4, 3, 3, 3, 2, 2, 1};

    assert(oddInteger(arr1) == 0 && "Failed test case: oddInteger({0}) must return 0!");
    assert(oddInteger(arr2) == 1 && "Failed test case: oddInteger({1}) must return 1!");
    assert(oddInteger(arr3) == 2 && "Failed test case: oddInteger({1, 1, 2}) must return 2!");
    assert(oddInteger(arr4) == 1 && "Failed test case: oddInteger({1, 2, 1, 2, 1}) must return 1!");
    assert(oddInteger(arr5) == 4 && "Failed test case: oddInteger({1, 2, 2, 3, 3, 3, 4, 3, 3, 3, 2, 2, 1}) must return 4!");

    std::cout << "All tests passed successfully! Ready to submit solution.\n";

    return 0;
}
