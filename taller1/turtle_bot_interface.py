import rclpy
import pygame

from rclpy.node import Node

from geometry_msgs.msg import Twist


class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            Twist,
            'turtlebot_position',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

        #Initialize pygame window
        (width, height) = (500,500)
        background_color = (255,255,255)
        self.screen = pygame.display.set_mode((width,height))
        self.screen.fill(background_color)
        pygame.display.flip()
        self.pos_actual = [250,250]

        


    def listener_callback(self, msg):

        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                self.get_logger().info("Chao")

        if self.pos_actual != (msg.linear.x, msg.linear.y):

            nuevas = self.cordenates(msg.linear.x, msg.linear.y)

            pygame.draw.line(self.screen, (60,179,113), self.pos_actual,nuevas,5)
            pygame.display.update()
            self.pos_actual = nuevas
            self.get_logger().info('pintao')
    

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



def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
