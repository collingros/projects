#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
#define UP 0
#define DOWN 1
#define LEFT 2
#define RIGHT 3

void init();
void event(SDL_Event e, int *quit);
void clear();

struct ply {
	SDL_Rect pos;
	SDL_Rect old_pos;
	int speed;
	int dir;
	SDL_Color color;
	Uint8 up;
	Uint8 down;
	Uint8 left;
	Uint8 right;
	SDL_Rect *wall;
	int wcount;
	int wsize;
	int old_dir;
	int turned;
	SDL_Rect turned_pos;
};
void init_ply(struct ply *p, int x, int y,
	       int r, int g, int b, int dir,
	       Uint8 up, Uint8 down, Uint8 left,
	       Uint8 right);
void render_ply(struct ply *p);
void move_ply(struct ply *p);
void update_keys(Uint8 *state, struct ply *p);
void add_wall(struct ply *p);
int collision(struct ply *p);

const int W = 640;
const int H = 480;
const int PLY_W = 10;
const int PLY_H = 10;
const int PLY_SPEED = 2;

SDL_Window *window = NULL;
SDL_Renderer *renderer = NULL;

int main(int argc, char *argv[])
{
	init();
	struct ply p1, p2;
	init_ply(&p1, 0, H / 2, 90, 90, 90, 3, SDL_GetScancodeFromName("W"),
	         SDL_GetScancodeFromName("S"), SDL_GetScancodeFromName("A"),
	         SDL_GetScancodeFromName("D"));
	init_ply(&p2, W - PLY_W, H / 2, 166, 166, 166, 2,
		 SDL_GetKeyFromName("UP"), SDL_GetScancodeFromName("DOWN"),
		 SDL_GetScancodeFromName("LEFT"),
		 SDL_GetScancodeFromName("RIGHT")); 

	Uint8 *state = NULL;
	int quit = 0;
	while (quit != 1) {
		puts("");
		state = SDL_GetKeyboardState(NULL);

		update_keys(state, &p1);
		update_keys(state, &p2);



		move_ply(&p1);
		move_ply(&p2);

		SDL_Event e;
		while (SDL_PollEvent(&e) != 0) {
			event(e, &quit);
		}

		clear();

		render_ply(&p1);
		render_ply(&p2);

		SDL_RenderPresent(renderer);
		SDL_Delay(25);

		if (collision(&p1)) {
			printf("p1 died\nGame Over\n");
			//getchar();
			//quit = 1;
		}
		/*if (collision(&p2)) {
			printf("p2 died\nGame Over\n");
			//quit = 1;
		}*/
	}

	return 0;
}

void init() /* tests if we can make a window or renderer (SDL working) */
{
	if (SDL_Init(SDL_INIT_VIDEO) < 0) {
		printf("SDL: couldn't init, error: %s\n", SDL_GetError());
		exit(1);
	}

	window = SDL_CreateWindow("CTron", SDL_WINDOWPOS_UNDEFINED,
				  SDL_WINDOWPOS_UNDEFINED, W, H,
				  SDL_WINDOW_SHOWN);
	if (window == NULL) {
		printf("Window: couldn't init, error: %s\n", SDL_GetError());
		exit(1);
	}

	renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
	if (renderer == NULL) {
		printf("Renderer: couldn't init, error: %s\n", SDL_GetError());
		exit(1);
	}
}

void init_ply(struct ply *p, int x, int y,
	       int r, int g, int b, int dir,
	       Uint8 up, Uint8 down, Uint8 left,
	       Uint8 right) /* assign p's properties*/
{
	p->pos.x = x;
	p->pos.y = y;
	p->pos.w = PLY_W;
	p->pos.h = PLY_H;
	p->old_pos = p->pos;
	p->speed = PLY_SPEED;
	p->turned_pos = p->pos;

	p->color.r = r;
	p->color.g = g;
	p->color.b = b;

	p->dir = dir;
	p->turned = 0;
	p->up = up;
	p->down = down;
	p->left = left;
	p->right = right;

	p->wsize = 100;
	p->wall = malloc(sizeof(struct SDL_Rect) * p->wsize);
	p->wcount = 0;
	p->wall[0].x = -10;
	p->wall[0].y = -10;
	p->wall[0].w = 0;
	p->wall[0].h = 0;
}

void add_wall(struct ply *p) /* adds wall to p */
{
	if (p->wsize - (p->wcount + 1) < 0) {
		p->wsize += 100;
		p->wall = realloc(p->wall, sizeof(struct SDL_Rect) *p->wsize);
	}

	p->wall[p->wcount] = p->pos;
	/* if p did not turn, add a wall normally by appending their w/h
	   on to the thickness of the wall */
	if (!p->turned) {
		switch(p->dir) {
		case UP:
			p->wall[p->wcount].y += PLY_H;
			p->wcount++;
			break;
		case DOWN:
			p->wall[p->wcount].y -= PLY_H;
			p->wcount++;
			break;
		case LEFT:
			p->wall[p->wcount].x += PLY_W;
			p->wcount++;
			break;
		case RIGHT:
			p->wall[p->wcount].x -= PLY_W;
			p->wcount++;
			break;
		}
	}
	else {
		
		puts("p turned\n");
		/* for each direction, shorten the wall to fit between where
		   the p started turning and their current position
		   so that it doesnt stick out */
		/*switch(p->dir) {
		case UP:
			p->wall[p->wcount].y += PLY_H;
			p->wcount++;
			break;
		case DOWN:
			p->wall[p->wcount].y -= PLY_H;
			p->wcount++;
			break;
		case LEFT:
			p->wall[p->wcount].x += PLY_W;
			p->wcount++;
			break;
		case RIGHT:
			p->wall[p->wcount].x -= PLY_W;
			p->wcount++;
			break;
		}*/
	}

}

