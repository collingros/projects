#include <iostream>

using namespace std;

int main()
{
    int i = 1;
    cout << "suffix" << endl;
    for (i; i < 5; i++) {
        cout << std::to_string(i) << endl;
    }

    cout << "prefix" << endl;
    for (i; i < 5; ++i) {
        cout << std::to_string(i) << endl;
    }
}
