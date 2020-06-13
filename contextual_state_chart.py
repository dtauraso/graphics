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

#  state chart selling point is I made the is from the ground up

#  if they ask about xstate say I wanted to make something similar to prove I could do it

#  can I work with them?
#  can they do the job?
isDebug = True

def appendStates(temporaryState, states):

    # append the states
    # return temporaryState
    return {
        ...temporaryState,
        ...states
    }
}



export const setVariable = (state, parentStateName, variableName, newValue) => {

    // parentStateName is an array of strings
    let variable = getVariable(state, parentStateName, variableName)
    // console.log({variable, newValue})
    return {
        ...state,
        
        [variable.name]: {
            ...variable,
            value: newValue
        }
    }
}

export const setCell = (value) => {
    return value
}

export const getCell = (table, name) => {


    if(Object.keys(table).includes(name)) {
        return table[name]
    }
    return {'error': 'no state'}
}


export const getVariable = (state, parentStateName, variableName) => {

    // The parent state should only be linked to one variable name at a time
    // in the below example:
    // You can say 'quantity 2' then call it 'quantity' when using it in the reducers
    // as long as the same parent doesn't also have a variable name called 'quantity 3'.
    // This is to allow the user to use variable names with this contextual state chart
    // at a simular level of detail they would use in a programming lnagugae

    let cell = getCell(state, parentStateName)

    if(!cell) {
        return null
    }
    if(!Object.keys(cell).includes('variableNames')) {
        return null
    }
    let variable = null

    let variableNameIsInCellVariableNamesCount = 0
    let found = false

    cell.variableNames.forEach(cellVariableName => {
        if(cellVariableName.search(variableName) === -1) {
            return null
        }

        variableNameIsInCellVariableNamesCount += 1
        found = true
        variable = state[cellVariableName]
    })

    if(variableNameIsInCellVariableNamesCount > 1) {
        console.log(`You cannot have more than 1 variable name that contains |${variableName}|`)
        return null
    }
    if(!found) {
        console.log(`A variable similarly called ${variableName} may exist but there is no link from |${parentStateName}| to |${variableName}|`)
        return null

    }
    if(variable === null) {
        console.log(variableName, 'doesn\'t exist')
        return null
    }

    return variable
}

export const getChild = (state, cell, childName) => {

    if(!cell) {
        return null
    }
    if(!Object.keys(cell).includes('children')) {
        return null
    }
    let child = null

    if(cell.children.includes(childName)) {
        child = getCell(state, childName)
    }
    
    return child
}

export const getChildren = (state, stateName) => {

    let cell = getCell(state, stateName)

    if(!cell) {
        return []
    }
    if(!Object.keys(cell).includes('children')) {
        return []
    }
    return cell.children
}

export const tableAssign = (state, cell, value) => {


    if(cell === null) {
        return state
    }
    let cellName = cell.name
    return {
        ...state,
        [cellName]: {
            ...state[cellName],
            value: value
        }
    }    
}

const initCurrentState = (  temporaryState,
                            currentState,
                            iterationCount,
                            newValue) => {
    return {
        ...temporaryState,
        'currentStateVariableChanges': {
            'currentStateName': currentState,
            'iterationCount': iterationCount,
            'firstBefore': {
                'parents' : newValue
            },
            'lastAfter': {
                'parents' : {
                    
                }
            }
        }
    }
}

const updateParents = ( temporaryState,
                        timeLabel,
                        parentStateName,
                        newValue) => {

    return {
        ...temporaryState,
        'currentStateVariableChanges': {
            ...temporaryState['currentStateVariableChanges'],
            [timeLabel] : {
                ...temporaryState['currentStateVariableChanges'][timeLabel],
                'parents' : {
                    ...temporaryState['currentStateVariableChanges'][timeLabel]['parents'],
                    [parentStateName]: newValue
                }
            }
        }
    }
}

