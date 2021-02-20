########################################
# My version of famous game Mastermind #
# colors.py                            #
# Mastermind terminal colors' settings #
#             Piotr Loos (c) 2019-2021 #
########################################


class Color:

    greeting_on = "\033\1331;95m"
    greeting_off = "\033\13322;39m"
    error_on = "\033\1331;4;91m"
    error_off = "\033\13322;24;39m"
    number_on = "\033\1331;94m"
    number_off = "\033\13322;39m"
    attribute_on = "\033\1333m"
    attribute_off = "\033\13323m"
    time_on = "\033\1331;96m"
    time_off = "\033\13322;39m"
    progress_title_on = "\033\1331;94m"
    progress_title_off = "\033\13322;39m"
    progress_value_on = "\033\1331;93m"
    progress_value_off = "\033\13322;39m"
    progress_summary_on = "\033\1331;92m"
    progress_summary_off = "\033\13322;39m"


class NoColor:

    greeting_on = ""
    greeting_off = ""
    error_on = ""
    error_off = ""
    number_on = ""
    number_off = ""
    time_on = ""
    time_off = ""
    attribute_on = "`"
    attribute_off = "`"
    progress_title_on = ""
    progress_title_off = ""
    progress_value_on = ""
    progress_value_off = ""
    progress_summary_on = ""
    progress_summary_off = ""
