#include <unistd.h>

void libc_execve()
{
    const char* argv[] = {"/bin/sh", NULL};
    execve ( argv[0], ( char** ) argv, NULL );
}

void syscall_execve()
{
    asm (
        "mov  rax,0xff978cd091969dd1\n"
        "neg  rax\n"
        "push rax\n"
        "mov  rdi,rsp\n"
        "xor  edx,edx\n"
        "push rdx\n"
        "push rdi\n"
        "mov  rsi,rsp\n"
        "xor  eax,eax\n"
        "mov  al,59\n"
        "syscall"
    );
}

int main()
{
    libc_execve();
    //syscall_execve();
    return -1;
}
