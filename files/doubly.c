#include <stdio.h>
#include <stdlib.h>

struct cell {
    struct cell *prev;
    int elm;
    struct cell *next;
};

int main()
{
    struct cell *head = NULL;
    struct cell *first = malloc(sizeof(struct cell));
    first->elm = 100;
    first->next = NULL;
    first->prev = NULL;
}
