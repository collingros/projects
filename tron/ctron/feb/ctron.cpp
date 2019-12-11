#include <SDL.h>
#include <stdio.h>
#define up 0
#define down 1
#define right 2
#define left 3
int init();
void quit();
void move(struct player_t *player, int direction);

const int SCREEN_WIDTH = 640;
const int SCREEN_HEIGHT = 480;
const Uint8* currentKeyStates = SDL_GetKeyboardState(NULL);
SDL_Window *window = NULL;
SDL_Surface *screenSurface = NULL;
SDL_Renderer *renderer = NULL;

struct player_t
{
	int speed;
	SDL_Rect rect;
	SDL_Color color;
};

//argc is argcount, size of args[] ()
int main(int argc, char* args[])
{
	if (!init())
	{
		return 1;
	}
	
	SDL_Event e;

	player_t p1;
	p1.speed = 2;
	p1.rect.w = 10;
	p1.rect.h = 10;
	p1.rect.x = 0;
	p1.rect.y = SCREEN_HEIGHT / 2 - p1.rect.h / 2;
	p1.color = {255, 0, 0, 255};

	player_t p2;
	p2.speed = 2;
	p2.rect.w = 10;
	p2.rect.h = 10;
	p2.rect.x = SCREEN_WIDTH - p2.rect.w;
	p2.rect.y = SCREEN_HEIGHT / 2  - p2.rect.h / 2;
	p2.color = {0, 0, 255, 255};

	bool running = true;
	unsigned int lastStep = 0;
	while (running) 
	{
		if (SDL_GetTicks() - lastStep >= 25)
		{
			printf("\n");
			screenSurface = SDL_GetWindowSurface(window);
			SDL_FillRect(screenSurface, NULL, SDL_MapRGB(screenSurface->format, 123, 123, 123));
			SDL_FillRect(screenSurface, &p1.rect, SDL_MapRGB(screenSurface->format, p1.color.r, p1.color.g, p1.color.b));
			SDL_FillRect(screenSurface, &p2.rect, SDL_MapRGB(screenSurface->format, p2.color.r, p2.color.g, p2.color.b));
			
			if(currentKeyStates[SDL_SCANCODE_W])
			{
				move(&p1, up);
			}
			else if(currentKeyStates[SDL_SCANCODE_S])
			{
				move(&p1, down);
			}
			if(currentKeyStates[SDL_SCANCODE_A])
			{
				move(&p1, left);
			}
			else if(currentKeyStates[SDL_SCANCODE_D])
			{
				move(&p1, right);
			}

			if(currentKeyStates[SDL_SCANCODE_UP])
			{
				move(&p2, up);
			}
			else if(currentKeyStates[SDL_SCANCODE_DOWN])
			{
				move(&p2, down);
			}
			else if(currentKeyStates[SDL_SCANCODE_LEFT])
			{
				move(&p2, left);
			}
			else if(currentKeyStates[SDL_SCANCODE_RIGHT])
			{
				move(&p2, right);
			}
			lastStep = SDL_GetTicks();
			SDL_UpdateWindowSurface(window);
		}

		while(SDL_PollEvent(&e) != 0)
			{
				if(e.type == SDL_QUIT){
					running = false;
				}
			}
	}

	quit();

	return 0;
}

int init()
{
	if(SDL_Init(SDL_INIT_VIDEO) < 0)
	{
		printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
		return false;
	}

	window = SDL_CreateWindow("CTron", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, SCREEN_WIDTH, SCREEN_HEIGHT, SDL_WINDOW_SHOWN);

	if(window == NULL)
	{
		printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
		return false;
	}

	renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
	
	if (renderer == NULL)
	{
		printf("fucked renderer\n");
	}

	return true;
}

void quit()
{
	SDL_DestroyWindow(window);
	window = NULL;

	SDL_Quit();
}

void move(struct player_t *player, int direction)
{
	if (direction == up)
	{
		if (player->rect.y - player->rect.h <= 0)
		{
			return;
		}
		printf("up\n");
		player->rect.y -= player->speed;
	}
	else if(direction == down)
	{
		if (player->rect.y + player->rect.h >= SCREEN_HEIGHT)
		{
			return;
		}
		player->rect.y += player->speed;
		printf("down\n");
	}
	else if(direction == right)
	{
		if(player->rect.x + player->rect.w >= SCREEN_WIDTH)
		{
			return;
		}
		player->rect.x += player->speed;
		printf("right\n");
	}
	else if (direction == left)
	{
		if (player->rect.x - player->rect.w <= 0)
		{
			return;
		}
		player->rect.x -= player->speed;
		printf("left\n");
	}
	else
	{
		printf("kys - fucked\n");
	}
}





























