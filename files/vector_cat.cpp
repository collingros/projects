// Collin Gros

// studying for first Data Structures test..
// also, the first time i'm writing in cpp

#include <vector>
#include <iostream>

using namespace std;


void print_vectors(std::vector<int> A)
{
    cout << "func called" << endl;
    for (int i = 0; i < A.size(); i++) {
        cout << "this is a[i]: " + std::to_string(A[i]) << endl;
    }
}


int main()
{
    std::vector<int> A(5, 0);
    std::vector<int> B(5, 1);


    A.insert(A.begin(), B.begin(), B.end());
    print_vectors(A);

    return 0;
}
