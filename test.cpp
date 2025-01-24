#include
using namespace std;
int main()
{
    int x;
    int s = 0, t = 10;
    float a = 1.1;
    while (t >= 0)
    {
        cin >> x;
        t = t - 1;
        s = s + x;
    }
    cout << "sum=" << s;
    return 0;
}