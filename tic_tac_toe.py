'''
Program: CS 115 Program 2
Author: David Tauraso
Description:
This program presents a tic-tac-toe board and allows two players to play
tic-tac-toe.
'''

from graphics import *
from math import *


def getData():

    '''
        This function gets size_of_window, number_of_squares,
        number_of_squares_to_win from the user.

        no assumptions

        no input

        output:
        user_results = [size_of_window, number_of_squares,
        number_of_squares_to_win]
    '''

    size_of_window = int(input("Window side length in pixels: "))
    if size_of_window < 100 or size_of_window > 1000:

        print("Error: must be a number between 100 and 1000.")
        exit()

    number_of_squares = int(input("Number of squares per side: "))

    max_squares = floor(size_of_window / 10)

    if number_of_squares < 3 or number_of_squares > max_squares:

        print("Error: must be a number between 3 and", str(max_squares) + ".")
        exit()

    number_of_squares_to_win = int(input("Squares in a row to win: "))

    if number_of_squares_to_win <= 0 or number_of_squares_to_win > max_squares:

        print("Error: must be a number between 1 and" +
' ' + str(number_of_squares_to_win) + ".")
        exit()

    # Make a list of the results obtained form the user.
    user_results = [size_of_window, number_of_squares,
number_of_squares_to_win]

    return user_results


def drawVerticleLines(user_results):

    '''
        This function draws verticle lines using the data collected from
        getData().

        assumptions:
        user_results has 3 elements
        user_results = [size_of_window, number_of_squares,
        number_of_squares_to_win]

        input:
        user_results

        output:
        window
    '''

    window = GraphWin("Tic-tac-toe", user_results[0], user_results[0])

    # Use the size_of_window / number_of_squares to find the first point_x.
    first_point_x = user_results[0] / user_results[1]

    # The first point starts on the x axis.
    first_point_y = 0

    # Make a point at the other end of the window ensuring the x value
    # is constant.
    second_point_x = first_point_x
    second_point_y = user_results[0]

    number_of_lines = user_results[1] - 1

    # Make and draw line and change the x coordinates.
    for i in range(number_of_lines):

        point_one = Point(first_point_x, first_point_y)
        point_two = Point(second_point_x, second_point_y)
        line = Line(point_one, point_two)
        line.setWidth(2)
        line.draw(window)

        # Increment first_point_x by first_point_x + the distance of size_of
        # window / number_of_squares.
        first_point_x = (user_results[0] / user_results[1]) + first_point_x

        # Set second_point_x to first_point_x for the verticle line.
        second_point_x = first_point_x

    return window


def drawHorizontalLines(user_results, window):

    '''
        TThis function draws verticle lines using the data collected from
        getData().

        assumptions:
        window is a GraphWin object
        user_results has 3 elements
        user_results = [size_of_window, number_of_squares,
        number_of_squares_to_win]

        input:
        window, user_results
    '''

    # Use the size_of_window / number_of_squares to find the first point_y.
    first_point_y = user_results[0] / user_results[1]
    first_point_x = 0

    # Keep both y points the same so the line is horizontal.
    second_point_y = first_point_y
    second_point_x = user_results[0]

    # Only draw the lines that are not the boundaries of the board.
    # If there are n squares on a side, n - 1 dividers have to be drawn.
    # The element user_results[1] = number of squares on a side.
    number_of_lines = user_results[1] - 1

    for i in range(1, user_results[1]):

        point_one = Point(first_point_x, first_point_y)
        point_two = Point(second_point_x, second_point_y)
        line = Line(point_one, point_two)
        line.setWidth(2)
        line.draw(window)

        # Increment first_point_y by first_point_y + the distance of size_of
        # window / number_of_squares.
        # The element user_results[0] = size_of_window.
        first_point_y = (user_results[0] / user_results[1]) + first_point_y

        # Set second_point_y to first_point_y for the hroizontal line.
        second_point_y = first_point_y


