#include <cstdio>
#include <cstdlib>
#include <unistd.h>

typedef long ( *callable ) ( long, long, long, long, long, long );

int main()
{
    char* buffer = ( char* ) malloc ( 4096 );
    int pid = getpid();
    snprintf ( buffer, 4095, "/proc/%d/maps", pid );
    FILE* f = fopen ( buffer, "r" );
    int s = fread ( buffer, 1, 4096, f );
    fwrite ( buffer, 1, s, stdout );
    fclose ( f );
    long arg[7];
    for ( int i = 0; i < 7; i++ )
    {
        if ( scanf ( "%li", arg + i ) != 1 )
        {
            return 0;
        }
    }
    return ( ( callable ) arg[0] ) ( arg[1], arg[2], arg[3], arg[4], arg[5], arg[6] );
}
