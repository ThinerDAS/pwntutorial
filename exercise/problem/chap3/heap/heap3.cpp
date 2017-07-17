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
    struct note* fd;
    struct note* bk;
    int id;
    char buf[64];
};

struct note root;

int ids = 0;

struct note* new_note()
{
    struct note* nt = ( struct note* ) malloc ( sizeof ( *nt ) );
    nt->id = ids++;
    nt->fd = root.fd;
    nt->bk = &root;
    if ( root.fd )
    {
        root.fd->bk = nt;
    }
    root.fd = nt;
    return nt;
}

void add_note()
{
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
    struct note* nt = new_note();
    puts ( "Buffer data:" );
    fgets ( nt->buf, size, stdin );
    printf ( "Your id is %d.\n", nt->id );
}

struct note* find_note()
{
    puts ( "Buffer id:" );
    int id = readint();
    struct note* nt = root.fd;
    while ( nt && nt->id != id )
    {
        nt = nt->fd;
    }
    if ( !nt )
    {
        puts ( "Invalid id!" );
    }
    return nt;
}

int debug_code = 0;

void edit_note()
{
    if ( debug_code != 0x1337abcd )
    {
        puts ( "Editing a note is forbidden for security issues!" );
        return;
    }
    struct note* nt = find_note();
    if ( !nt )
    {
        return;
    }
    puts ( "Buffer data:" );
    fgets ( nt->buf, 64, stdin );
}

void list_note()
{
    struct note* nt = find_note();
    if ( !nt )
    {
        return;
    }
    printf ( "Content: %s\n", nt->buf );
}

void del_note()
{
    struct note* nt = find_note();
    if ( !nt )
    {
        return;
    }
    if ( nt->fd )
    {
        nt->fd->bk = nt->bk;
    }
    if ( nt->bk )
    {
        nt->bk->fd = nt->fd;
    }
    free ( nt );
}

