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
};
void init_ply(struct ply *p, int x, int y,
	       int r, int g, int b, int dir,
	       Uint8 up, Uint8 down, Uint8 left,
	       Uint8 right);
void render_ply(struct ply *p);
int move_ply(struct ply *p);
void update_keys(Uint8 *state, struct ply *p);
void update_wall(struct ply *p);
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
	init_ply(&p1, 0, H / 2, 10, 255, 10, 3, SDL_GetScancodeFromName("W"),
	         SDL_GetScancodeFromName("S"), SDL_GetScancodeFromName("A"),
	         SDL_GetScancodeFromName("D"));
	init_ply(&p2, W - PLY_W, H / 2, 166, 166, 166, 2,
		 SDL_GetKeyFromName("UP"), SDL_GetScancodeFromName("DOWN"),
		 SDL_GetScancodeFromName("LEFT"),
		 SDL_GetScancodeFromName("RIGHT")); 

	Uint8 *state = NULL;
	int quit = 0;
	int bounds = 1;
	while (quit != 1) {
		clear();
		render_ply(&p1);

		SDL_RenderPresent(renderer);

		SDL_Event e;
		while (SDL_PollEvent(&e) != 0) {
			event(e, &quit);
		}

		if (bounds){
			update_wall(&p1);
		}

		state = SDL_GetKeyboardState(NULL);
		update_keys(state, &p1);
		update_keys(state, &p2);
		bounds = move_ply(&p1);


		SDL_Delay(100);

		if (collision(&p1)) {
			//printf("p1 died\n");
		}
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
	       Uint8 right) /* assign player's properties*/
{
	p->pos.x = x;
	p->pos.y = y;
	p->pos.w = PLY_W;
	p->pos.h = PLY_H;
	p->old_pos = p->pos;
	p->speed = PLY_SPEED;
	p->color.r = r;
	p->color.g = g;
	p->color.b = b;
	p->dir = dir;
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
	p->old_dir = 4;
}



void update_wall(struct ply *p)
{
	if (p->wsize - (p->wcount+1) < 0) {
		p->wsize += 100;
		p->wall = realloc(p->wall, sizeof(struct SDL_Rect) * p->wsize);
	}
	if (p->dir != p->old_dir) {
		puts("turned");
		p->wcount++;
		p->wall[p->wcount] = p->pos;
		p->pos.w = 0;
		p->pos.h = 0;
		switch(p->dir) {
		case UP:
			
			break;
		case DOWN:

			break;
		case LEFT:

			break;
		case RIGHT:

			break;
		}
	}
	switch(p->dir) {
	case UP:
		p->wall[p->wcount].y -= p->speed;
		p->wall[p->wcount].h += p->speed;
		p->wall[p->wcount].w = PLY_W;
		break;
	case DOWN:
		p->wall[p->wcount].h += p->speed;
		p->wall[p->wcount].w = PLY_W;
		break;
	case LEFT:
		p->wall[p->wcount].x -= p->speed;
		p->wall[p->wcount].w += p->speed;
		p->wall[p->wcount].h = PLY_H;
		break;
	case RIGHT:
		p->wall[p->wcount].w += p->speed;
		p->wall[p->wcount].h = PLY_H;
		break;
	}

	/*switch(p->dir) {
	case UP:
		
		break;
	case DOWN:

		break;
	case LEFT:

		break;
	case RIGHT:
		if (changed) {
			puts("changed");
			p->wall[p->wcount].x -= 10;
			return;
		}
		else {
			puts("didnt change");
			p->wall[p->wcount].x += 10;
		}
		break;
	}*/
	//p->wall[p->wcount].w = 0;
	//p->wall[p->wcount].h = 0;
}

int move_ply(struct ply *p) /* returns 1 for bounds checks are good */
{
	switch(p->dir) {
	case UP:
		if (p->pos.y - p->speed >= 0) {
			p->pos.y -= p->speed;
			return 1;
		}
		break;
	case DOWN:
		if (p->pos.y + PLY_H + p->speed <= H) {
			p->pos.y += p->speed;
			return 1;
		}
		break;
	case LEFT:
		if (p->pos.x - p->speed >= 0) {
			p->pos.x -= p->speed;
			return 1;
		}
		break;
	case RIGHT:
		if (p->pos.x + PLY_W + p->speed <= W) {
			p->pos.x += p->speed;
			return 1;
		}
		break;
	}
	return 0;
}

