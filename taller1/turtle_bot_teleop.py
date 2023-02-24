import rclpy
import pynput

from pynput import keyboard

from rclpy.node import Node
from my_msgs.srv import SaveMotions
from os.path import abspath

from geometry_msgs.msg import Twist


class TurtleBotTeleop(Node):

    def __init__(self):
        super().__init__('turtle_bot_teleop')
        self.publisher_ = self.create_publisher(Twist, 'turtlebot_cmdVel', 10)
        listener = keyboard.Listener(on_press=self.on_presss, on_release=self.on_release)
        listener.start()
        self.linear = float(input("Ingrese la velocidad lineal: "))
        self.angular = float(input("Ingrese la velocidad angular: "))
        self.motion = '' # lista de movimientos
        # crear un servicio que guarde la lista de movimientos en un archivo txt
        self.service = self.create_service(SaveMotions, 'save_motion', self.save_motion_callback)
    
    def save_motion_callback(self, request, response):
        filename = 'motion/' + request.filename + '.txt'
        response.path = abspath(filename)
        self.get_logger().info('Writing to file: ' + response.path)

        with open(response.path, 'w') as f:
            f.write(self.motion)
        # retornar el path global del archivo
        return response

    def on_presss(self, key):

        if not(hasattr(key, 'char')): 
            self.get_logger().info('Invalid input')
            return # evitar que muera la terminal
        
        msg = Twist()
        if key.char == 'w':
            msg.linear.x=self.linear
            self.get_logger().info('Publishing:  Adelante')
        elif key.char == 's':
            msg.linear.x=-self.linear
            self.get_logger().info('Publishing: Atras')
        elif key.char == 'a':
            msg.angular.z=self.angular
            self.get_logger().info('Publishing: Izquierda')
        elif key.char == 'd':
            msg.angular.z=-self.angular
            self.get_logger().info('Publishing: Derecha')
        else:
            self.get_logger().info('Invalid input')
            return
        
        self.publisher_.publish(msg)
        self.motion += key.char

    def on_release(self, key):
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
