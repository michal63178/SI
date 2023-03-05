import numpy

data = numpy.loadtxt(
    'SPECTF-all-modif.txt',
    int
)

# 3
# c), f)

for attribute in range(data.shape[1] - 1):
    column = data[:, attribute]

    if not len(column) & 1:
        maximum = max(column[0], column[1])
        minimum = min(column[0], column[1])
        index = 2

    else:
        maximum = minimum = column[0]
        index = 1

    while index < len(column) - 1:
        if column[index] < column[index + 1]:
            maximum = max(maximum, column[index + 1])
            minimum = min(minimum, column[index])
        else:
            maximum = max(maximum, column[index])
            minimum = min(minimum, column[index + 1])

        index += 2

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
    )
)
