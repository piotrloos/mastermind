############################################
# My version of the famous Mastermind game #
# class_progress.py                        #
# Progress utility for Mastermind          #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################

from time import time


class Progress:
    """ Displays progress (percentage) during long-taking operations """

    def __init__(
            self,
            items_number,
            style,
            title=None,
            summary=None,
            timing=True,
            update_time_func=None,
            auto_start_stop=True,
    ):
        """ Initializes Progress class object """

        self._style = style

        if title is None:
            self._title = (  # default title
                f"{self._style.progress_title_on}"
                f"[Progress] Thinking..."
                f"{self._style.progress_title_off}"
            )
        else:
            self._title = str(title)  # (str) Progress process title to be displayed

        if summary is None:
            self._summary = (  # default summary
                f"{self._style.progress_summary_on}"
                f"Done!"
                f"{self._style.progress_summary_off}"
            )
        else:
            self._summary = str(summary)  # (str) Progress process summary to be displayed (after finishing)

        if items_number < 1:
            raise ValueError(
                f"{self._style.error_on}"
                f"[Progress] The Progress process must last for one operation at least!"
                f"{self._style.error_off}"
            )

        self._index = 0  # (int) index of current operation
        self._portion = items_number / 100  # (float) 1% of progress to be added to threshold
        self._inv = 100 / items_number  # (float) inversion of portion (to be * instead of /) to get the progress value
        self._threshold = self._portion  # (float) current threshold (start with 1%)
        self._threshold_int = int(round(self._threshold))  # (int) round the threshold to be compared with index

        self._timing = bool(timing)  # (bool) flag whether Progress process should be timed
        self._total_time = 0  # (float) total time in seconds
        self._start_time = None  # (float) last resume start timestamp

        self._update_time_func = update_time_func  # (func) Solver func that allows to overwrite/accumulate solving time

        self._auto_start_stop = bool(auto_start_stop)  # (bool) flag whether Progress should start/stop automatically
        self._running = False  # (bool) flag whether Progress process is currently running
        self._finished = False  # (bool) flag whether Progress process is finished

    def __enter__(self):
        """ Initializes Progress context manager """

        if self._auto_start_stop:
            self.start()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ Ends Progress context manager """

        if self._auto_start_stop:
            self.stop(finish=True)

    @staticmethod
    def _print(string):
        """ Outputs `string` in the same line """

        print(string, end="", flush=True)

    def _print_title_value(self):
        """ Prints `title` and `value` """

        self._print(
            f"\r"  # start from the beginning of line
            f"{self._title} "
            f"{self._style.progress_value_on}"
            f"{int(round(self._index * self._inv)):3d}%"
            f"{self._style.progress_value_off}"
        )

    def _print_value(self):
        """ Prints `value` """

        self._print(
            f"\b\b\b\b"  # 4 backspaces and the new value (in the same place)
            f"{self._style.progress_value_on}"
            f"{int(round(self._index * self._inv)):3d}%"
            f"{self._style.progress_value_off}"
        )

    def _print_summary(self):
        """ Prints `summary` in place of `value` """

        self._print(
            f"\b\b\b\b"  # 4 backspaces and the summary (in the same place)
            f"{self._summary}"
            f"\n"  # finish `progress` and go to the new line
        )

    def _check_state(self, should_be_running):
        """ Checks `finished` and `running` state and raises exception if needed """

        if self._finished:
            raise RuntimeError(
                f"{self._style.error_on}"
                f"[Progress] Progress process is finished!"
                f"{self._style.error_off}"
            )

        if should_be_running and not self._running:
            raise RuntimeError(
                f"{self._style.error_on}"
                f"[Progress] Progress process is not running!"
                f"{self._style.error_off}"
            )

        if not should_be_running and self._running:
            raise RuntimeError(
                f"{self._style.error_on}"
                f"[Progress] Progress process is already running!"
                f"{self._style.error_off}"
            )

    def start(self, title=None):
        """ Starts/resumes printing Progress process and changes `title` text if given """

        self._check_state(should_be_running=False)
        self._running = True

        if title is not None:
            self._title = str(title)

        if self._timing:
            self._start_time = time()

        self._print_title_value()

    def stop(self, finish=False, summary=None):
        """ Stops/pauses printing Progress process and changes `summary` text if given """

        self._check_state(should_be_running=True)
        self._running = False

        if finish:
            self._finished = True

        if summary is not None:
            self._summary = str(summary)  # change `summary` text if given

        if self._timing:

            was_paused = self._total_time != 0  # set the flag if there was some time saved already

            partial_time = time() - self._start_time  # calculate time for last partial operation
            self._total_time += partial_time  # update total time

            if self._update_time_func is not None:
                if not callable(self._update_time_func):
                    raise RuntimeError(
                        f"{self._style.error_on}"
                        f"[Progress] Given invalid `update_time_func` Solver function!"
                        f"{self._style.error_off}"
                    )
                self._update_time_func(self._total_time)  # send total time to Solver

            self._summary += (
                f" ("
            )

            if was_paused or not finish:  # check if it is partial operation
                self._summary += (
                    f"partial "
                )

            self._summary += (
                f"time: "
                f"{self._style.time_on}"
                f"{partial_time:.3f}s"  # time in milliseconds
                f"{self._style.time_off}"
            )

            if was_paused and finish:  # check if it was last execution of partial operation
                self._summary += (
                    f", total time: "
                    f"{self._style.time_on}"
                    f"{self._total_time:.3f}s"  # time in milliseconds
                    f"{self._style.time_off}"
                )

            self._summary += (
                f")"
            )

        self._print_summary()

    def item(self, wrapped_value=None):
        """ Wraps value - checks if next Progress process value should be printed """

        self._index += 1

        if self._index >= self._threshold_int:

            self._check_state(should_be_running=True)

            self._print_value()  # calc the new Progress process value and print it
            self._threshold += self._portion  # (float) set the new threshold
            self._threshold_int = int(round(self._threshold))  # (int) round the threshold to be compared with index

        return wrapped_value