void move_ply(struct ply *p) /* moves p forward by speed in their dir */
{
	switch(p->dir) {
	case UP:
		if (p->pos.y - p->speed >= 0) {
			p->pos.y -= p->speed;
			add_wall(p);
		}
		break;
	case DOWN:
		if (p->pos.y + PLY_H + p->speed <= H) {
			p->pos.y += p->speed;
			add_wall(p);
		}
		break;
	case LEFT:
		if (p->pos.x - p->speed >= 0) {
			p->pos.x -= p->speed;
			add_wall(p);
		}
		break;
	case RIGHT:
		if (p->pos.x + PLY_W + p->speed <= W) {
			p->pos.x += p->speed;
			add_wall(p);
		}
		break;
	}
}

void update_keys(Uint8 *state, struct ply *p) /* chng ply direction if ctrl
						 is pressed */
{
	if (state[p->up] && p->dir != UP && p->dir != DOWN) {
		if (p->pos.x - p->old_pos.x >= 10 && p->dir == RIGHT) {
			p->old_pos = p->pos;
			p->dir = UP;
			p->turned = 1;
			p->turned_pos = p->pos;
		}
		else if (p->old_pos.x - p->pos.x >= 10 && p->dir == LEFT) {
			p->old_pos = p->pos;
			p->dir = UP;
			p->turned = 1;
			p->turned_pos = p->pos;
		}
	}
	else if (state[p->down] && p->dir != UP && p->dir != DOWN) {
		if (p->pos.x - p->old_pos.x >= 10 && p->dir == RIGHT) {
			p->old_pos = p->pos;
			p->dir = DOWN;
			p->turned = 1;
			p->turned_pos = p->pos;
		}
		else if (p->old_pos.x - p->pos.x >= 10 && p->dir == LEFT) {
			p->old_pos = p->pos;
			p->dir = DOWN;
			p->turned = 1;
			p->turned_pos = p->pos;
		}
	}
	else if (state[p->left] && p->dir != LEFT && p->dir != RIGHT) {
		if (p->old_pos.y - p->pos.y >= 10 && p->dir == UP) {
			p->old_pos = p->pos;
			p->dir = LEFT;
			p->turned = 1;
			p->turned_pos = p->pos;
		}
		else if (p->pos.y - p->old_pos.y >= 10 && p->dir == DOWN) {
			p->old_pos = p->pos;
			p->dir = LEFT;
			p->turned = 1;
			p->turned_pos = p->pos;
		}
	}
	else if (state[p->right] && p->dir != LEFT && p->dir != RIGHT) {
		if (p->old_pos.y - p->pos.y >= 10 && p->dir == UP) {
			p->old_pos = p->pos;
			p->dir = RIGHT;
			p->turned = 1;
			p->turned_pos = p->pos;
		}
		else if (p->pos.y - p->old_pos.y >= 10 && p->dir == DOWN) {
			p->old_pos = p->pos;
			p->dir = RIGHT;
			p->turned = 1;
			p->turned_pos = p->pos;
		}
	}
	else
		p->turned = 0;

}

int collision(struct ply *p) /* returns 1 for collision */
{
	int ptop = p->pos.y;
	int pbottom = p->pos.y + p->pos.h;
	int pleft = p->pos.x;
	int pright = p->pos.x + p->pos.w;

	int wtop, wbottom, wleft, wright;
	int collision = 0;
	for (int i = 0; i <= p->wcount; i++) {
		wtop = p->wall[i].y;
		wbottom = p->wall[i].y + p->wall[i].h;
		wleft = p->wall[i].x;
		wright = p->wall[i].x + p->wall[i].w;
		/* impossible for it to have a collision if one of their 
		   axes are not intersecting */
		if (wbottom <= ptop || pbottom <= wtop || 
		    wright <= pleft || pright <= wleft) {
			continue;
		}
		collision = 1;
	}
	if (collision)
		return 1;
	return 0;
}

void render_ply(struct ply *p) /* renders ply and their wall */
{
	for (int i = 0; i < p->wcount; i++) {
		SDL_SetRenderDrawColor(renderer, p->color.r - 10,
				       p->color.g - 10, p->color.b - 10, 255);
        	SDL_RenderFillRect(renderer, (const SDL_Rect*) (&p->wall[i]));
	}

	SDL_SetRenderDrawColor(renderer, p->color.r,
			       p->color.g, p->color.b, 255);
	SDL_RenderFillRect(renderer, (const SDL_Rect*) (&p->pos));
}

void event(SDL_Event e, int *quit) /* processes SDL_Events, used for quitting */
{
	if (e.type == SDL_QUIT) {
		*quit = 1;
	}
}

void clear() /* used to clear background */
{
	SDL_SetRenderDrawColor(renderer, 128, 128, 128, 255);
	SDL_RenderClear(renderer);
}
