#include <iostream>
#include <fstream>
#include <vector>
#include <stdio.h>
#include <SDL2/SDL.h>
#include <string>

#define SCR_WIDTH 600
#define SCR_HEIGHT 600
#define SWU SDL_WINDOWPOS_UNDEFINED

using namespace std;

struct controls_t {
    int left;
    int up;
    int right;
    int down;
};

struct settings_t {
    int res_x;
    int res_y;
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
        struct controls_t controls;
        struct settings_t settings;

    Data(string file_name)
    {
        int status = read_file(file_name);
        if (status != 0)
            exit(1);
    }


    string get_key(string line)
    {
        string key = "";
        for (unsigned i = 0; i < line.length(); i++) {
                if (line[i] == ':')
                    break;

                string chr(1, line.at(i));
                key = key + chr;
            }

        cout << "returning key:\t" << key << endl;
        return key;
    }


    string get_val(string line)
    {
        string val = "";
        bool halfway = false;
        for (unsigned i = 0; i < line.length(); i++) {
                if (line[i] == ':') {
                    halfway = true;
                    continue;
                }
                if (!halfway)
                    continue;

                string chr(1, line.at(i));
                val = val + chr;
            }

        cout << "returning val:\t" << val << endl;
        return val;
    }


    void save_setting(string key, string val)
    {
        if (key == "res_x")
            settings.res_x = stoi(val);
        else if (key == "res_y")
            settings.res_y = stoi(val);
        else {
            cout << "\n\"" << key << "\" is not a valid setting\n"
                                     "ignoring..." << endl;
        }
    }


    int read_file(string file_name)
    {
        // note: the character '/' in the settings file
        // marks a line to be ignored
        //
        // the settings file must be in the following format:
        //   setting_name:setting_value
        string line;
        ifstream my_file (file_name.c_str());

        int line_num = 0;
        if (my_file.is_open()) {
            while (getline (my_file, line)) {
                if (line.length() < 1)
                    continue;
                else if (line[0] == '/')
                    continue;

                string key = get_key(line);
                string val = get_val(line);

                if (key == "" || val == "") {
                    cout << "\nerror: no valid setting or value was "
                             "specified" << endl;
                    cout << "line number: " << line_num << endl;
                    cout << "ignoring..." << endl;

                    continue;
                }

                save_setting(key, val);
            }
            my_file.close();
        }
        else {
            cout << "error: no file named \"" << file_name << "\" "
                    "was found in the current working directory" << endl;

            return 1;
        }

        return 0;
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





