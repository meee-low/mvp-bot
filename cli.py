import sys
import mvptracker
import time

tracker_backup_file = 'mvp_list_file.txt'  # txt file name here
tracker = mvptracker.MvpTracker(tracker_backup_file)

def main():
    command = sys.argv[1]
    if command == "mvp" and len(sys.argv) > 2:
        mvpCommand(sys.argv)
    elif command == "mvplist":
        mvpListCommand()
    else:
        mvpHelpCommand()

def mvpCommand(input):
    input_string = ' '.join(input)
    mvp = ' '.join(input_string.split(' ')[2:-1])
    input_tod = input_string.split(' ')[-1]
    if input_tod.find(":") > -1:
        time_of_death = tracker.from_input_to_seconds(input_tod)
    else:
        mvpHelpCommand()
        return

    if tracker.update_death(mvp, time_of_death):  # try to update it
        monster_display_name = tracker.find_monster(mvp).display_name
        to_say = "Last known time of death for {} has been updated to: {}".format(monster_display_name, input_tod)
    else:  # if it can't find or update it, it falls here
        to_say = 'Sorry, I could not understand your request. Try using !mvphelp.'

    print(to_say)

def mvpListCommand():
    to_say = 'Current Server Time: {}\n\n'.format(tracker.display_time(tracker.current_time()))
    list_empty = True
    for monster in tracker.relevant_deaths():
        to_say += '{}: {}~{}\n'.format(monster[0], monster[1], monster[2])
        list_empty = False
    if list_empty:
        to_say += 'The MVP list is currently empty.'

    print(to_say)

def mvpHelpCommand():
    to_say = '--!mvp <mvpname> <time of death> -> updates the time of death of an MVP'
    to_say += '\ne.g. !mvp Stormy Knight 03:57'
    to_say += '\nFor bosses with multiple spawn locations, use !mvp mvpname '
    to_say += '(location) timeofdeath; e.g. !mvp Atroce (ve_fild02) 02:03'
    to_say += '\n--!mvplist -> displays the MVPs that respawned recently or that will respawn in the future.'
    to_say += '\nAll time stamps should be in server time and in HH:MM format (24 hour clock).'
    to_say += '\nThis is a work in progress, currently being developed by RoundPiano#0630 and HuiJun#8063.'

    print(to_say)

main()
