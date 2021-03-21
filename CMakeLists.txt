# CMakeLists.txt for dungeon
cmake_minimum_required(VERSION 3.12)

project(Dungeon VERSION 1.0
	DESCRIPTION "Dungeon: A text adventure game"
	LANGUAGES C)

# Create the executable
add_executable(zork
	actors.c ballop.c clockr.c demons.c dgame.c dinit.c dmain.c
	dso1.c dso2.c dso3.c dso4.c dso5.c dso6.c dso7.c dsub.c dverb1.c
	dverb2.c gdt.c lightp.c local.c nobjs.c np.c np1.c np2.c np3.c
	nrooms.c objcts.c rooms.c sobjs.c supp.c sverbs.c verbs.c villns.c
        funcs.h vars.h parse.h)

# Duplicate the text strings file into the build folder
configure_file(dtextc.dat dtextc.dat COPYONLY)

# Where to install the program
set(BINDIR /usr/games)

# Where to install the data file
set(DATADIR /usr/games/lib)

# Where to install the man page
set(MANDIR /usr/share/man)

# Tell the executable where we installed the dtextc.dat:
target_compile_definitions(zork PRIVATE TEXTFILE="${DATADIR}/dtextc.dat")

# Choose to allow game saving when you set up your initial cmake configuration
option(ALLOW_SAVE_GAME "Allow saving and restoring the game" ON)
if (ALLOW_SAVE_GAME)
    target_compile_definitions(zork PRIVATE ALLOW_SAVE_GAME)
endif ()

# Choose to allow using the shell from in-game when you set up your initial cmake configuration
option(ALLOW_SHELL_COMMANDS "Allow using shell commands from within the game" ON)
if (ALLOW_SHELL_COMMANDS)
    target_compile_definitions(zork PRIVATE ALLOW_SHELL_COMMANDS)
endif ()

# The dungeon program provides a ``more'' facility which tries to
# figure out how many rows the terminal has.  Several mechanisms are
# supported for determining this; the most common one has been left
# uncommented.  If you have trouble, especially when linking, you may
# have to select a different option.

# more option 1: use the termcap routines.  On some systems the LIBS
# variable may need to be set to -lcurses.  On some it may need to
# be /usr/lib/termcap.o.  These options are commented out below.
target_link_libraries(zork termcap)
#target_link_libraries(zork curses)
#target_link_libraries(zork /usr/lib/termcap.o)

# more option 2: use the terminfo routines.  On some systems the LIBS
# variable needs to be -lcursesX, but probably all such systems support
# the termcap routines (option 1) anyhow.
#target_link_libraries(zork curses)
#target_compile_definitions(zork PRIVATE MORE_TERMINFO)

# more option 3: assume all terminals have 24 rows
#target_compile_definitions(zork PRIVATE MORE_24)

# more option 4: don't use the more facility at all
#target_compile_definitions(zork PRIVATE MORE_NONE)

# End of more options


# Uncomment the following line if you want to have access to the game
# debugging tool.  This is invoked by typing "gdt".  It is not much
# use except for debugging.
target_compile_definitions(zork PRIVATE ALLOW_GDT)


# I don't have the original dtextc files to use for porting this portion
# of the Makefile to cmake:
#dtextc.dat:
#	cat dtextc.uu1 dtextc.uu2 dtextc.uu3 dtextc.uu4 | uudecode

# Installation is not important to me at this point. But here is what the Makefile used to say:
#install: zork dtextc.dat
#	mkdir -p $(BINDIR) $(LIBDIR) $(MANDIR)/man6
#	cp zork $(BINDIR)
#	cp dtextc.dat $(DATADIR)
#	cp dungeon.6 $(MANDIR)/man6/


# Choose RelWithDebInfo build type by default:
set(CMAKE_BUILD_TYPE RelWithDebInfo CACHE STRING "Choose the type of build, options are: None Debug Release RelWithDebInfo MinSizeRel ..." FORCE)
