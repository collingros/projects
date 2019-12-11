#include <iostream>
#include <fstream>
#include <vector>
#include <stdio.h>
#include <string>

#include <SDL2/SDL.h>

#define SCR_WIDTH 600
#define SCR_HEIGHT 600
#define SWU SDL_WINDOWPOS_UNDEFINED

using namespace std;

struct controls {
    int left;
    int up;
    int right;
    int down;
};

struct settings {
    int num_cells;
    int res_x;
    int res_y;

    int p1_color;
    int p2_color;
};

class Cell
{
    public:
        int radius; // aka population
        int _x;
        int _y;
        int owner;

    Cell()
    {
        radius = 1;
    }


    void migrate(int num, int newcell)
    {
    
    }

    void render(SDL_Renderer *renderer)
    {
        int x = radius - 1;
        int y = 0;
        int tx = 1;
        int ty = 1;
        int err = tx - (radius << 1); // shifting bits left by 1 effectively
                 // doubles the value. == tx - diameter
        while (x >= y)
        {
            //  Each of the following renders an octant of the circle
            SDL_RenderDrawPoint(renderer, _x + x, _y - y);
            SDL_RenderDrawPoint(renderer, _x + x, _y + y);
            SDL_RenderDrawPoint(renderer, _x - x, _y - y);
            SDL_RenderDrawPoint(renderer, _x - x, _y + y);
            SDL_RenderDrawPoint(renderer, _x + y, _y - x);
            SDL_RenderDrawPoint(renderer, _x + y, _y + x);
            SDL_RenderDrawPoint(renderer, _x - y, _y - x);
            SDL_RenderDrawPoint(renderer, _x - y, _y + x);

            if (err <= 0) {
                y++;
                err += ty;
                ty += 2;
            }
            if (err > 0) {
                x--;
                tx += 2;
                err += tx - (radius << 1);
            }
        }
    }
};


class Player
{
    public:
        SDL_Color color;

    Player(SDL_Color color)
    {
        this->color = color;
    }


    void attack()
    {

    }


    void communicate()
    {

    }
};


class Map
{
    int i;
    vector <Cell> cells;

    public:

    Map()
    {       
        cells.reserve(9);
        for (i = 0; i < 9; i++) {
            cells[i].radius = 10;
            cells[i]._x = 10 * i;
            cells[i]._y = 10 * i;
        }
    }


    void render(SDL_Renderer *renderer)
    {
        for (i = 0; i < 9; i++) {
            cells[i].render(renderer);
        }
    
    }
};


class Screen
{
    public:
        SDL_Window *window;
        SDL_Renderer *renderer;

    Screen()
    {
        // Initialize SDL
        if (SDL_Init(SDL_INIT_VIDEO) < 0) {
            cout << "SDL could not initialize! SDL Error: %s\n"
                 << SDL_GetError();

            exit(EXIT_FAILURE);
        }

        // Create window
        window = SDL_CreateWindow("A shitty game", SWU, SWU, SCR_WIDTH,
                                  SCR_HEIGHT, SDL_WINDOW_SHOWN);
        if (window == NULL) {
            cout << "Window could not be created! SDL Error: %s\n"
                 << SDL_GetError();

            exit(EXIT_FAILURE);
        }

        // Create renderer for window
        renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
        if (renderer == NULL) {
            cout << "Renderer could not be created! SDL Error: %s\n"
                 << SDL_GetError();

            exit(EXIT_FAILURE);
        }
        cout << "Game init success!" << endl;
    }


    void render_players()
    {

    }


    void render_map()
    {

    }
};


class Data
{
    public:
        struct controls;
        struct settings;

    Data(string file_name)
    {
        read_file(file_name);
    }


    void read_file(string file_name)
    {
        string line;
        ifstream my_file (file_name.c_str());
        if (my_file.is_open()) {
            while (getline (my_file, line)) {
                cout << line << "\n";
            }
            my_file.close();
        }
        else {
            cout << "fucked" << endl;
        }

    }


    void init_players()
    {

    }


    void init_map()
    {

    }
};


class Game
{
    string file_name = "settings.txt";

    public:
        Screen screen;
        Data data(string);
        SDL_Event event;
        Map map;

    Game()
    {
        Data data(file_name);
    }


    void run()
    {
        int game_running = true;

        SDL_Rect rect;
        rect.x = 50;
        rect.y = 50;
        rect.w = 50;
        rect.h = 50;

        while (game_running) {
            read_events();

            // clear screen
		    SDL_SetRenderDrawColor(screen.renderer, 0, 0, 0, 255);
		    SDL_RenderClear(screen.renderer);

            // draw red square
		    SDL_SetRenderDrawColor(screen.renderer, 255, 0, 0, 255);
            SDL_RenderFillRect(screen.renderer, &rect);
            map.render(screen.renderer);
            // apply render changes to screen
		    SDL_RenderPresent(screen.renderer);
        }
    }


    void read_events()
    {
        while (SDL_PollEvent(&event) != 0) {
            switch (event.type) {
                case SDL_QUIT:
                    exit(EXIT_SUCCESS);
            }
        }
    }
};


int main(int argc, char **argv)
{
    Game game;
    game.run();

    return 0;
}





