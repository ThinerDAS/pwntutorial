#include <cstdio>
#include <cstdlib>
int main()
{
    long l1, l2, l3;
    scanf ( "%li", &l1 );
    printf ( "%#016lx\n", * ( long* ) l1 );
    scanf ( "%li%li", &l2, &l3 );
    * ( long* ) l2 = l3;
    _Exit ( 0 );
}
