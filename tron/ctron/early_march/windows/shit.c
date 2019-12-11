#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
 
#define SWU SDL_WINDOWPOS_UNDEFINED
#define SCR_W 800
#define SCR_H 600
SDL_Window *window = NULL;
SDL_Renderer *renderer = NULL;
 
int main(int argc, char **argv)
{
        if (SDL_Init(SDL_INIT_VIDEO) < 0)
        {
                printf("SDL could not initialize! SDL_Error: %s\n", SDL_GetError());
                exit(1);
        }
 
        window = SDL_CreateWindow("SDL Tutorial", SWU, SWU, SCR_W, SCR_H, SDL_WINDOW_SHOWN);
        if (window == NULL)
        {
                printf("Window could not be created! SDL_Error: %s\n", SDL_GetError());
                exit(1);
        }
       
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
        if (renderer == NULL) {
                printf("Renderer could not be created! SDL Error: %s\n", SDL_GetError());
                exit(1);
        }
    SDL_Rect p;
    p.x = 0;
    p.y = 0;
    p.w = 20;
    p.h = 20;
 
    SDL_Rect r;
    r.x = 200;
    r.y = 200;
    r.w = 20;
    r.y = 20;
 
    Uint8 *keystate;
    SDL_Event event;
        while (1) {
                while (SDL_PollEvent(&event) != 0) {
                        switch (event.type) {
                        case SDL_QUIT:
                                exit(0);
                                break;
                        }
                }
                keystate = SDL_GetKeyboardState(NULL);
                if (keystate[SDL_SCANCODE_W]) {
                        p.y--;
                } else if (keystate[SDL_SCANCODE_A]) {
                        p.x--;
                } else if (keystate[SDL_SCANCODE_S]) {
                        p.y++;
                } else if (keystate[SDL_SCANCODE_D]) {
                        p.x++;
                }
 
                SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
                SDL_RenderClear(renderer);
 
                SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
                SDL_RenderFillRect(renderer, (const SDL_Rect*) &p);
        SDL_RenderFillRect(renderer, (const SDL_Rect*) &r);
        SDL_RenderPresent(renderer);
        SDL_Delay(1);
    }
 
}
