import rclpy
import pynput

from pynput import keyboard

from rclpy.node import Node

from geometry_msgs.msg import Twist


class TurtleBotTeleop(Node):

    def __init__(self):
        super().__init__('turtle_bot_teleop')
        self.publisher_ = self.create_publisher(Twist, 'turtlebot_cmdVel', 10)
        listener = keyboard.Listener(on_press=self.on_presss, on_release=self.on_releasee)
        listener.start()
        self.linear = float(input("Ingrese la velocidad lineal: "))
        self.angular = float(input("Ingrese la velocidad angular: "))
    
    def on_presss(self, key):

        if not(hasattr(key, 'char')): 
            self.get_logger().info('Invalid input')
            return # evitar que muera la terminal
        
        if key.char == 'w':

            msg = Twist()
            msg.linear.x=self.linear
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing:  Adelante')

        elif key.char == 's':

            msg = Twist()
            msg.linear.x=-self.linear
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: Atras')

        elif key.char == 'a':

            msg = Twist()
            msg.angular.z=self.angular
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: Izquierda')

        elif key.char == 'd':

            msg = Twist()
            msg.angular.z=-self.angular
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: Derecha')
        
        
    def on_releasee(self, key):
        msg = Twist()
        msg.linear.x=0.0
        msg.angular.z=0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: Stop')
            
        


def main(args=None):
    rclpy.init(args=args)
    
    teleop = TurtleBotTeleop()

    rclpy.spin(teleop)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    teleop.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
