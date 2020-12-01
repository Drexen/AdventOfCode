def solve():
    print("Part one fuel = " + str(sum(partOne())))
    print("Part two fuel = " + str(partTwo()))


def partOne():
    lines = open("day-1-input.txt").readlines()
    fuel_masses = []
    for line in lines:
        fuel_masses.append(fuelEqn(int(line)))

    return fuel_masses


def partTwo():
     fuel_masses = partOne()
     adjusted_fuel = 0
     for fuel in fuel_masses:
         while fuel > 0:
             adjusted_fuel += fuel
             fuel = fuelEqn(fuel)

     return adjusted_fuel


def fuelEqn(fuel):
    return (int((int(fuel) / 3)) - 2)


solve()
