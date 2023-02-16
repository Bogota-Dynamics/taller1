import rclpy
import pygame

from rclpy.node import Node

from geometry_msgs.msg import Twist

coords = []

class TurtleBotInterface(Node):

    def __init__(self):
        super().__init__('turtle_bot_interface')
        self.subscription = self.create_subscription(
            Twist,
            'turtlebot_position',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        #Initialize pygame window
        (width, height) = (500,550)
        background_color = (255,255,255)
        self.screen = pygame.display.set_mode((width,height))
        self.screen.fill(background_color)
        pygame.display.flip()
        self.button1 = Button('Guardar', 100,20,(50,525),self.screen)
        self.pos_actual = [250,250]
    

    def listener_callback(self, msg):
        global coords

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.get_logger().info("Chao")
                pygame.quit()

        self.button1.draw()

        if not self.button1.check_click():
            self.get_logger().info("Presionado")


        if self.pos_actual != (msg.linear.x, msg.linear.y):

            nuevas = self.cordenates(msg.linear.x, msg.linear.y)
            pygame.draw.line(self.screen, (60,179,113), self.pos_actual,nuevas,5)
            pygame.display.update()
            self.pos_actual = nuevas
            self.get_logger().info(f"Coordenadas: [{nuevas[0]}]")
            coords.append(nuevas[0]) # guardar las coordenadas en el archivo

    def cordenates(self,linearx,lineary):
        if linearx>0:
            x = 250+linearx*100
        else:
            x = 250+linearx*100
        if lineary>0:
            y = 250-lineary*100
        else:
            y = 250-lineary*100
        return (x,y)

class Button:
    def __init__(self,text,width,height,pos,screen):
        self.screen = screen
        self.pressed = False
        #Top rectangle
        self.top_rect = pygame.Rect((pos),(width, height))
        self.top_color = '#475F77'

        #Texto Boton
        self.text_surface = pygame.font.Font(None, 20).render(text, True, '#FFFFFF')
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

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
