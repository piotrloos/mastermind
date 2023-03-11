############################################
# My version of the famous Mastermind game #
# class_colors.py                          #
# Mastermind terminal colors' settings     #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################


class Color:

    # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

    greeting_on = "\033\1331;95m"               # bold on, pink fg
    greeting_off = "\033\13322;39m"             # bold off, reset fg
    error_on = "\033\1331;4;91m"                # bold on, underline on, red fg
    error_off = "\033\13322;24;39m"             # bold off, underline off, reset fg
    number_on = "\033\1331;94m"                 # bold on, blue fg
    number_off = "\033\13322;39m"               # bold off, reset fg
    attribute_on = "\033\1333m"                 # italic on
    attribute_off = "\033\13323m"               # italic off
    time_on = "\033\1331;96m"                   # bold on, cyan fg
    time_off = "\033\13322;39m"                 # bold off, reset fg
    progress_title_on = "\033\1331;94m"         # bold on, blue fg
    progress_title_off = "\033\13322;39m"       # bold off, reset fg
    progress_value_on = "\033\1331;93m"         # bold on, yellow fg
    progress_value_off = "\033\13322;39m"       # bold off, reset fg
    progress_summary_on = "\033\1331;92m"       # bold on, green fg
    progress_summary_off = "\033\13322;39m"     # bold off, reset fg
    setting_value_on = "\033\1331;33m"          # bold on, orange fg
    setting_value_off = "\033\13322;39m"        # bold off, reset fg


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
    setting_value_on = ""
    setting_value_off = ""
