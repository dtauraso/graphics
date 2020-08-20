#  There is one glitch here. We cannot autogenerate state graphs with using a single universal rule(adding a new string to the state name and incrememnting it
#  when there is a neighbor in the trie tree to keep all the state name vectors unique)
#  this is called the adding extra dimentions glitch

#  A solution to this glitch is to make a string shift
#  (x, y, z) => (offsetStringx, offsetStringy, offsetStringz)
#  to allow for the same structure of points (x, y, z) to exist in a different plane

#  We are currently using a generator dependent on the problem domain(number of problems)

#  for the number generating formula:
    #  numbering needs to be in the first name
    #  extra context names need to also be included in the first name

#  The other glitch is this. Each name in the root hash table must be unique or
#  a cell will overwrite another cell

'''
limitations
a function state cannot have a value
you should always access a variable state using the parent state name
a variable state can't have children attributes(a nested value doesn't count as a child)

alowances(not currently imlemented)
children can be variables
variables can store jsObjects as values
submahcines can be treated like hash tables as long as the parent state is used to access them
use flags to keep track of things
make special functions to assume different properties of the states and print out error messages when they fail
'''


def getVariable(graph, parentStateName, variableName):

    # The parent state should only be linked to one variable name at a time
    # in the below example:
    # You can say 'quantity 2' then call it 'quantity' when using it in the reducers
    # as long as the same parent doesn't also have a variable name called 'quantity 3'.
    # This is to allow the user to use variable names with this contextual state chart
    # at a simular level of detail they would use in a programming lnagugae

    cell = graph['nodeGraph2'][parentStateName]  #getCell(graph, parentStateName)

    if not cell:
        return None

    if not cell['variableNames']:
        return None

    variable = None

    variableNameIsInCellVariableNamesCount = 0
    found = False

    for cellVariableName in cell['variableNames']:

        # cell.variableNames.forEach(cellVariableName => {

		# this doesn't work if 1 vaiable name is a substring of the one we are loking for
        if cellVariableName == variableName:
            # return null
            found = True
            # console.log(cellVariableName, Object.keys(graph['nodeGraph2']))
            variable = graph['nodeGraph2'][cellVariableName]
            break


        variableNameIsInCellVariableNamesCount += 1
		# console.log({variable})
        # })

    if variableNameIsInCellVariableNamesCount > 1:
        print(f'You cannot have more than 1 variable name that contains |{variableName}|')
        return None

    if not found:
        print(f'A variable similarly called {variableName} may exist but there is no link from |{parentStateName}| to |{variableName}|')
        return None


    if variable == None:
        print(variableName, 'doesn\'t exist')
        return None

	# print({variable})

    return variable

def setVariable(graph, parentStateName, variableName, newValue):

	# print({parentStateName, variableName, newValue})
    # parentStateName is an array of strings
    variable = getVariable(graph, parentStateName, variableName)
	# print({variable, newValue})
    graph['nodeGraph2'][variable['name']]['value'] = newValue

class ListNode ():
    def __init__(self, currentParent, ithParent, grandParent):

	self.currentParent = currentParent
	self.ithParent = ithParent
	self.grandParent = grandParent

def getIndents(count):

	indent = ''

	while count > 0:
		indent += '    '
		count -= 1

	return indent



def printLevelsBounds(ithState, graph, stateName, indents):
	ourString = graph['input']
	if type(ourString) == 'object':
		ourString = ourString.join(' ')

	print(f'Round #: {ithState} {getIndents(indents)} | state name = \'{stateName}\' | level = {indents} | function =  {graph.nodeGraph2[stateName].function.name} | a = {graph.operationVars.a} | expression = {ourString}\n')

def printVarStore(graph):

	m = graph['input']
	return '|' + graph['input'][m] + '|'


def visitNode(graph, nextState, stateMetrics, parentStateHead):
	
    # used to say undefined not None
	if nextState == None:
		print("the js syntax for the next states is wrong")
		return stateMetrics

	# last round was a pass
	if stateMetrics['passes']:
		return stateMetrics

	state = graph['nodeGraph2'][nextState]
	if not state.function:
		print(state, "doesn't have a function")
		return stateMetrics

	parentState = ''
	if parentStateHead:
		parentState = parentStateHead.currentParent

	else:
		parentState = None

	# update to use a parent state
	# (current_state, graph, parent_state)
	success = state['function'](graph, parentState, nextState)
	if not success:
		return stateMetrics

	stateMetrics['passes'] = true
	stateMetrics['winningStateName'] = nextState
	return stateMetrics

def goDown1Level(graph, machineMetrics, stateMetrics):

	currentState = stateMetrics['winningStateName']
	currentStateObject = graph['nodeGraph2'][currentState]
				
	machineMetrics['parent'] = ListNode(currentStateObject.name, 0, machineMetrics['parent'])
	machineMetrics['indents'] += 1
	machineMetrics['nextStates'] = graph['nodeGraph2'][currentState]['children']
	return machineMetrics

