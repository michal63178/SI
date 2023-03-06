import numpy

data = numpy.loadtxt(
    'SPECTF-all-modif.txt',
    int
)
min_max_values = []

# 3
# c), f)

for attribute in range(data.shape[1] - 1):
    column = data[:, attribute]

    if not len(column) & 1:
        maximum = max(
            column[0],
            column[1]
        )
        minimum = min(
            column[0],
            column[1]
        )
        index = 2

    else:
        maximum = minimum = column[0]
        index = 1

    while index < len(column) - 1:
        if column[index] < column[index + 1]:
            maximum = max(
                maximum,
                column[index + 1]
            )
            minimum = min(
                minimum,
                column[index]
            )

        else:
            maximum = max(
                maximum,
                column[index]
            )
            minimum = min(
                minimum,
                column[index + 1]
            )

        index += 2

    min_max_values.append(
        (
            minimum,
            maximum
        )
    )
    standard_deviation = numpy.std(
        column,
        dtype=numpy.float64
    )

    print(
        f'attribute: {attribute + 1}, '
        f'minimum value: {minimum}, '
        f'maximum value: {maximum}, '
        f'standard deviation: {standard_deviation}'
    )

print(
    'decision class '
    'standard deviation:',
    numpy.std(
        data[:, -1],
        dtype=numpy.float64
    ),
    end='\n\n'
)

# 4
# b), c)

print('<−1, 1> <0, 1> <−10, 10>')

for given_object in data:
    for which, value in enumerate((
            (-1, 1),
            (0, 1)
    )):
        print(
            ((given_object[which]
              - min_max_values[which][0])
             * (value[1] - value[0])) /
            (min_max_values[which][1]
             - min_max_values[which][0])
            + value[0],
            end=' '
        )

    for which, given_attribute in enumerate(
            given_object[2:-1],
            2
    ):
        print(
            ((given_attribute
              - min_max_values[which][0]) * 20) /
            (min_max_values[which][1]
             - min_max_values[which][0]) - 10,
            end=' '
        )

    print()
