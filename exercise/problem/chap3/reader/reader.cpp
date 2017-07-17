#include <unistd.h>

int main()
{
    char buf[16];
    read ( 0, buf, 1024 );
    return 0;
}
