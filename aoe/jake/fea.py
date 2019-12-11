import sys
import sdl2
import sdl2.ext

sdl2.ext.init()

MAX_X = 640
MAX_Y = 480
red = sdl2.ext.Color(255, 0, 0)
blue = sdl2.ext.Color(0, 0, 255)
green = sdl2.ext.Color(0, 255, 0)

window = sdl2.ext.Window("Hello World!", size=(MAX_X, MAX_Y))
window.show()

renderer = sdl2.ext.Renderer(window)

renderer.color = red # sets the color to be renderered in the following command
renderer.clear() # clear will "clear" the screen with color

renderer.color = blue
renderer.fill( (100, 100, 100, 100) ) # this "fills" an area. a rectangle outline can be created with renderer.draw_rect

renderer.draw_rect( (300, 100, 325, 150) )

renderer.color = green
renderer.draw_line( (200, 200, 300, 300) ) # x1, y1, x2, y2.

#in case you want to fill 1 pixel at a time ...
renderer.draw_point( (400, 400), sdl2.ext.Color(255, 255, 255) ) # you can inline the color as param 2 if you don't want to set renderer.color every time


running = True
last_flash = 0
background_color = red

box_x = 5
box_y = 5
# 1 tick ~= 1ms, 1000ticks = 1s
# sdl2.SDL_GetTicks() returns ticks that program has been running
while running:
    if sdl2.SDL_GetTicks() > 5000:
        renderer.clear(background_color)
    if sdl2.SDL_GetTicks() > 5000 and sdl2.SDL_GetTicks() - last_flash > 500:
        if background_color == red:
            background_color = green
        else:
            background_color = red
        last_flash = sdl2.SDL_GetTicks()
    if background_color == green:
        renderer.fill( (200, 200, 300, 300), red )

    # there are NO BOUNDS CHECKS FOR DRAWING
    # you could draw the box 10,000 units off the screen
    # and it will start overriding system files then your
    # computer will start doing funny things lolololol jk jk
    # here's some nice bounds checking cause we don't
    # want our box to escape the screen, he is forever trapped.
    if box_x + 10 > MAX_X:
        box_x = MAX_X - 10
    elif box_x < 0:
        box_x = 0
    if box_y + 10 > MAX_Y:
        box_y = MAX_Y - 10
    elif box_y < 0:
        box_y = 0
    renderer.fill( (box_x, box_y, 10, 10), blue )

    events = sdl2.ext.get_events()
    for event in events:
        if event.type == sdl2.SDL_QUIT:
            running = False
            break
        elif event.type == sdl2.SDL_KEYDOWN:
            if event.key.keysym.sym == sdl2.SDLK_UP:
                box_y = box_y - 1 # origin is in the top left haha
            elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                box_y = box_y + 1
            elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                box_x = box_x + 1
            elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                box_x = box_x - 1
    renderer.present() # updates renderer, this is critical to ensure your changes actually change
    window.refresh() #updates window

sdl2.ext.quit()
#whats the eta on aoe