#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define W 640
#define H 480
#define COLOR 128, 128, 128
#define NUM_CELLS 50
#define MIN_CELL_SPREAD 10
#define NUM_PLY 2
#define MAX_R 20

struct cell {
        int hp, team, x, y, r;
        SDL_Color color;
};
struct ply {
        int team;
        struct cell *c;
};

void init_sdl();
void gen_map(struct cell *c);
void clear();
void event(SDL_Event e);
void init_ply(struct ply *p);
void init_cells(struct cell *c);
void empty(struct cell *c, struct ply *p);
void draw_circle(int x1, int y1, int r);
void render_map(struct cell *c);
int rand_range(int lower, int upper);
int is_overlap(int x1, int x2, int y1, int y2, int r1, int r2);

SDL_Window *window = NULL;
SDL_Renderer *renderer = NULL;
int main(int argc, char *argv[])
{
        init_sdl();

        srand(time(0));
        struct cell *c = malloc(sizeof(struct cell) * NUM_CELLS);
        struct ply *p = malloc(sizeof(struct ply) * 2);
        empty(c, p);
        gen_map(c);
        while (1) {
                clear();
                render_map(c);
                SDL_Event e;
                while (SDL_PollEvent(&e) != 0) {
                        event(e);
                }
                SDL_RenderPresent(renderer);
                SDL_Delay(25);
        }
        return 0;
}

void init_sdl() /* tests if we can make a window or renderer (SDL working) */
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

void gen_map(struct cell *c)
{
        int rr, rx, ry;
        for (int x = 0; x < NUM_CELLS; x++) {
                rr = rand_range(10, MAX_R);
                rx = rand_range(rr, W - rr);
                ry = rand_range(rr, H - rr);
                if (x == 0) {
                        c[x].r = rr;
                        c[x].x = rx;
                        c[x].y = ry;
                        continue;
                }
                for (int i = 0; i < x; i++) {
                        while (is_overlap(rx, c[i].x, ry, c[i].y, rr, c[i].r)) {
                                rx = rand_range(rr, W - rr);
                                ry = rand_range(rr, H - rr);
                                i = 0;
                        }
                }
                c[x].r = rr;
                c[x].x = rx;
                c[x].y = ry;
        }
}

void render_map(struct cell *c)
{
        for (int i = 0; i < NUM_CELLS; i++) {        
                draw_circle(c[i].x, c[i].y, c[i].r);
        }
}

int rand_range(int lower, int upper)
{
        int x = lower + rand() / (RAND_MAX / (upper - lower + 1) + 1);
        return x;
       
}

int is_overlap(int x1, int x2, int y1, int y2, int r1, int r2)
{
        int sqr1 = (x1 - x2) * (x1 - x2);
        int sqr2 = (y1 - y2) * (y1 - y2);
        int rsum = r1 + r2;
        if (sqrt(sqr1 + sqr2) > rsum + MIN_CELL_SPREAD) {
                return 0;
        }
        return 1;
}

void pos_valid(struct cell *c)
{
        /*
        int valid = 0;
        for (int x = 0; x < NUM_CELLS; x++) {
                for (int i = 0; i < NUM_CELLS; i++) {
                        if (c[x].pos.x > c[i].pos.x + 10 &&
                            c[x].pos.x > c[i].pos.y + 10) {
                   
                                valid = 1;
                        }
                }
        }
        return valid;
        */
}

void empty(struct cell *c, struct ply *p)
{
        SDL_Rect null = {0, 0, 0, 0};
        for (int i = 0; i < NUM_PLY; i++) {
                p[i].team = i;
        }
        for (int i = 0; i < NUM_CELLS; i++) {
                c[i].hp = 0;
                c[i].r = 0;
                c[i].team = 0;
                c[i].x = 0;
                c[i].y = 0;
        }
}

void draw_circle(int x1, int y1, int r)
{
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255);
        int x = r - 1;
        int y = 0;
        int dx = 1;
        int dy = 1;
        int err = dx - (r << 1);
        while(x >= y) {
                SDL_RenderDrawPoint(renderer, x1 + x, y1 + y);
                SDL_RenderDrawPoint(renderer, x1 + y, y1 + x);
                SDL_RenderDrawPoint(renderer, x1 - y, y1 + x);
                SDL_RenderDrawPoint(renderer, x1 - x, y1 + y);
                SDL_RenderDrawPoint(renderer, x1 - x, y1 - y);
                SDL_RenderDrawPoint(renderer, x1 - y, y1 - x);
                SDL_RenderDrawPoint(renderer, x1 + y, y1 - x);
                SDL_RenderDrawPoint(renderer, x1 + x, y1 - y);

                if(err <= 0) {
                        y++;
                        dy += 2;
                        err += dy;
                }
                else {
                        x--;
                        dx += 2;
                        err += dx - (r << 1);
                }
        }
}

void clear()
{
        SDL_SetRenderDrawColor(renderer, COLOR, 255);
	SDL_RenderClear(renderer);
}

void event(SDL_Event e)
{
        if (e.type == SDL_QUIT) {
                exit(1);
        }
}
