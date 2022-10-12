# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
class Server:

    @staticmethod
    def repeat(num_times):
        def decorator_repeat(func):
            def wrapper_repeat(*args, **kwargs):
                for _ in range(num_times):
                    value = func(*args, **kwargs)
                return value

            return wrapper_repeat

        return decorator_repeat


server = Server()


@server.repeat(10)
def print_rama():
    print("hola")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_rama()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
