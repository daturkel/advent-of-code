Another unusually hard problem for this early in the month. I go line by line, using
regex again to find the multi-digit numbers. A helper function checks every spot "around"
a number to see if it's a special char. If it is, this is a valid number and we increment the "parts total."

For part two, I keep track of asterisks that touch a number and build up a dictionary of asterisk location
to parts touching it. For any asterisk touching two parts, we add their product to the gear ratio total.