def findXCoordinates(user_results, window, point):

    '''
        This function finds the x coordinate from the user click to the record
        board list.

        assumptions:
        user_results has 3 elements
        user_results = [size_of_window, number_of_squares,
        number_of_squares_to_win]
        window is a GraphWin object
        point is a Point object from the user

        input:
        user_results, window, point

        output:
        [point, x_coordinate, first_point_x, second_point_x]
    '''

    # Get the x coordinate from point.
    user_x = point.getX()

    # This is the x coordinate for the first line.
    first_point_x = 0

    # initalize the point for the record_board x coordinate.
    x_coordinate = 0

    for i in range(user_results[1]):

        # increment x_coordinate to follow the loop iterations.
        x_coordinate = x_coordinate + 1

        # Increment second_point_x by first_point_x + the distance of size_of
        # window / number_of_squares.
        second_point_x = (user_results[0] / user_results[1]) + first_point_x

        if first_point_x <= user_x <= second_point_x:

            return [point, x_coordinate, first_point_x, second_point_x]

        else:

            # move first_point_x to the beginning of the next square.
            # (window / number_of_squares) is the distance from the beginning
            # of the first square to the beginning of the second square.
            # (i + 1) is a scalar that increases the more times the loop is run
            first_point_x = (i + 1) * (user_results[0] / user_results[1])


def findYCoordinates(user_results, window, point):

    '''
        This function finds the y coordinate from the user click to the record
        board list.

        assumptions:
        user_results has 3 elements
        user_results = [size_of_window, number_of_squares,
        number_of_squares_to_win]
        window is a GraphWin object
        point is a Point object from the user

        input:
        user_results, window, point

        output:
        [point, x_coordinate, first_point_x, second_point_x]
    '''

    # Get the y coordinate from point.
    user_y = point.getY()

    # This is the y coordinate for the first line
    first_point_y = 0

    # initalize the point for the record_board y coordinate.
    y_coordinate = 0

    for i in range(user_results[1]):

        # increment y_coordinate to follow the loop iterations.
        y_coordinate = y_coordinate + 1

        # Increment second_point_y by first_point_y + the distance of size_of
        # window / number_of_squares.
        second_point_y = (user_results[0] / user_results[1]) + first_point_y

        if first_point_y <= user_y <= second_point_y:

            return_list = [y_coordinate, first_point_y, second_point_y]
            return return_list

        else:

            # Move first_point_y to the beginning of the next square.
            # (window / number_of_squares) is the distance from the beginning
            # of the first square to the beginning of the second square.
            # (i + 1) is a scalar that increases the more times the loop is run
            first_point_y = (i + 1) * (user_results[0] / user_results[1])


def makeRecord(size_of_window):

    '''
        This function makes a record board.

        assumptions:
        size_of_window is an integer

        input:
        size_of_window

        output:
        board
    '''

    # Make a 2d list where the number of sublists = size_of_window.
    board = [[0] * size_of_window for i in range(size_of_window)]

    return board


def makeVisit(size_of_window):

    '''
        This function makes a visit board.

        assumptions:
        size_of_window is an integer

        input:
        size_of_window

        output:
        board
    '''

    # Make a 2d list where the number of sublists = size_of_window.
    # The list is set to False because no one has clicked on a square yet.
    board = [[False] * size_of_window for i in range(size_of_window)]

    return board


def recordUserClicks(point_x, point_y, record_board, player):

    '''
        This function takes the coordinates of the square the user visited
        and sets the position of the record board with the player number.

        assumptions:
        point_x is an integer
        point_y is an integer
        record_board has been made

        input:
        point_x, point_y, record_board, player

        output:
        record_board
    '''

    # Set record_board to player number.
    record_board[point_y - 1][point_x - 1] = player

    return record_board


