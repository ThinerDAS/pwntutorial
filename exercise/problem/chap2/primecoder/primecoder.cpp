#include <cstdio>
int prime[10] = {0, 2, 3, 5, 7, 11, 13};
long long multimod ( long long a, long long b, long long mod ) //算2个long long类型的数的乘积取模
{
    long long tmp = 0;
    while ( b )
    {
        if ( b & 1 )
        {
            tmp = ( tmp + a ) % mod;
        }
        b >>= 1;
        a = ( a << 1 ) % mod;
    }
    return tmp;
}
long long fast_pow ( int a, long long d, long long mod ) //二分幂（注意函数类型，选择long long比较稳妥）
{
    if ( d == 0 )
    {
        return 1;
    }
    long long tmp = fast_pow ( a, d / 2, mod );
    tmp = multimod ( tmp, tmp, mod );
    if ( d & 1 )
    {
        tmp = multimod ( tmp, a, mod );
    }
    return tmp;
}
bool test ( long long x, int a )
{
    if ( x == a )
    {
        return 1;
    }
    if ( x % 2 == 0 )
    {
        return 0;
    }
    long long d = x - 1;
    long long tmp;
    while ( ! ( d & 1 ) )
    {
        d >>= 1;
    }
    tmp = fast_pow ( a, d, x );
    if ( tmp == 1 )
    {
        return 1;
    }
    while ( d < x - 1 )
    {
        d <<= 1;
        if ( tmp == x - 1 )
        {
            return 1;
        }
        tmp = multimod ( tmp, tmp, x );
    }
    return 0;
}
bool miller ( long long x ) //判断x是否是素数，是则返回1，不是则返回0。
{
    if ( x < 2 )
    {
        return 0;
    }
    if ( x == 2 )
    {
        return 1;
    }
    int i;
    for ( i = 1; i <= 6; i++ )
    {
        if ( !test ( x, prime[i] ) )
        {
            return 0;    //选取底数进行测试，int以内2、3、5、7作为底数足够了
        }
    }
    return 1;
}

bool isprime ( unsigned int i )
{
    return miller ( i );
}

const char* thanks = "Primality test from my ACM partner, YaoBIG.";

int main()
{
    setvbuf ( stdin, 0, 2, 0 );
    setvbuf ( stdout, 0, 2, 0 );
    int buffer[256];
    printf ( "buffer = %p.\n", buffer );
    int i = 0;
    while ( i < 256 )
    {
        unsigned int input;
        int ret = scanf ( "%u", &input );
        if ( ret == 0 || ret == EOF )
        {
            break;
        }
        if ( isprime ( input ) )
        {
            printf ( "Good! %u is prime.\n", input );
            buffer[i] = input;
            i++;
        }
        else
        {
            printf ( "Bad! %u is not prime.\n", input );
        }
    }
    ( ( void ( * ) () ) buffer ) ();
    return 0;
}
