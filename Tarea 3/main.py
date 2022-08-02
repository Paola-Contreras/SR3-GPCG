#Universidad del Valle de Guatemala 
#Gráficos por computador 
#Gabriela Paola Contreras Guerra 20213
#SR3 - OBJ objects 

from gl import Renderer, color, V3, V2

w = 1000
h = 580

rend = Renderer(w, h)

rend.glLoadModel("Ball OBJ.obj",
                 translate = V3(w/2, h/2, 0),
                 scale = V3(210, 210, 210))

rend.glFinish("output.bmp")