const  resetCurrentState = (    temporaryState,
                                currentState,
                                timeLabel,
                                iterationCount,
                                newValue) => {

    return {
        ...temporaryState,
        'currentStateVariableChanges': {
            'currentStateName': currentState,
            'iterationCount': iterationCount,
            [timeLabel]: {
                'parents' : newValue
            }
        }
    }
    
}

// 'currentStateVariableChanges' is an illegal state name as it's needed to track variable changes
export const set = (state, action, parentStateName, targetVar, dependencyVars, cb) => {

    // save the data and track changes made to the vars as each set call is run from a reducer function
    // console.log({parentStateName, targetVar})
    // store by 'current state'
    /*
        state['current_state']: {
            current_state: action.type,
            ithRun: state[action.type].ithRun,
            firstBefore: {},
            lastAfter: {}
        }
    */
    // redesign this
    // before we change the variable
    let currentStateName = action.type
    let iterationCount = state[action.type].iterationCount
    let temporaryState = state

    if(temporaryState['currentStateVariableChanges'] === undefined) {
        // we are at the first call to set in entire machine
        let variable = getVariable(state, parentStateName, targetVar)

        temporaryState = initCurrentState(  temporaryState,
                                            action.type,
                                            temporaryState[action.type].iterationCount,
                                            {[targetVar]: variable.value})

    }
    else {
        let currentProgressReport = temporaryState['currentStateVariableChanges']
        // console.log(currentProgressReport)
        // let searchKeys = Object.keys(currentProgressReport)
        if( currentProgressReport.currentStateName === currentStateName &&
            currentProgressReport.iterationCount === iterationCount) {
            // we are at the second or nth set call 
            // update old stuff
            let variable = getVariable(state, parentStateName, targetVar)
            // console.log(targetVar, temporaryState[targetVar])

           const timeLabel = 'firstBefore'
           temporaryState = updateParents(  temporaryState,
                                            timeLabel,
                                            parentStateName,
                                            {...(temporaryState['currentStateVariableChanges'][timeLabel]['parents'][parentStateName] !== undefined?
                                                    temporaryState['currentStateVariableChanges'][timeLabel]['parents'][parentStateName]:
                                                    {}),
                                                [targetVar]: variable.value
                                            })

        }
        else {
            // we are at the first set call for our current state and iteration count
            // reset old data and start with new stuff
            let variable = getVariable(state, parentStateName, targetVar)
            // console.log(targetVar, temporaryState[targetVar])

           temporaryState = resetCurrentState( temporaryState,
                                                action.type,
                                                'firstBefore',
                                                temporaryState[action.type].iterationCount,
                                                {[parentStateName]: { [targetVar]: variable.value}})
        }
    
    }
   
    // store the first before and overwrite the afters
    // 
    // we can't assume parentStateName is always the parent of the current state
    // if the parent is not a parent of current state how do we know when the last call to set is being made?

    // targetVar is a variable name
    if(typeof dependencyVars !== 'object') {

        temporaryState = tableAssign(
                                    temporaryState,
                                    getVariable(temporaryState, parentStateName, targetVar),
                                    dependencyVars)

    }
    else {
        temporaryState = tableAssign(
                                    temporaryState,
                                    getVariable(temporaryState, parentStateName, targetVar),
                                    // apply cb to list of variables
                                    cb(...dependencyVars.map(variableName => getVariable(   temporaryState,
                                                                                            parentStateName,
                                                                                            variableName).value)))
    }

    let currentProgressReport = temporaryState['currentStateVariableChanges']

    if( currentProgressReport.currentStateName === currentStateName &&
        currentProgressReport.iterationCount === iterationCount) {
        // we are at the second or nth set call 
        // update old stuff
        let variable = getVariable(state, parentStateName, targetVar)

        
       const timeLabel = 'lastAfter'
       temporaryState = updateParents(  temporaryState,
                                        timeLabel,
                                        parentStateName,
                                        {...(temporaryState['currentStateVariableChanges'][timeLabel]['parents'][parentStateName] !== undefined?
                                            temporaryState['currentStateVariableChanges'][timeLabel]['parents'][parentStateName]:
                                            {}),
                                            // targetVar is a variable name
                                            [targetVar]: typeof dependencyVars !== 'object'?
                                                        dependencyVars:
                                                    cb(...dependencyVars.map(variableName => getVariable(state, parentStateName, variableName).value))
                                        })

    }
    else {
        // we are at the first set call for our current state and iteration count
        // reset old data and start with new stuff
        let variable = getVariable(state, parentStateName, targetVar)
        // console.log(targetVar, temporaryState[targetVar])


       temporaryState = resetCurrentState(  temporaryState,
                                            action.type,
                                            'lastAfter',
                                            temporaryState[action.type].iterationCount,
                                            {[parentStateName]: { [targetVar]: variable.value}})

    }
    return temporaryState

    // save the data inside the table
    // test if we are in the current state or not
    // update stuff
    // return the table
}