def recordVisits(point_x, point_y, visit_board, record_board):

    '''
        This function takes the coordinates of the square the user visited
        and sets the position of the vist board with True or False.

        assumptions:
        point_x and point_y are integers
        visite_board has been made
        record board has been made

        input:
        point_x, point_y, visit_board, record_board

        outputs:
        visit_board
    '''

    # Mark the visit_board at the spot the user clicked at on the record_board.
    visit_mark = record_board[point_y - 1][point_x - 1]

    if visit_mark == 0:

        visit_board[point_y - 1][point_x - 1] = True

        return visit_board

    else:

        visit_board[point_y - 1][point_x - 1] = False
        return visit_board


def drawX(lower_x, upper_x, lower_y, upper_y, window):

    '''
        This function draws an x on the square the user clicks on.

        assumptions:
        lower_x, upper_x, lower_y, upper_y are numbers
        upper_x > lower_x and upper_y > lower_y
        window is a GraphWin object

        input:
        lower_x, upper_x, lower_y, upper_y, window

        no output
    '''

    # Make and draw line_one.
    line_one = Line(Point(lower_x, lower_y), Point(upper_x, upper_y))
    line_one.setFill('red')
    line_one.setWidth(2)
    line_one.draw(window)

    # Make and draw line_two.
    line_two = Line(Point(lower_x, upper_y), Point(upper_x, lower_y))
    line_two.setFill('red')
    line_two.setWidth(2)
    line_two.draw(window)


def drawCircle(lower_x, upper_x, lower_y, upper_y, window):

    '''
        This function draws a circle on the square the user clicks on.

        assumptions:
        lower_x, upper_x, lower_y, upper_y are numbers
        upper_x > lower_x and upper_y > lower_y
        window is a GraphWin object

        input:
        lower_x, upper_x, lower_y, upper_y, window

        no output
    '''

    # Go half way from the visited square.
    radius = (upper_x - lower_x) / 2

    # The distance from boundary of board is lower_x and lower_y.
    point_x = lower_x + (upper_x - lower_x) / 2
    point_y = lower_y + (upper_y - lower_y) / 2
    point = Point(point_x, point_y)

    # radius - 2 for extra grid thickness
    # radius - 2 - 5 so circle doesn't get cropped at the top of the board.
    circle = Circle(point, radius - 7)
    circle.setOutline('red')
    circle.setWidth(2)
    circle.draw(window)


def diagonals(record_board, number_of_squares_to_win, number_of_squares):

    '''
        This function records all of the diagonals on the record board.

        assumptions:
        record_board has been made

        input:
        record_board, number_of_squares_to_win, number_of_squares

        output:
        main_list
    '''

    main_list = []

    # Get the length of the first row.
    length = len(record_board[0])

    # Make a range compatible with Python's index style.
    # range(n) = [0, 1, 2, ..., n - 1]
    altered_range = number_of_squares - 1

    # Make the first group of up to down diagonals.
    main_list = upToDownDiagonalsPart1(length, record_board, main_list)

    # Make the second group of up to down diagonals
    # These are made from the bottom up.
    main_list = upToDownDiagonalsPart2(number_of_squares, altered_range,
record_board, main_list)

    # Make the first group of down to up diagonals
    main_list = downToUpDiagonalsPart1(altered_range, length, record_board,
main_list)

    # Make the second group of down to up diagonals
    # These are made from the top down.
    main_list = downToUpDiagonalsPart2(altered_range, record_board,
main_list, number_of_squares)

    main_list = listSive(main_list, number_of_squares_to_win)

    return main_list


def upToDownDiagonalsPart1(length, record_board, main_list):

    '''
        This function records diagonals from the record board.

        assumptions:
        length is an integer
        record_board has been made
        main_list is a list with 0 elements

        input:
        length, record_board, main_list
        output:
        main_list
    '''

    # loop through each pivot column that starts in the first row.
    # For each column get all diagonals starting at column 1.
    for column in range(1, length):

        sub_list = []
        row = 0

        # Change other_column.
        other_column = column

        # The row stops increasing when the column number = 0.
        while other_column >= 0:

            sub_list.append(record_board[row][other_column])
            if column != 0:
                row = row + 1
            other_column = other_column - 1

        main_list.append(sub_list)

    return main_list


