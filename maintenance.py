#!/usr/bin/env python3
# -!- encoding:utf8 -!-
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#    file: maintenance.py
#    date: 2017-09-19
#  author: paul.dautry
# purpose:
#       Perform maintenance actions on DB
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#==============================================================================
# IMPORTS
#==============================================================================
import os
from argparse import ArgumentParser
from core.modules import db
from core.modules import ini
#==============================================================================
# FUNCTIONS
#==============================================================================
##
## @brief      { function_description }
##
## @return     { description_of_the_return_value }
##
def __confirm():
    print("Do you really want to run this script ? [yes/n]: ", end='')
    resp=input("");
    if resp != 'yes':
        exit(1)
##
## @brief      { function_description }
##
## @return     { description_of_the_return_value }
##
def __configure(configuration_file):
    # load ini file
    if not ini.init(configuration_file):
        logger.mprint("Configuration file is missing. Server can't be started !")
        exit(1)
    # initialize database
    db.init()
##
## @brief     fixes issue #14:
##                  safe password storage with salt and blowfish encryption
##
##            PATCH DB v1.3.0
##
def fix_issue_14():
    for u in db.get_all_users():
        print("Updating: ", u, "...", end='')
        db.update_user_password(u.id)
        print("done!")
##
## Fix scripts
##
FIXES = {
    14: fix_issue_14
}
##
## @brief      { function_description }
##
## @param      args  The arguments
##
## @return     { description_of_the_return_value }
##
def toggle(args):
    opposite_mode = 'on' if args.mode == 'off' else 'off'
    expected_filename = 'maintenance_{}.html'.format(args.mode)
    opposite_filename = 'maintenance_{}.html'.format(opposite_mode)

    if os.path.isfile(expected_filename):
        print("maintenance mode already: {}".format(args.mode))
        return

    if not os.path.isfile(opposite_filename):
        print("error: missing maintenance_*.html file! Create it first.")
        exit(1)

    print("renaming: {} -> {}".format(opposite_filename, expected_filename))
    os.rename(opposite_filename, expected_filename)
##
## @brief      { function_description }
##
## @param      args  The arguments
##
## @return     { description_of_the_return_value }
##
def fix(args):
    fix_func = FIXES.get(args.issue)
    if fix_func:
        __confirm()
        fix_func()
##
## @brief      { function_description }
##
## @return     { description_of_the_return_value }
##
def main():
    parser = ArgumentParser(description='Maintenance tool for MapIF.')
    parser.add_argument('-c', '--config', default='mapif.ini')
    # -- subparsers
    subparsers = parser.add_subparsers()
    subparsers.required = True
    #subparsers.required = True
    # --- toggle server maintenance mode ON/OFF
    toggle_parser = subparsers.add_parser('toggle')
    toggle_parser.add_argument('mode', choices=['on', 'off'], default='off')
    toggle_parser.set_defaults(func=toggle)
    # --- run a fix script
    fix_parser = subparsers.add_parser('fix')
    fix_parser.add_argument('issue', type=int)
    fix_parser.set_defaults(func=fix)
    #
    args = parser.parse_args()
    #
    __configure(args.config)
    #
    args.func(args)
    #
    exit(0)
#===============================================================================
# SCRIPT
#===============================================================================
if __name__ == '__main__':
    main()
