import functools
import time
import timeit


def test_time(n=1000):
    """Execute function multiple times to test the time using timeit."""
    def decorator_test_time(func):
        @functools.wraps(func)
        def wrapper_timeit(*args, **kwargs):
            t_total = timeit.timeit(lambda: func(*args, **kwargs), number=n)
            arg_str = arguments_str(*args, **kwargs)
            print(
                f"Average runtime of {t_total / n:>10.5f} s for "
                f"{func.__name__}({arg_str})."
            )

            return func(*args, **kwargs)

        return wrapper_timeit

    return decorator_test_time


def timer(func):
    """Measure the runtime of a function."""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        t_start = time.perf_counter()
        return_value = func(*args, **kwargs)
        t_end = time.perf_counter()
        t_run = t_end - t_start
        # arg_str = arguments_str(*args, **kwargs)
        # print(f"Runtime of {t_run:>10.5f} s for {func.__name__}({arg_str}).")
        print(f"Runtime of {t_run:>10.5f} s for {func.__name__}.")

        return return_value

    return wrapper_timer


def show_input_output(func):
    """Print the function call and the return values."""
    @functools.wraps(func)
    def wrapper_show_input_output(*args, **kwargs):
        arg_str = arguments_str(*args, **kwargs)
        print(f"Calling: {func.__name__}({arg_str})")
        return_value = func(*args, **kwargs)
        print(f"{'\u2794':^8} {return_value}")

        return return_value

    return wrapper_show_input_output


def arguments_str(*args, **kwargs):
    """Return comma separated string of arguments and keyword arguments."""
    args_strings = [str(arg) for arg in args]
    kwargs_strings = [f"{key}={value}" for key, value in kwargs.items()]

    return ", ".join(args_strings + kwargs_strings)