def upToDownDiagonalsPart2(number_of_squares, altered_range, record_board,
main_list):

    '''
        This function records diagonals from the record board.

        assumptions:
        record_board has been made
        main_list is a list

        input:
        number_of_squares, altered_range, record_board, main_list

        output:
        main_list
    '''

    # loop through each pivot column that starts in the last row.
    # For each column get all diagonals starting at column 1.
    for column in range(1, altered_range):

        sub_list = []

        # Change row.
        row = altered_range

        # Change other_column.
        other_column = column

        # The row stops decreasing when the column number = 0.
        while other_column < number_of_squares:

            sub_list.append(record_board[row][other_column])
            if other_column != altered_range:

                row = row - 1
            other_column = other_column + 1
        main_list.append(sub_list)

    return main_list


def downToUpDiagonalsPart1(altered_range, length, record_board, main_list):

    '''
        This function records diagonals from the record board.

        assumptions:
        record_board has been made
        main_list is a list

        input:
        altered_range, length, record_board, main_list

        output:
        main_list
    '''

    # loop through each pivot column that starts in the last row.
    # For each column get all diagonals starting at column 1.
    for column in range(1, length):

        sub_list = []
        row = altered_range
        other_column = column

       # The row stops decreasing when the column number = 0.
        while other_column >= 0:

            sub_list.append(record_board[row][other_column])
            if column != 0:
                row = row - 1
            other_column = other_column - 1

        main_list.append(sub_list)

    return main_list


def downToUpDiagonalsPart2(altered_range, record_board, main_list,
number_of_squares):

    '''
        This function records diagonals from the record board.

        assumptions:
        record_board has been made
        main_list is a list

        input:
        number_of_squares, altered_range, record_board, main_list

        output:
        main_list
    '''

    # loop through each pivot column that starts in the last row.
    # For each column get all diagonals starting at column 1.
    for column in range(1, altered_range):

        sub_list = []
        row = 0

        # Change other_column
        other_column = column

        # The row stops decreasing when the column number = 0.
        while other_column < number_of_squares:

            sub_list.append(record_board[row][other_column])

            if other_column != altered_range:

                row = row + 1
            other_column = other_column + 1
        main_list.append(sub_list)

    return main_list


def listSive(main_list, number_of_squares_to_win):

    '''
        This function removes sublists from main_list whose length is less than
        number_of_squares_to_win.

        assumptions:
        main_list has more than 0 elements

        input:
        main_list, number_of_squares_to_win

        output:
        main_list_2
    '''

    main_list_2 = []

    # Only append elements from main_list to main_list_2 if the length of each
    # element is >= number_of_squares_to_win.
    for sub_list_2 in main_list:

        length_of_sub_list = len(sub_list_2)
        if length_of_sub_list >= number_of_squares_to_win:

            main_list_2.append(sub_list_2)

    return main_list_2


def playerStreakMeasure(streak_list):

    '''
        This function determines if a player won or not.

        assumptions:
        streak_list has been made

        input:
        streak_list

        output:
        True or False
    '''

    player_one_total = 0
    player_two_total = 0
    for item in streak_list:

        # Count the number of 1's.
        if item == 1:

            player_one_total = player_one_total + 1

        # Count the number of 2's.
        if item == 2:

            player_two_total = player_two_total + 1

    # Check if either player won.
    if player_one_total == len(streak_list):

        return True

    elif player_two_total == len(streak_list):

        return True

    else:

        return False


def streak(row, number_of_squares_to_win):

    '''
        This function finds if there is a streak and which player won if there
        is a streak.  This function only checks one row at a time.

        assumptions:
        row is a list

        input:
        row, number_of_squares_to_win

        output:
        the number of the player
        player 1: player value = 1
        player 2: player value = 2
    '''

    streak_number = 0
    streak_list = []

    index_of_row = 0
    next_index_of_row = 0

    # Make sure the row index doesn't access a non-existent location in the
    # row.

    while index_of_row <= len(row) - 1:

        streak_list.append(row[index_of_row])

        streak_number = len(streak_list)

        # Get the player number from the row.
        player = row[index_of_row]

        # If the player wins the player number is returned.
        # Check if the number of elements in
        # streak_list = number_of_squares_to_win.
        if streak_number == number_of_squares_to_win:

            next_index_of_row = index_of_row + 1

            if playerStreakMeasure(streak_list):

                return player

            else:

                # Take an item off of streak_list so when another element
                # is added streak_list shifts along the row.
                streak_list = streak_list[1:]

                # Keep program from freezing.
                index_of_row = next_index_of_row

        else:

            index_of_row = index_of_row + 1

    return False


