import numpy

data = numpy.loadtxt(
    'car.txt',
    str,
    delimiter=' '
)
most_common = numpy.empty(
    (data.shape[1],),
    data.dtype
)

for attribute in range(data.shape[1]):
    column = numpy.unique(
        data[:, attribute],
        return_counts=True)
    column = tuple(sorted(zip(
        column[0],
        column[1]),
        key=lambda item: item[1],
        reverse=True))
    most_common[attribute] = column[0][0]
    print(f'attribute {attribute}: '
          f'{", ".join([name for name, occurrences in column])}')

size = round(data.size * 1.1)
size += data.shape[1] - size % data.shape[1]
extended = numpy.empty(
    (size,),
    data.dtype
)

index = 0

for row in range(data.shape[0]):
    for column in range(data.shape[1]):
        extended[index] = data[row][column]
        index += 1

for index in range(data.size, extended.size):
    extended[index] = '?'

extended = extended.reshape((-1, 7))

for attribute in range(extended.shape[1]):
    extended[data.shape[0]:, attribute] = \
        most_common[attribute]
