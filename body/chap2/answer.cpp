#include <cstdio>
#include <cstdlib>

int main()
{
    char yourname[16];
    int ans;
    printf ( "Your name:" );
    scanf ( "%s", yourname );
    printf ( "Hello, %s. Tell me the answer to the universe:\n", yourname );
    scanf ( "%d", &ans );
    if ( ans != 1295 )
    {
        puts ( "You are wrong! No shell for you!" );
    }
    else
    {
        puts ( "You are right! Congratulations, you deserve a shell." );
    }
    return 0;
}
