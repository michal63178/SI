import numpy

data = numpy.loadtxt(
    'car.txt',
    str,
    delimiter=' '
)
most_common = numpy.empty(
    (data.shape[1],),
    str
)

for attribute in range(1, data.shape[1]):
    column = numpy.unique(
        data[:, attribute],
        return_counts=True)
    column = tuple(sorted(zip(
        column[0],
        column[1]),
        key=lambda item: item[1],
        reverse=True))
    most_common[attribute - 1] = column[0][0]
    print(f'attribute {attribute}: '
          f'{", ".join(column[0])}')

extended = numpy.empty(
    round(data.size * 1.1),
    str
)

for index in range(data.size):

