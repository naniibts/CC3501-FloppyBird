import pyglet
import numpy as np
from pyglet.gl import *
from pyglet.window import key

import random

import os

root = (os.path.dirname(__file__))

from librerias.scene_graph import *
from librerias import shapes
from librerias.drawables import Model

WIDTH = 1000
HEIGHT = 1000

#Controller
class Controller(pyglet.window.Window):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.time = 0.0
        self.gameState = 0

window = Controller(WIDTH, HEIGHT, "Tarea 2")

if __name__ == "__main__":
    
    vertex_source = """
#version 330

in vec3 position;
in vec2 texCoord;

uniform mat4 u_model = mat4(1.0);
uniform mat4 view = mat4(1.0);
uniform mat4 projection = mat4(1.0);

out vec2 fragTexCoord;

void main() {
    fragTexCoord = texCoord;
    gl_Position = projection * view * u_model * vec4(position, 1.0f);
}
    """
    fragment_source = """
#version 330

in vec2 fragTexCoord;

out vec4 outColor;

uniform sampler2D u_texture;

void main() {
    outColor =  texture(u_texture, fragTexCoord);
    if(outColor.a < 0.1)
        discard;
}
    """

    
    vert_program = pyglet.graphics.shader.Shader(vertex_source, "vertex")
    frag_program = pyglet.graphics.shader.Shader(fragment_source, "fragment")
    pipeline = pyglet.graphics.shader.ShaderProgram(vert_program, frag_program)

    #Grafo de escena
    graph = SceneGraph()
    quad = Model(shapes.Square["position"], shapes.Square["uv"], index_data=shapes.Square["indices"])

    #Grafo adicional para indicaciones
    graph.add_node("press_space", mesh=quad, pipeline=pipeline, texture=Texture(root + "/assets/press_space.png"), scale=[0.7, 0.07, 0.04], position=[0, 0.4, 0], rotation=[0, 0, 0], cull_face=False)
    graph.add_node("restart", mesh=quad, pipeline=pipeline, texture=Texture(root + "/assets/restart.png"), scale=[0, 0, 0], position=[0, -0.1, 0], rotation=[0, 0, 0], cull_face=False)

    #Grafo adicional para start y game over
    graph.add_node("start", mesh=quad, pipeline=pipeline, texture=Texture(root + "/assets/start.png"), scale=[0.4, 0.2, 0.04], position=[0, 0.25, 0], rotation=[0, 0, 0], cull_face=False)
    graph.add_node("gameover", mesh=quad, pipeline=pipeline, texture=Texture(root + "/assets/gameover.png"), scale=[0, 0, 0], position=[0, 0, 0], rotation=[0, 0, 0], cull_face=False)

    #Grafo pajaro y ala
    graph.add_node("wing", mesh=quad, pipeline=pipeline, texture=Texture(root + "/assets/bird_wing.png"), scale=[0.06, 0.04, 0.04], position=[-0.03, 0, 0.0], rotation=[0, 0, 0], cull_face=False)
    graph.add_node("bird", mesh=quad, pipeline=pipeline, texture=Texture(root + "/assets/bird_body.png"), scale = [0.15, 0.1, 0.15], position = [0, 0, 0], cull_face=True)
    
    #Grafo para las tuberias guardandolas en una lista para luego reciclarlas
    pipe_list = []
    gap = 0.5           

    for i in range(5):
        pipe_x = 2.0 + i*1.5
        pipe_y = random.uniform(0, 0.1)

        upper_pipe_name = 'upper_pipe_' + str(i)
        bottom_pipe_name = 'bottom_pipe_' + str(i)
       
        upper_height = 1.0 - (pipe_y + gap / 2)
        bottom_height = (pipe_y - gap / 2) + 1.0

        # Centros de cada tubo
        upper_y = 1.0 - upper_height/2
        bottom_y = -1.0 + bottom_height/2

        #Definimos los grafos con cierto gap para que pase el pajaro y con alturas random
        graph.add_node(upper_pipe_name, mesh=quad, pipeline=pipeline, texture=Texture(root + "/assets/pipe.png"), scale = [0.15, upper_height, 0.15], position = [pipe_x, upper_y, 0], rotation = [0, 0, 0], cull_face=True)
        graph.add_node(bottom_pipe_name, mesh=quad, pipeline=pipeline, texture=Texture(root + "/assets/pipe.png"), scale = [0.15, bottom_height, 0.15], position = [pipe_x, bottom_y, 0], rotation = [0, 0, -3.145], cull_face=True)
        
        #Agregamos a la lista
        pipe_list.append((upper_pipe_name, bottom_pipe_name))
    
    #Grafos para el fondo que se mueve
    graph.add_node("back_1", mesh=quad, pipeline=pipeline, texture=Texture(root + "/assets/back.jpg"), scale = [2.0, 2.0, 2.0], position = [0, 0, 0], cull_face=False)
    graph.add_node("back_2", mesh=quad, pipeline=pipeline, texture=Texture(root + "/assets/back.jpg"), scale = [2.0, 2.0, 2.0], position = [2.0, 0, 0], cull_face=False)


    @window.event
    def on_draw():
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.1, 0.1, 0.1, 0.0)
        window.clear()

        graph.draw()

    def check_collision():
        bird_pos = graph['bird']['position']
        bird_width = graph['bird']['scale'][0]
        bird_height = graph['bird']['scale'][1]
        
        for upper_pipe_name, bottom_pipe_name in pipe_list:
            upper_pos = graph[upper_pipe_name]['position']
            bottom_pos = graph[bottom_pipe_name]['position']
            
            upper_height = graph[upper_pipe_name]['scale'][1]
            bottom_height = graph[bottom_pipe_name]['scale'][1]
            
            # Comprobamos si el pájaro colisiona con el tubo superior o inferior
            if (bird_pos[0] + bird_width / 2 > upper_pos[0] - 0.075 and 
                bird_pos[0] - bird_width / 2 < upper_pos[0] + 0.075 and
                bird_pos[1] + bird_height / 2 > upper_pos[1] - upper_height / 2 and
                bird_pos[1] - bird_height / 2 < upper_pos[1] + upper_height / 2) or \
            (bird_pos[0] + bird_width / 2 > bottom_pos[0] - 0.075 and 
                bird_pos[0] - bird_width / 2 < bottom_pos[0] + 0.075 and
                bird_pos[1] + bird_height / 2 > bottom_pos[1] - bottom_height / 2 and
                bird_pos[1] - bird_height / 2 < bottom_pos[1] + bottom_height / 2):
                return True  # Colisión detectada
        return False  
        
    #Variables Globales para el movimiento de las cosas
    back_speed = 0.0
    bird_speed = 0.0
    gravity = -0.00015
    pipe_speed = 0.0
    pipe_speed_increment = 0.000001

    #Funcion para poder resetear las tuberias al comenxar el juego de nuevo
    def reset_pipe(upper_name, bottom_name, pipe_x):
            pipe_y = random.uniform(0, 0.1)
            gap = 0.5

            upper_height = 1.0 - (pipe_y + gap / 2)
            bottom_height = (pipe_y - gap / 2) + 1.0

            upper_y = 1.0 - upper_height / 2
            bottom_y = bottom_height / 2 - 1.0 

            graph[upper_name]['position'] = [pipe_x, upper_y, 0.0]
            graph[upper_name]['scale'][1] = upper_height

            graph[bottom_name]['position'] = [pipe_x, bottom_y, 0.0]
            graph[bottom_name]['scale'][1] = bottom_height

    #Una pequeña cosita extra, pensé que quedaría chistoso
    linkin = pyglet.resource.media('jiji.mp3', streaming=False)
    linkin_player = pyglet.media.Player()
    linkin_player.queue(linkin)

    @window.event
    def on_key_press(symbol, modifiers):
        global bird_speed, started, back_speed, pipe_speed

        if symbol == key.SPACE: 

            # inicia el juego
            if window.gameState == 0:
                window.gameState = 1
                graph['wing']['rotation'] = [0, 0, -30]
                graph['start']['scale'] = [0, 0, 0]
                graph['press_space']['scale'] = [0, 0, 0]
                linkin_player.play()
                
                #Los objetos adquieren velocidad
                bird_speed = 0.008
                back_speed = 0.01
                pipe_speed = 0.01

            # juego en curso
            if window.gameState == 1:
                bird_speed = 0.008
                graph['wing']['rotation'] = [0, 0, -30]
            
            # juego terminado
            if window.gameState == 2:
                window.gameState = 0
                linkin_player.pause()
                linkin_player.seek(0.0)

                #Reseteamos las posiciones de los objetos
                graph['bird']['position'] = [0, 0, 0]
                graph['wing']['position'] = [-0.03, 0, 0.0]
                graph['wing']['rotation'] = [0, 0, 0]
                graph['press_space']['scale'] = [0.7, 0.07, 0]
                graph['start']['scale'] = [0.4, 0.2, 0]
                graph['gameover']['scale'] = [0, 0, 0]
                graph['restart']['scale'] = [0, 0, 0]

                #Para resetear las tuberias
                i = 0
                for upper_name, bottom_name in pipe_list:
                    pipe_x = 2.0 + i * 1.5
                    reset_pipe(upper_name, bottom_name, pipe_x)
                    i += 1


    #Función para actualizar las tuberias mientras el juego está en curso
    def pipes_update(dt):
        global pipe_list, pipe_speed

        i = 0
        for upper_pipe_name, bottom_pipe_name in pipe_list:
            pos = graph[bottom_pipe_name]['position']
            new_x = pos[0] - pipe_speed

            #Cuando se salen las tuberias de la pantalla vuelven a posicionarse a la derecha
            if new_x < -2.0:
                pipe_x = 2.0 + i * 1.5
                reset_pipe(upper_pipe_name, bottom_pipe_name, pipe_x)
            else:
                #Mover tuberias hacia la izquierda
                graph[upper_pipe_name]['position'] = [new_x, graph[upper_pipe_name]['position'][1], 0.0]
                graph[bottom_pipe_name]['position'] = [new_x, graph[bottom_pipe_name]['position'][1], 0.0]

    #Funcion para que el ala del pajaro vuelva a su posicion luego de apretar espacio
    def reset_wing_rotation(dt):
        graph['wing']['rotation'] = [0, 0, 0]

    #Funcion para actualizar la posicion del fondo cuando se sale de la pantalla
    def background_update(dt):       
       global back_speed 

       if window.gameState != 1:
           return

       for name in ['back_1', 'back_2']:
           pos = graph[name]['position']
           graph[name]['position'] = [pos[0] - back_speed, pos[1], pos[2]]

       pos_1 = graph['back_1']['position']
       pos_2 = graph['back_2']['position']

       if pos_1[0] < -2.0:
           graph['back_1']['position'] = [pos_2[0] + 2.0, pos_1[1], pos_1[2]]
       if pos_2[0] < -2.0:
           graph['back_2']['position'] = [pos_1[0] + 2.0, pos_2[1], pos_2[2]]

    #Funcion para que el pajaro pueda caer e impulsarse
    def bird_update(dt):
        global bird_speed, back_speed, pipe_speed

        if window.gameState == 0:
            return

        bird_pos = graph['bird']['position']
        wing_pos = graph['wing']['position']

        bird_speed += gravity

        graph['bird']['position'] = [bird_pos[0], bird_pos[1] + bird_speed, bird_pos[2]]
        graph['wing']['position'] = [wing_pos[0], wing_pos[1] + bird_speed, wing_pos[2]]

        # Verificar colisión con las tuberías
        if check_collision():
            # Detener el juego
            linkin_player.pause()
            linkin_player.seek(0.0)
            graph['gameover']['scale'] = [1.0, 1.5, 0]
            graph['restart']['scale'] = [0.7, 0.07, 0]

            back_speed = 0
            bird_speed = 0
            pipe_speed = 0
            graph['bird']['position'] = [bird_pos[0], bird_pos[1], bird_pos[2]]
            graph['wing']['position'] = [wing_pos[0], wing_pos[1], wing_pos[2]]

            window.gameState = 2  # Cambiar el estado a "Game Over"

        #Si el pájaro toca el piso el juego se detiene y se resetean algunas cosas
        if bird_pos[1] <= -0.8:
            linkin_player.pause()
            linkin_player.seek(0.0)
            graph['gameover']['scale'] = [1.0, 1.5, 0]
            graph['restart']['scale'] = [0.7, 0.07, 0]

            back_speed = 0
            bird_speed = 0
            pipe_speed = 0
            graph['bird']['position'] = [bird_pos[0], -0.8, bird_pos[2]] 
            graph['wing']['position'] = [wing_pos[0], -0.8, wing_pos[2]] 

            #cambiamos el estado del juego a terminado
            window.gameState = 2

        #Si el pajaro toca el cielo el juego tambien se detiene y se resetean cosas
        if bird_pos[1] >= 0.95:
            linkin_player.pause()
            linkin_player.seek(0.0)
            graph['gameover']['scale'] = [1.0, 1.5, 0]
            graph['restart']['scale'] = [0.7, 0.07, 0]

            back_speed = 0
            bird_speed = 0
            pipe_speed = 0
            graph['bird']['position'] = [bird_pos[0], 0.95, bird_pos[2]] 
            graph['wing']['position'] = [wing_pos[0], 0.95, wing_pos[2]] 
            window.gameState = 2 



    def update(dt):
        # El tiempo queda guardado en la variable window.time
        window.time += dt
        background_update(dt)
        bird_update(dt)
        pipes_update(dt)
        if window.gameState == 1:
            global pipe_speed
            pipe_speed += pipe_speed_increment
        graph.update()



    pyglet.clock.schedule_interval(update, 1/60)
    pyglet.clock.schedule_interval(background_update, 1/60)
    pyglet.clock.schedule_interval(reset_wing_rotation, 0.4)
    pyglet.clock.schedule_interval(bird_update, 1/60)

    pyglet.app.run()

    

    
    
