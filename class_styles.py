############################################
# My version of the famous Mastermind game #
# class_styles.py                          #
# Mastermind terminal styles               #
#           Piotr Loos (c) 2019-2021, 2023 #
############################################


class Color:
    """ Class for styled output """

    # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters

    greeting_on = "\033\1331;95m"               # bold on, pink fg
    greeting_off = "\033\13322;39m"             # bold off, reset fg
    error_on = "\033\1331;91m"                  # bold on, red fg
    error_off = "\033\13322;39m"                # bold off, reset fg
    number_on = "\033\1331;94m"                 # bold on, blue fg
    number_off = "\033\13322;39m"               # bold off, reset fg
    attribute_on = "\033\1333m"                 # italic on
    attribute_off = "\033\13323m"               # italic off
    time_on = "\033\1331;96m"                   # bold on, cyan fg
    time_off = "\033\13322;39m"                 # bold off, reset fg
    response_on = "\033\1331;97m"               # bold on, white fg
    response_off = "\033\13322;39m"             # bold off, reset fg
    progress_title_on = "\033\1331;94m"         # bold on, blue fg
    progress_title_off = "\033\13322;39m"       # bold off, reset fg
    progress_value_on = "\033\1331;93m"         # bold on, yellow fg
    progress_value_off = "\033\13322;39m"       # bold off, reset fg
    progress_summary_on = "\033\1331;92m"       # bold on, green fg
    progress_summary_off = "\033\13322;39m"     # bold off, reset fg
    setting_value_on = "\033\1331;33m"          # bold on, orange fg
    setting_value_off = "\033\13322;39m"        # bold off, reset fg


class NoColor:
    """ Class for non-styled output """

    greeting_on = ""                            # nothing
    greeting_off = ""                           # nothing
    error_on = ""                               # nothing
    error_off = ""                              # nothing
    number_on = ""                              # nothing
    number_off = ""                             # nothing
    time_on = ""                                # nothing
    time_off = ""                               # nothing
    response_on = ""                            # nothing
    response_off = ""                           # nothing
    attribute_on = "`"                          # just single quotes
    attribute_off = "`"                         # just single quotes
    progress_title_on = ""                      # nothing
    progress_title_off = ""                     # nothing
    progress_value_on = ""                      # nothing
    progress_value_off = ""                     # nothing
    progress_summary_on = ""                    # nothing
    progress_summary_off = ""                   # nothing
    setting_value_on = ""                       # nothing
    setting_value_off = ""                      # nothing
