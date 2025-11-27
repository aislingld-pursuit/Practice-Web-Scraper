#include <iostream>
using namespace std;

int main() {
    int arr[] = {1, 3, 10, 11, 14};
    int n = sizeof(arr) / sizeof(arr[0]);
    int target = 13;
    bool found = false;

    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            if (arr[i] + arr[j] == target) {
                cout << "Pair found: " << arr[i] << " + " << arr[j]
                     << " = " << target << endl;
                found = true;
            }
        }
    }

    if (!found) {
        cout << "No pair sums to " << target << endl;
    }

    return 0;
}