void update_keys(Uint8 *state, struct ply *p)
{
	p->old_dir = p->dir;
	if (state[p->up] && p->dir != UP && p->dir != DOWN) {
		if (p->pos.x - p->old_pos.x >= 10 && p->dir == RIGHT) {
			p->old_pos = p->pos;
			p->old_dir = p->dir;
			p->dir = UP;
		}
		else if (p->old_pos.x - p->pos.x >= 10 && p->dir == LEFT) {
			p->old_pos = p->pos;
			p->old_dir = p->dir;
			p->dir = UP;
		}
	}
	else if (state[p->down] && p->dir != UP && p->dir != DOWN) {
		if (p->pos.x - p->old_pos.x >= 10 && p->dir == RIGHT) {
			p->old_pos = p->pos;
			p->old_dir = p->dir;
			p->dir = DOWN;
		}
		else if (p->old_pos.x - p->pos.x >= 10 && p->dir == LEFT) {
			p->old_pos = p->pos;
			p->old_dir = p->dir;
			p->dir = DOWN;
		}
	}
	else if (state[p->left] && p->dir != LEFT && p->dir != RIGHT) {
		if (p->old_pos.y - p->pos.y >= 10 && p->dir == UP) {
			p->old_pos = p->pos;
			p->old_dir = p->dir;
			p->dir = LEFT;
		}
		else if (p->pos.y - p->old_pos.y >= 10 && p->dir == DOWN) {
			p->old_pos = p->pos;
			p->old_dir = p->dir;
			p->dir = LEFT;
		}
	}
	else if (state[p->right] && p->dir != LEFT && p->dir != RIGHT) {
		if (p->old_pos.y - p->pos.y >= 10 && p->dir == UP) {
			p->old_pos = p->pos;
			p->old_dir = p->dir;
			p->dir = RIGHT;
		}
		else if (p->pos.y - p->old_pos.y >= 10 && p->dir == DOWN) {
			p->old_pos = p->pos;
			p->old_dir = p->dir;
			p->dir = RIGHT;
		}
	}
}

int collision(struct ply *p)
{
	int ptop = p->pos.y;
	int pbottom = p->pos.y + p->pos.h;
	int pleft = p->pos.x;
	int pright = p->pos.x + p->pos.w;
	int wtop, wbottom, wleft, wright;
	int collision = 0;
	for (int i = 0; i <= p->wcount; i++) {
		/*printf("i: %d \t wall[i].y: %d \t wall[i].h: %d\n",
			i, p->wall[i].y, p->wall[i].h);*/
		wtop = p->wall[i].y;
		wbottom = p->wall[i].y + p->wall[i].h;
		wleft = p->wall[i].x;
		wright = p->wall[i].x + p->wall[i].w;
		/*printf("wbottom: %d ptop: %d outcome: %d\n",
			wbottom, ptop, wbottom < ptop);*/
		if (!(wbottom < ptop || pbottom < wtop ||
		      wright < pleft || pright < wleft)) {
			return 1;
		}
	}
	return 0;
}

void render_ply(struct ply *p) /* renders ply and their wall */
{
	int i, walls = 0;
	for (i = 0; i <= p->wcount; i++) {
		SDL_SetRenderDrawColor(renderer, 255,
				       0, 0, 255);
        	SDL_RenderFillRect(renderer, (const SDL_Rect*) (&p->wall[i]));
		walls++;
	}
	//printf("walls rendered: %d\n", walls);
	/*printf("last wall rendered info: x: %d y: %d w: %d h: %d\n",
		p->wall[p->wcount].x, p->wall[p->wcount].y,
		p->wall[p->wcount].w, p->wall[p->wcount].h);*/
	SDL_SetRenderDrawColor(renderer, p->color.r,
			       p->color.g, p->color.b, 255);
	SDL_Rect a;
	a = p->pos;
	a.w = 1;
	a.h = 1;
	SDL_RenderFillRect(renderer, (const SDL_Rect*) (&a));
}

void event(SDL_Event e, int *quit) /* processes SDL_Events, used for quitting */
{
	if (e.type == SDL_QUIT) {
		*quit = 1;
	}
}

void clear() /* used to clear background */
{
	SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
	SDL_RenderClear(renderer);
}