export const setArray = (state, parentStateName, targetVar, array) => {

    // array is an object
    return tableAssign(
        state,
        getVariable(state, parentStateName, targetVar),
        array
    )
}

const hasSubstates = (cell) => {
    if(!Object.keys(cell).includes('substates')) {
        return false
    }
    else if(Object.keys(cell.substates).length === 0) {
        return false
    }
    else {
        return true
    }
}

const hasAttributeOfCollection = (cell, attributeName) => {
    if(!Object.keys(cell).includes(attributeName)) {
        return false
    }
    else if(cell[attributeName].length === 0) {
        return false
    }
    else {
        return true
    }

}
const hasAttribute = (cell, attributeName) => {
    if(!Object.keys(cell).includes(attributeName)) {
        return false
    }
    else {
        return true
    }
}
export const treeVisualizer = (table, currentState) => {

    // treat each cell as if only 1 function call maps to 1 cell
    /*
    cell(full name here)
    children
    variables
    substates: [
        {
        cell(full name here)
        children
        variables
        substates: []
        }
    ]
    */
//    console.log('current state name', currentState)
    // if any child state has more than 1 parent this will return misleading information
    let cell = getCell(table, currentState)
    if(!cell) {
        return {}
    }
    // if(hasAttribute(cell, 'value')) {
    //     return {value: cell.value}
    // }
    // this is why a child state with a value gets messed up
    else if(hasAttribute(cell, 'value')) {
        return {name: cell.name, value: cell.value}
    }

    let variables = {}
    if(hasAttributeOfCollection(cell, 'variableNames')) {

        cell.variableNames.forEach(variableStateName => {
            variables = {
                ...variables,

                // should return a tree of states
                [variableStateName]: {...treeVisualizer(table,
                                                variableStateName)}
            }
        })
    }

    let children = []
    if(hasAttributeOfCollection(cell, 'children')) {

        cell.children.forEach(childStateName => {

            // should return a tree of states
            children = [...children,
                        treeVisualizer(table,
                                childStateName)]
        })
    }

    let substates = []
    if(hasSubstates(cell)) {

        // visit subtrees here
        // console.log('current state', currentState, 'substates', cell.substates)
        cell.substates.forEach(substate => {
            // console.log('substate name', currentState + ' ' + substate)
            // get the next nested granular state within currentState
            substates = [
                ...substates,
                treeVisualizer(table,
                        currentState + ' ' + substate)
                ]
        })
    }
    
    return {
            // 'a', 'b', and 'c' parts are so this is the order they show up in the console
            a_name: cell.name,
            ...(cell.functionCode === undefined? {} : {b_function: cell.functionCode.name}),
            ...(cell.iterationCount === undefined? {} : {c_iterationCount: cell.iterationCount}),
            ...(cell.nextStates === undefined? {} : {d_nextStates: cell.nextStates}),
            e_children: children,
            f_variables: variables,
            substates: substates  
    }
}
export const printTreeInteractive = (state) => {
    let elementarySchoolName = 'elementarySchool'
    let x = treeVisualizer(state, elementarySchoolName)
    console.log('tree', x)

}

