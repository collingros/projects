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
void init_ply(struct ply *player, int x, int y,
	       int r, int g, int b, int dir,
	       Uint8 up, Uint8 down, Uint8 left,
	       Uint8 right);
void render_ply(struct ply *player);
void move_ply(struct ply *player);
void update_keys(Uint8 *state, struct ply *player);
void add_wall(struct ply *player);
int collision(struct ply *player);

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
			getchar();
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

void init_ply(struct ply *player, int x, int y,
	       int r, int g, int b, int dir,
	       Uint8 up, Uint8 down, Uint8 left,
	       Uint8 right) /* assign player's properties*/
{
	player->pos.x = x;
	player->pos.y = y;
	player->pos.w = PLY_W;
	player->pos.h = PLY_H;
	player->old_pos = player->pos;
	player->speed = PLY_SPEED;
	player->color.r = r;
	player->color.g = g;
	player->color.b = b;
	player->dir = dir;
	player->up = up;
	player->down = down;
	player->left = left;
	player->right = right;
	player->wsize = 100;
	player->wall = malloc(sizeof(struct SDL_Rect) * player->wsize);
	player->wcount = 0;
	player->wall[0].x = -10;
	player->wall[0].y = -10;
	player->wall[0].w = 0;
	player->wall[0].h = 0;
	player->old_dir = 4;
}

void add_wall(struct ply *player)
{
	if (player->wsize - (player->wcount + 1) < 0) {
		puts("iqiq");
		player->wsize += 100;
		player->wall = realloc(player->wall, sizeof(struct SDL_Rect) * player->wsize);
	}

	player->wall[player->wcount] = player->pos;
	printf("player->wall[player->wcount].y: %d\n", player->wall[player->wcount].y);
	switch(player->dir) {
	case UP:
		player->wall[player->wcount].y += PLY_H;
		player->wcount++;
		break;
	case DOWN:
		player->wall[player->wcount].y -= PLY_H;
		player->wcount++;
		break;
	case LEFT:
		player->wall[player->wcount].x += PLY_W;
		player->wcount++;
		break;
	case RIGHT:
		player->wall[player->wcount].x -= PLY_W;
		player->wcount++;
		break;
	}
}

void move_ply(struct ply *player) /* move's player forward by speed in their dir */
{
	//printf("old x: %d old y: %d\n", player->pos.x, player->pos.y);
	//printf("old w: %d old h: %d\n", player->pos.w, player->pos.h);
	switch(player->dir) {
	case UP:
		if (player->pos.y - player->speed >= 0) {
			player->pos.y -= player->speed;
		}
		break;
	case DOWN:
		if (player->pos.y + PLY_H + player->speed <= H) {
			player->pos.y += player->speed;
		}
		break;
	case LEFT:
		if (player->pos.x - player->speed >= 0) {
			player->pos.x -= player->speed;
		}
		break;
	case RIGHT:
		if (player->pos.x + PLY_W + player->speed <= W) {
			player->pos.x += player->speed;
		}
		break;
	}
	//printf("new x: %d new y: %d\n", player->pos.x, player->pos.y);
	//printf("new w: %d new h: %d\n\n", player->pos.w, player->pos.h);
}

void update_keys(Uint8 *state, struct ply *player)
{
	if (state[player->up] && player->dir != UP && player->dir != DOWN) {
		if (player->pos.x - player->old_pos.x >= 10 && player->dir == RIGHT) {
			player->old_pos = player->pos;
			player->old_dir = player->dir;
			player->dir = UP;
			add_wall(player);
		}
		else if (player->old_pos.x - player->pos.x >= 10 && player->dir == LEFT) {
			player->old_pos = player->pos;
			player->old_dir = player->dir;
			player->dir = UP;
			add_wall(player);
		}
	}
	else if (state[player->down] && player->dir != UP && player->dir != DOWN) {
		if (player->pos.x - player->old_pos.x >= 10 && player->dir == RIGHT) {
			player->old_pos = player->pos;
			player->old_dir = player->dir;
			player->dir = DOWN;
			add_wall(player);
		}
		else if (player->old_pos.x - player->pos.x >= 10 && player->dir == LEFT) {
			player->old_pos = player->pos;
			player->old_dir = player->dir;
			player->dir = DOWN;
			add_wall(player);
		}
	}
	else if (state[player->left] && player->dir != LEFT && player->dir != RIGHT) {
		if (player->old_pos.y - player->pos.y >= 10 && player->dir == UP) {
			player->old_pos = player->pos;
			player->old_dir = player->dir;
			player->dir = LEFT;
			add_wall(player);
		}
		else if (player->pos.y - player->old_pos.y >= 10 && player->dir == DOWN) {
			player->old_pos = player->pos;
			player->old_dir = player->dir;
			player->dir = LEFT;
			add_wall(player);
		}
	}
	else if (state[player->right] && player->dir != LEFT && player->dir != RIGHT) {
		if (player->old_pos.y - player->pos.y >= 10 && player->dir == UP) {
			player->old_pos = player->pos;
			player->old_dir = player->dir;
			player->dir = RIGHT;
			add_wall(player);
		}
		else if (player->pos.y - player->old_pos.y >= 10 && player->dir == DOWN) {
			player->old_pos = player->pos;
			player->old_dir = player->dir;
			player->dir = RIGHT;
			add_wall(player);
		}
	}

	/*printf("\nwcount: %d\n", player->wcount);
	for (int i = 0; i < player->wcount; i++) {
		printf("\n\ni: %d \twcount: %d\n\n", i, player->wcount);
	}*/
}

int collision(struct ply *player)
{
	int ptop = player->pos.y;
	int pbottom = player->pos.y + player->pos.h;
	int pleft = player->pos.x;
	int pright = player->pos.x + player->pos.w;
	//printf("called collision\n");
	int wtop, wbottom, wleft, wright;
	int collision = 0;
	for (int i = 0; i <= player->wcount; i++) {
		printf("i: %d \t wall[i].y: %d \t wall[i].h: %d\n",
			i, player->wall[i].y, player->wall[i].h);
		wtop = player->wall[i].y;
		wbottom = player->wall[i].y + player->wall[i].h;
		wleft = player->wall[i].x;
		wright = player->wall[i].x + player->wall[i].w;
		printf("wbottom: %d ptop: %d outcome: %d\n",
			wbottom, ptop, wbottom < ptop);
		if (wbottom < ptop || pbottom < wtop ||
		    wright < pleft || pright < wleft) {
			continue;
		}
		collision += 1;
	}
	/*printf("values: ptop : %d pbottom: %d pleft: %d pright: %d\n \
		wtop: %d wbottom: %d wleft: %d wright: %d\n", ptop, pbottom,
		pleft, pright, wtop, wbottom, wleft, wright);*/
	if (collision > 0)
		return 1;
	return 0;
}

void render_ply(struct ply *player) /* renders ply and their wall */
{
	int i;
	//printf("wcount: %d\n", player->wcount);
	for (i = 0; i < player->wcount; i++) {
		SDL_SetRenderDrawColor(renderer, player->color.r - 10,
				       player->color.g - 10, player->color.b - 10, 255);
        	SDL_RenderFillRect(renderer, (const SDL_Rect*) (&player->wall[i]));
	}

	SDL_SetRenderDrawColor(renderer, player->color.r,
			       player->color.g, player->color.b, 255);
	SDL_RenderFillRect(renderer, (const SDL_Rect*) (&player->pos));
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
