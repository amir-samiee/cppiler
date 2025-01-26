#include
using namespace std;
int main(){
    float x;
    int s=0, t=10;
    while (t >= 0){
        cin>>x;
        t = t - 1;
        s = s+x- 1 * 3;
    }
    cout<<"sum="<<s;
    return 0;
}