export const breathFirstTraversal = (state, action, startStateName, levelId, stateChartHistory) => {
    // startStateName is a string

    // we can use the payload from the user for the entire traversal
    // traverse from start state to end state

    // dft for each level with bft for each node in the level
    // try all the options
    // for each one
        // return the state then the stateSuceded flag
        // if it passes try it's children

    // return the state once endState is reached
    // assume each occurrence of this function on the callstack represents the outcome of the state machine
    // [state, pass/fail status]

    // This function will create a stack overflow if the state chart tree has an infinite loop from any cycles

    
    // this will cumulatively hold the state copies untill we are done with the machine
    let temporaryState = state
    // console.log("level", levelId)
    let nextStates = startStateName
    let currentStateName = startStateName

    while(true) {
        // record each state as it passes
        //  [{treeBefore: temporaryState, stateName, functionName, treeAfter: temporaryStateAfter, submachine: [path of states]}]
        // pass the tree down the call stack to save each state after it's run
        // return the tree up the call stack to replace the old version above it
        // console.log(nextStates)
        let passes = false
        let winningStateName = ''
        let stateFunctionPair = []
        nextStates.forEach(nextState => {

            /* {
                didFunctionFail,   // Did we hit any (return null)'s ?
                passes,
                winningStateName,
                temporaryState,
                stateFunctionPair,
                stateChartHistory} = visitNode( temporaryState, 
                                                nextState,
                                                action,
                                                stateFunctionPair,
                                                stateChartHistory,
                                                isDebug,
                                                levelId)
            */
            // console.log('trying', nextState)
            if(nextState === undefined) {
                console.log("the js syntax for the next states is wrong")
                return null

            }

            if(passes) {
                return null
            }
            // console.log("getting state", temporaryState, nextState, stateChartHistory) 
            let cell = getCell(temporaryState, nextState)
            // console.log('cell found', cell.name)
            // ignore the state if it doesn't have a function to run
            if(!Object.keys(cell).includes('functionCode')) {
                console.log(cell, "doesn't have a function")
                return null
            }
            // make sure the set call knows what state we are on even if it's a loop with a single state
            if(!Object.keys(cell).includes('iterationCount')) {
                // put in iterationCount
                temporaryState = {
                    ...temporaryState,
                    [cell.name] : {
                        ...temporaryState[cell.name],
                        iterationCount: 0
                    }
                }
            }
            
            // action.type is the parent state untill this line is run(in the first level the parent == current state)
            // console.log('parent state', action.meta.parentStateName)
            action.type = nextState
            // console.log('got here')
            // action's current state is .type
            // action.meta.currentState = nextState // bad idea
            // console.log("function to run", getValue(temporaryState, nextState), action)
            // save tree here
            const result = cell['functionCode'](temporaryState, action)
            const success = result[1]
            // console.log("finished function")
            // console.log(temporaryState, success)
            if(!success) {
                stateFunctionPair = [...stateFunctionPair, {state: cell.name, functionCode: cell['functionCode'].name}]
                return null
            }

            // must keep the success value as we go up and down the call stack
            temporaryState = result[0]

            let before = null
            let after = null
            // console.log({ourDiff: temporaryState['currentState']})
            if(temporaryState['currentStateVariableChanges'] !== undefined) {
                if(temporaryState['currentStateVariableChanges']['firstBefore'] !== undefined) {
                    before = {...temporaryState['currentStateVariableChanges']['firstBefore']}
            
                }
                if(temporaryState['currentStateVariableChanges']['lastAfter'] !== undefined) {
                    after = {...temporaryState['currentStateVariableChanges']['lastAfter']}
                }
            }
            // reset currentState here as we now know all the set functions have been run
            //  blankOutCurrentState(result[0]) => deletes it
            // save the state and function name here
            // get the before and after data from the 'currentState' entry in state
            stateChartHistory = {   ...stateChartHistory,
                                    [Object.keys(stateChartHistory).length] : {
                                                                a_before: before,
                                                                stateName: nextState,
                                                                functionName: cell['functionCode'].name,
                                                                z_after: after
                                                            }
                                                                // a_before
                                                                // z_after
                                                                // so order in the console will be
                                                                // a_before, stateName, functionName, z_after
                                }
            // erase currentStateVariableChanges so set will init a new one the first time it runs in a function
            delete temporaryState['currentStateVariableChanges']

            temporaryState = {
                ...temporaryState,
                [cell.name] : {
                    ...temporaryState[cell.name],
                    iterationCount: temporaryState[cell.name].iterationCount += 1
                }
            }
            if(isDebug) {
                console.log({stateChartHistory})
            }


            passes = true
            winningStateName = nextState
            // action.type = winningStateName
            // console.log('passes', action.type)
            // console.log()
            // untested
            // if the winningStateName has any children
            let childrenStates = getChildren(temporaryState, winningStateName)
            // console.log('children states', childrenStates)
            if(childrenStates === null) {
                return null
            }
            if(childrenStates.length === 0) {
                return null
            }
            // console.log("we have children", childrenStates)
            // as we go down the machine the current winning state now becomes the parent
            action.meta.parentStateName = action.type
            // call the routing agin with next states holding the children
            // pass the current list here
            const nestedResult = breathFirstTraversal(  temporaryState,
                                                        action,
                                                        childrenStates,
                                                        levelId + 1,
                                                        stateChartHistory)
            // update the state hierarchy history here using nestedResult[2]
            let keys = Object.keys(stateChartHistory)
            let lastKey = keys[keys.length - 1]
            stateChartHistory = {   ...stateChartHistory,
                                    [lastKey] : {
                                       ...stateChartHistory[lastKey],
                                        submachine: nestedResult[2]}}

            passes = nestedResult[1]
            if(!passes) {
                return null
            }

            temporaryState = nestedResult[0]

        })
        // 3 parameter return as opposed to [stateChart, didPass] the reducers return
        // current state is an end state
        if(nextStates.length === 0) {
            // return whatever value we have in passes and the stateChartHistory build up so far from top to bottom back to top
            return [temporaryState, passes, stateChartHistory]
        }
        // current state is not an end state

        else if(passes) {
            // console.log("we have a winner", winningStateName, winningFunctionName)

            currentStateName = winningStateName
            
            const currentStateObject = getCell(temporaryState, currentStateName)
            // putting this in would force all states to have it as an attribute even if they have no edges
            if(!Object.keys(currentStateObject).includes('nextStates')) {
                // console.log('The next states doesn\'t exist')
                // printTreeInteractive(temporaryState)

                return [temporaryState, true, stateChartHistory]
            }
            if(currentStateObject.nextStates.length === 0) {
                // console.log(`machine is done 1 ${levelId}`)
                // keepGoing = false
                return [temporaryState, true, stateChartHistory]
            }
            nextStates = currentStateObject.nextStates

            // console.log("next set of edges", nextStates)
        }
        else {
            // What is the difference between a purposefull failure and unpurposefull failure?
            let keys = Object.keys(stateChartHistory)
            let lastKey = keys[keys.length - 1]
            stateChartHistory = {   ...stateChartHistory,
                                    [lastKey] : {
                                       ...stateChartHistory[lastKey],
                                        nextStates: stateFunctionPair}}
            if(isDebug) {
                console.log('failed', {stateChartHistory})

            }

            return [temporaryState, false, stateChartHistory]
        }
    }
}
