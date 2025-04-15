# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import tensorflow as tf

from config.settings import MODEL_DIRS


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    model = tf.saved_model.load(MODEL_DIRS[1])
    # 추론 (예측)
    inference = model.signatures["serving_default"]
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
