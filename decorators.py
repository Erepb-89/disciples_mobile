# decorators



def second_outer(*dargs, **dkwargs):
    def outer(func):
        def inner(*args, **kwargs):
            # print(param)
            print(*dargs, **dkwargs)
            return func(*args, **kwargs)

        return inner

    return outer
