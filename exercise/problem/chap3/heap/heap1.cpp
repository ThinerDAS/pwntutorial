#include <cstdio>
#include <cstdlib>
#include <unistd.h>

int readint();
void add_note();
void edit_note();
void list_note();
void del_note();

int main()
{
    setvbuf ( stdin, NULL, _IONBF, 0 );
    setvbuf ( stdout, NULL, _IONBF, 0 );
    alarm ( 15 );
    int choice = -1;
    printf (
        "Hello player, you can:\n"
        "[1]add note\n"
        "[2]edit note\n"
        "[3]list note\n"
        "[4]delete note\n"
        "[0]exit\n"
    );
    while ( true )
    {
        puts ( "Your command:" );
        choice = readint();
        switch ( choice )
        {
            case 0:
                exit ( 0 );
                break;
            case 1:
                add_note();
                break;
            case 2:
                edit_note();
                break;
            case 3:
                list_note();
                break;
            case 4:
                del_note();
                break;
            default:
                puts ( "Invalid command" );
        }
    }
}

int readint()
{
    char buf[16];
    if ( feof ( stdin ) )
    {
        return 0;
    }
    fgets ( buf, 16, stdin );
    return atoi ( buf );
}

struct note
{
    char* buf;
    int size;
};

struct note* ptrs[20];

int next_empty()
{
    for ( int i = 0; i < 20; i++ )
        if ( ptrs[i] == 0 )
        {
            return i;
        }
    return -1;
}

void add_note()
{
    int empty_slot = next_empty();
    if ( empty_slot == -1 )
    {
        puts ( "Sorry, full!" );
        return;
    }
    puts ( "Buffer size:" );
    int size = readint();
    if ( size > 0x10000 )
    {
        puts ( "Don't waste memory, please!" );
        return;
    }
    if ( size < 0x10 )
    {
        size = 0x10;
    }
    char* buf = ( char* ) malloc ( size );
    struct note* nt = ( struct note* ) malloc ( sizeof ( *nt ) );
    puts ( "Buffer data:" );
    fgets ( buf, size, stdin );
    nt->buf = buf;
    nt->size = size;
    ptrs[empty_slot] = nt;
    printf ( "Your id is %d.\n", empty_slot );
}

void edit_note()
{
    puts ( "Buffer id:" );
    int id = readint();
    if ( ptrs[id] == 0 )
    {
        puts ( "Invalid slot!" );
        return;
    }
    puts ( "Buffer size:" );
    int size = readint();
    if ( size > 0x10000 )
    {
        puts ( "Don't waste memory, please!" );
        return;
    }
    if ( size < 0x10 )
    {
        size = 0x10;
    }
    puts ( "Buffer data:" );
    fgets ( ptrs[id]->buf, size, stdin );
    ptrs[id]->size = size;
}

void list_note()
{
    puts ( "Buffer id:" );
    int id = readint();
    if ( ptrs[id] == 0 )
    {
        puts ( "Invalid slot!" );
        return;
    }
    printf ( "Note %d (len = %d) content: %s\n", id, ptrs[id]->size, ptrs[id]->buf );
}

void del_note()
{
    puts ( "Buffer id:" );
    int id = readint();
    if ( ptrs[id] == 0 )
    {
        puts ( "Invalid slot!" );
        return;
    }
    free ( ptrs[id]->buf );
    free ( ptrs[id] );
}