def playerWin(list, number_of_squares_to_win, window):

    '''
        This function determines which player won.

        assumptions:
        window is a GraphWin object
        list has been made

        input:
        list, number_of_squares_to_win, window

        no output
    '''

    player_one_total = 0
    player_two_total = 0

    for row in list:

        # Get the player number if possible.
        player = streak(row, number_of_squares_to_win)

        if player is not False:

            print("Winner: Player", str(player) +
" . Click the window to exit.")
            window.getMouse()
            window.close()
            exit()


def columns(record_board, main_list):

    '''
        This function collects the columns of the record board.

        assumptions:
        record_board, and main_list has been made

        input:
        record_board, main_list

        output:
        main_list
    '''

    for column in range(len(record_board[0])):

        # Initialize sub_list.
        sub_list = []

        # Access record_board with one element in each row.
        # The other_column variable acceses a row in record_board.
        for other_column in range(len(record_board[0])):

            # Append a colunn element from the record_board.
            sub_list.append(record_board[other_column][column])

        main_list.append(sub_list)

    return main_list


def rows(record_board, main_list):

    '''
        This function collects the rows of the record board.

        assumptions:
        record_board, and main_list has been made

        input:
        record_board, main_list

        output:
        main_list
    '''

    # Add each row to main_list.
    for row in record_board:

            main_list.append(row)

    return main_list


def visitSquare(point_x, point_y, visit_board, record_board, player_turn,
window, user_results, player_id):

    '''
        This function finds out if the square has been visited before.

        assumptions:
        point_x, point_y are lists that contain an x coordinate
        and a y coordinate respecitvely
        visit_board has been made
        record_board has been made
        player_turn is an integer
        window is a GraphWin object
        user_results has 3 elements
        user_results = [size_of_window, number_of_squares,
        number_of_squares_to_win]

        input:
        point_x, point_y, visit_board, record_board,
        player_turni, window, user_results, player_id

        output:
        [1, player_turn, number_for_error_message]
        or[0, number_for_error_message]
    '''

    # point_y[0] =  y coordinate
    # point_x[1] = x coordinate
    if visit_board[point_y[0] - 1][point_x[1] - 1] is True:

        # Draw x.
        # point_x[2] = first_point_x
        # point_x[3] = second_point_x
        # point_y[1] = first_point_y
        # point_y[2] = second_point_y
        if player_id == 1:
        
            drawCircle(point_x[2], point_x[3], point_y[1], point_y[2], window)

        else:
        
            drawX(point_x[2], point_x[3], point_y[1], point_y[2],
window)
        # Record click from user.
        record_board = recordUserClicks(point_x[1], point_y[0],
record_board, player_id)

        # Find out if player 2 is the winner.
        # Get all of the possible win lists.
        main_list = diagonals(record_board, user_results[2],
user_results[1])
        main_list = columns(record_board, main_list)
        main_list = rows(record_board, main_list)

        # Find out if player 2 is the winner.
        # Get all of the possible win lists.
        # Gather all of the sublists for checking for winner.
        playerWin(main_list, user_results[2], window)

        player_turn = player_turn + 1
        number_for_error_message = 0

        return [1, player_turn, number_for_error_message]

    else:

        number_for_error_message = 1
        return [0, number_for_error_message]



