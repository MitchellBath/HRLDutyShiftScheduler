import csv

people = []
while True:
    name = input("Enter a CSV preference file name (ex. MitchBath) or 'quit' to end: ")
    if name.lower() == "quit":
        break

    name = name + ".csv"
    dates = []
    prefs = []
    with open(name, mode='r') as file:
        csvFile = csv.reader(file)
        next(csvFile)  # Skip header row
        for row in csvFile:
            dates.append(row[0])
            prefs.append(float(row[2]))  # Convert preference to float for proper comparison
            print(row[0] + " " + row[2])

    people.append([name, dates, prefs])
    print("Got it!")

if len(people) == 0:
    print("No people found! Goodbye")
else:
    masterdates = people[0][1]
    if len(masterdates) % 2 != 0:
        input("Dates are not even! Expect errors")
    assignments = [""] * len(masterdates)

    # Define shift pairs
    shift_pairs = [(i, i+1) for i in range(0, len(masterdates), 2)]  # Adjust based on the number of shifts

    print("Shift pairs:")
    print(shift_pairs)

    print("Performing assignments...")

    while "" in assignments:
        print(assignments)
        slot_filled = False  # Flag to check if any assignment occurred in this iteration
        for person in people:
            if "" not in assignments:
                break
            maxpref = -1  # Initialize maxpref to a value lower than any preference
            maxindex = -1

            for i in range(len(masterdates)):
                if i % 2 == 0:
                    thispair = i + 1
                else:
                    thispair = i - 1

                # compare everyone's preferences in the case of ties
                if assignments[i] == "" and assignments[thispair] != person[0]:
                    totalpreference = sum(p[2][i] for p in people)
                    oldtotalpreference = sum(p[2][maxindex] for p in people) if maxindex > -1 else 0

                    if person[2][i] == maxpref and totalpreference < oldtotalpreference:
                        maxpref = person[2][i]
                        maxindex = i

                    # if a higher preference, change pick for this round
                    elif person[2][i] > maxpref:
                        maxpref = person[2][i]
                        maxindex = i

            if maxindex != -1:  # If a valid slot was found for assignment
                assignments[maxindex] = person[0]
                slot_filled = True

        if not slot_filled:  # If no slots were filled in this iteration, break the loop
            break

    # Balancing shifts (same as before)
    shifts_per_person = len(masterdates) // len(people)
    remainder = len(masterdates) % len(people)

    for i in range(len(people)):
        start_index = i * shifts_per_person + min(i, remainder)
        end_index = (i + 1) * shifts_per_person + min(i + 1, remainder)

        assigned_count = assignments.count(people[i][0])
        additional_shifts = shifts_per_person + (1 if assigned_count < shifts_per_person else 0)

        for j in range(start_index, end_index):
            if assigned_count < additional_shifts and assignments[j] == "":
                assignments[j] = people[i][0]
                assigned_count += 1

    # Writing to CSV
    with open('final_schedule.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Date', 'Assignment'])
        for date, assignment in zip(masterdates, assignments):
            writer.writerow([date, assignment])

    input("All done! Check the final schedule")