def moveUpParentAndDockIndents(graph, machineMetrics):

	parent = machineMetrics['parent']
	# print('traveling up parent', machine_metrics)
	while parent:
		machineMetrics['indents'] -= 1

		#  console.log({parent})//, state: graph['node_graph2'][parent.current_parent]})
        # used to compare to undefined (next one != undefined)
		if graph['nodeGraph2'][parent.currentParent]['next']:
			if graph['nodeGraph2'][parent.currentParent]['next'].length > 0:


				machineMetrics['nextStates'] = graph['nodeGraph2'][parent.currentParent]['next']
				machineMetrics['parent'] = parent.grandParent
	
				return machineMetrics

		
		else:
			#  we are at a parent end state
			temp = parent
			parent = parent.grandParent
			del temp

	#  guaranteed to have traversed up all end states at end of machine
	machineMetrics['parent'] = None
	machineMetrics['nextStates'] = []
	return machineMetrics

def backtrack(graph, machineMetrics):

	#  go through the parent linked list and look for any remaining unrun children to resume the visitor function on
	print(f'{getIndents(machineMetrics.indents)} failed states L > 2 {machineMetrics.nextStates}')

	count = 0
	#  the second to the nth round of the loop is case 2
	while machineMetrics['parent']:

		machineMetrics['parent'].ithParent += 1

		ithParent = machineMetrics['parent'].ithParent
		currentParent = machineMetrics['parent'].currentParent

		children = graph['nodeGraph2'][currentParent]['children']

		# secondary loop exit
		# case 1
		# we are done if there is at least 1 unrun child
		if ithParent < children.length:

			machineMetrics['nextStates'] = children[ithParent: children.length]

			return machineMetrics

        else:
			# the first round of children will be failed children

            message = 'failed' if count == 0 else 'passed'
            childrenString = ', '.join(children)
            print(f'{getIndents(machineMetrics.indents)} {message} children ${childrenString}')
        
        temp = machineMetrics['parent']
        # case 2.1 can turn into case 2.2 if loop condition breaks
        machineMetrics['parent'] = machineMetrics['parent'].grandParent
        del temp
        machineMetrics['indents'] -= 1
        count += 1

	# case 2.2
	if machineMetrics['parent'] == None:
		# the current state on the highest parent level failed so we cannot continue
		machineMetrics['nextStates'] = []

	return machineMetrics

def visitRedux(graph, startState, indents):

    # does depth first tranversal for each subgraph(each subgraph is a state name that has children)
    # does breath first traversal for within each subgraph

    '''
    3 planes
    plane 1) the parent linked list
    plane 2) a machine defined by the parent state and it's child states 
    plane 3) the layers of machines(plain 2) linked to by the parent states in the linked list
        the layers may changed based on what the parent is at the ith level(you can have a machine where more than
            1 child state is also a parent will eventually be in the parent linked list)
    '''
    # parent3 -> parent2 -> parent1 -> null
    # when we have a state that is a parent
        # add it to the head of the list
    # when machine is over
        # delete nodes from head till we find one with next states length > 0
    # assumes state_name actually runs
    i = 0
    #  start from the state state


    machineMetrics = {
		'nextStates': [startState],
		'parent': None,
		'indents': indents
	}

    while machineMetrics['nextStates'].length > 0:
    	# print(i)
        if i == 75:

            print('we are out of states')
            exit()

        print(getIndents(indents), 'next_states', next_states)
        stateMetrics = {
            passes: false,
            winningStateName: ''
        }
        # machine will stop running if all have failed(there must be more than 0 states for this to be possible) or error state runs
        # loop ends after the first state passes

        for nextState in machineMetrics['nextStates']:

            stateMetrics = visitNode(	graph,
                                        nextState,
                                        stateMetrics,
                                        machineMetrics['parent'])

		# Object.keys(user).forEach(userAttribute => {
		 	# console.log(userAttribute)
		 	# console.log(user[userAttribute])
		#  })
		#  console.log({machine_metrics, state_metrics, graph})
		#  current state passes
        if stateMetrics['passes']:
			#  console.log({mm: machineMetrics})
			printLevelsBounds(i, graph, stateMetrics['winningStateName'], machineMetrics['indents'])

			currentStateName = stateMetrics['winningStateName']
			currentState = graph['nodeGraph2'][currentStateName]
			#  console.log()
			#  current state is a parent
			if currentState['children']:
				#  console.log("here")
				machineMetrics = exports.goDown1Level(graph, machineMetrics, stateMetrics)
				#  console.log({mm: machine_metrics})

			# current state is not a parent but has next states
			elif currentState['next']:
				machineMetrics['nextStates'] = graph['nodeGraph2'][currentStateName]['next']

			# current state is not a parent and has no next states (end state)
			else:
				# console.log('done with machine')
				# console.log({machine_metrics})
				machineMetrics = exports.moveUpParentAndDockIndents(graph, machineMetrics)

        else:

			#  console.log('submachine fails')
			#  submachine fails
			#  if this was recursive this case would return to the children check case above
			machineMetrics = exports.backtrack(graph, machineMetrics)

        i += 1