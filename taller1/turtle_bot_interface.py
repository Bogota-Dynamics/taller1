import rclpy
import pygame

from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleBotInterface(Node):

    def __init__(self):

        #Inicializar el subscriber
        super().__init__('turtle_bot_interface')
        self.subscription = self.create_subscription(
            Twist,
            'turtlebot_position',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        #Definicion de variables
        self.pos_actual = [275,300]
        self.coords = []
        self.background_color = (255,255,255)

        #Initialize pygame window
        self.screen = pygame.display.set_mode((550,600))
        self.screen.fill(self.background_color)

        #Display button
        self.button1 = Button('Guardar', 120,35,(25,560),self.screen)
        self.button1.draw()

        #Input text
        self.user_text = 'Grafica 1'
        self.input_rect = pygame.Rect((25,10), (500, 30))
        self.input_state = False

        #Rectangulo Area de juego
        self.area_rect = pygame.Rect((25,50), (500, 500))



        

    def listener_callback(self, msg):


        #Para que no se muera pygame 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit() #Cerrar la ventana 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.input_state = True   
                else:
                    self.input_state = False

            if event.type == pygame.KEYDOWN and self.input_state:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    if self.text_surface.get_width()<350:
                        self.user_text += event.unicode

        #Area de juego

        pygame.draw.rect(self.screen, '#9b9b9b', self.area_rect, 5) 
        
        #Nombre de la grafica
        if self.input_state:
            pygame.draw.rect(self.screen, '#9b9b9b', self.input_rect) 
        else:
            pygame.draw.rect(self.screen, (255,255,255), self.input_rect) 

        self.text_surface = pygame.font.Font(None, 35).render(self.user_text, True, '#475F77')
        self.screen.blit(self.text_surface, (self.input_rect.x + ((500-self.text_surface.get_width())/2), self.input_rect.y + 2.5))


        #Guardar Imagen del camino
        if not self.button1.check_click():
            self.get_logger().info("Presionado")




        #Dibujar el camino robot
        if self.pos_actual != (msg.linear.x, msg.linear.y):

            nuevas = self.cordenates(msg.linear.x, msg.linear.y)
            pygame.draw.line(self.screen, (60,179,113), self.pos_actual,nuevas,5)
            pygame.display.update()
            self.pos_actual = nuevas
            #self.get_logger().info(f"Coordenadas: [{nuevas[0]}]")
            self.coords.append(nuevas) # guardar las coordenadas en el archivo


    def cordenates(self,linearx,lineary):
        if linearx>0:
            x = 275+linearx*100
        else:
            x = 275+linearx*100
        if lineary>0:
            y = 300-lineary*100
        else:
            y = 300-lineary*100
        return (x,y)



class Button:
    def __init__(self,text,width,height,pos,screen):
        self.screen = screen
        self.pressed = False
        #Top rectangle
        self.top_rect = pygame.Rect((pos),(width, height))
        self.top_color = '#475F77'

        #Texto Boton
        self.text_surface = pygame.font.Font(None, 25).render(text, True, '#FFFFFF')
        self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=5)
        self.screen.blit(self.text_surface, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                return True
            else:
                if self.pressed == True:
                    self.pressed = False
                    return False
        return True





def main(args=None):
    rclpy.init(args=args)
    pygame.init()
    interface = TurtleBotInterface()
    rclpy.spin(interface)

    interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