def player(number_for_error_message, window, user_results, visit_board,
record_board, player_turn, player_id):

    '''
        This function control the visit recording and the drawing on the square
        for player 2.

        assumptions:
        number_for_error_message is an integer
        window is a GraphWin object
        user_results has 3 elements
        user_results = [size_of_window, number_of_squares,
        number_of_squares_to_win]
        visit_board has been made
        record_board has been made
        player_turn is an integer

        input:
        number_for_error_message, window, user_results, visit_board,
        record_board, player_turn, player_id

        output:
        [1, player_turn, number_for_error_message]
        or [0, number_for_error_message]
    '''

    # Check if user visited a square that has been visited before.
    if number_for_error_message == 1:

        print("Error.")
        # i will stay constant and playerTwo will be called.
        # As long as number_for_error_message = 0 the next player will not have
        # a turn.
        number_for_error_message = 0

    # Have player 1 click.
    if player_id == 1:
    
        print("player 1: click a square.")

    else:
    
        print("player 2: click a square.")
    # Get (x, y) coordinates from the user clicking on a square.
    point = window.getMouse()

    # Find the coordinateds of the square the user clicked on.
    point_x = findXCoordinates(user_results, window, point)
    point_y = findYCoordinates(user_results, window, point)

    # Take data from point_x and point_y and use it to record a visit.
    visit_board = recordVisits(point_x[1], point_y[0], visit_board,
record_board)

    # Find out if user has visited a square more than once.
    results = visitSquare(point_x, point_y, visit_board, record_board,
player_turn, window, user_results, player_id)

    if results[0] == 1:

        player_turn = results[1]
        return [1, player_turn, results[2]]

    else:

        number_for_error_message = results[1]
        return [0, number_for_error_message]


def twoPlayers(player_turn, upper_bound, visit_board, record_board, window,
number_for_error_message, user_results):

    '''
        This function alternates between players.
        Each player clicks on the a square.  The square is not drawn if the
        user clicks on a square if it has been visited befoe.

        assumptions:
        player_turn is an integer
        upper_bound = number_of_squares ** 2
        visit_board has been made
        record_board has been made
        window is a GraphWin object
        number_for_error_message is an integer

        input:
        player_turn, upper_bound, visit_board, record_board, window,
        number_for_error_message

        no output
    '''

    player_id = 0
    while player_turn < upper_bound:

            if player_turn % 2 == 0:

                # Run routine for player 1.
                player_id = 1
                number = player(number_for_error_message, window,
user_results, visit_board, record_board, player_turn, player_id)

                # Check for evidence for number_for_error_message.
                if number[0] == 0:

                    number_for_error_message = number[1]
                else:

                    player_turn = number[1]
                    number_for_error_message = number[2]

            else:

                # Run routine for player 2.
                player_id = 2
                number = player(number_for_error_message, window,
user_results, visit_board, record_board, player_turn, player_id)

                # Check for evidence for number_for_error_message.
                if number[0] == 0:

                    number_for_error_message = number[1]

                else:
                    player_turn = number[1]
                    number_for_error_message = number[2]


def main():

    '''
        This function calls other functions and sets up variables up for use
        in other functions.

        no assumptions

        no input

        no output
    '''

    # Get data from user.
    user_results = getData()

    # Draw verticle lines in window.
    window = drawVerticleLines(user_results)

    # Draw horizontal lines in window.
    drawHorizontalLines(user_results, window)

    # Make record_board
    record_board = makeRecord(user_results[1])

    # Make visit_record.
    visit_board = makeVisit(user_results[1])

    # Set the upper_bound to the number_of_squares ** 2 so all unvisited
    # squares can be visited on at least once.  There can be a winner before
    # all of the squares have been visited.
    # user_results[1] = number_of_squares
    upper_bound = user_results[1] ** 2

    player_turn = 0

    # The number_for_error_message variable tells me if the user clicked on a
    # square that has been visited before.
    number_for_error_message = 0

    # Run the 2-player loop.
    twoPlayers(player_turn, upper_bound, visit_board, record_board, window,
number_for_error_message, user_results)

    print("There is no winner. Click the window to exit.")
    window.getMouse()

    window.close()

main()
