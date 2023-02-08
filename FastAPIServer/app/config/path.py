import os
import platform
myos = platform.system()
root = r"/app"
def dir_path(param):
    return os.path.join(root, param)

if __name__ == '__main__':
    print(">> "+dir_path("models/chatbot"))
    #a = os.path.dirname(os.path.realpath(__file__))
    #print(a)