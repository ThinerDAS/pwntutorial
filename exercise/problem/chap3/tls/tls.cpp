#include <cstdio>

__thread void* thread_cand;

int main()
{
    char buf[16];
    printf ( "%#016lx", &thread_cand );
    scanf ( "%s", buf );
    return 0;
}
