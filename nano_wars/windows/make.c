#include <stdlib.h>

int main()
{
        system("gcc nano_wars.c "
	       "-IC:/Users/Collin/Desktop/nano_wars/windows/include "
	       "-LC:/Users/Collin/Desktop/nano_wars/windows/lib -w -lmingw32 "
	       "-lSDL2main -lSDL2 -o run -lws2_32 -lm");
}
