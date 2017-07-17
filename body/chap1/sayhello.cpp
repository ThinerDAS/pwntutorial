#include <cstdio>
#include <cstdlib>

int main()
{
    char yourname[16];
    scanf ( "%s", yourname );
    printf ( "Hello, %s\n", yourname );
    return 0;
}

void getshell()
{
    system ( "/bin/sh" );
}
