import numpy as np
from sklearn.linear_model import LinearRegression as lr
import matplotlib.pyplot as plt
from celluloid import Camera


class LinearRegression:
    def __init__(self, w=1, b=1, lr=0.01):
        self.lr = lr
        self.w = np.array([[w]])
        self.b = np.array([b])

    def cost(self, x, y):
        pred = x @ self.w + self.b
        e = y - pred
        return np.mean(e ** 2)

    def fit(self, x, y):
        pred = x @ self.w + self.b
        e = y - pred
        dJ_dw = (np.mean(e * (-2 * x), axis=0))
        dJ_db = (np.mean(e * (-2), axis=0))
        self.w = (self.w.T - self.lr * dJ_dw).T
        self.b = self.b - self.lr * dJ_db

    def predict(self, x):
        return (x @ self.w.T + self.b)

    def params(self):
        return (self.w, self.b)


# 1
def get_unemployment(model, year):
    return model.coef_[0][0] * year + model.intercept_[0]


given_year = (
    (2000,),
    (2002,),
    (2005,),
    (2007,),
    (2010,),
)
given_percentage = (
    (6.5,),
    (7.0,),
    (7.4,),
    (8.2,),
    (9.0,),
)
given_model = \
    lr().fit(
        given_year,
        given_percentage
    )

print(
    f'{round(get_unemployment(given_model, 2023), 3)}',
    round(np.ceil(  # 2
        (12 - given_model.intercept_[0])
        / given_model.coef_[0][0])),
    sep='\n'
)
given_model = LinearRegression(w=3, b=-1, lr=0.001)
w_list = []
b_list = []
c_list = []
ys_list = []
cl_list = []
xs = np.array([
    [-3],
    [10]
])

for i in range(60000):  # set number of epochs
    w_list.append(given_model.params()[0])
    b_list.append(given_model.params()[1])
    c_list.append(given_model.cost(given_year, given_percentage))
    ys_list.append(given_model.predict(xs).T)
    cl_list.append(given_model.predict(given_year).T)
    given_model.fit(given_year, given_percentage)

a = np.arange(0, 50, 1).tolist()
b = np.arange(50, 100, 5).tolist()
c = np.arange(100, 12000, 200).tolist()
p = a + b + c

w = np.array(w_list).flatten()
b = np.array(b_list).flatten()
c = np.array(c_list).flatten()
ys = np.array(ys_list)
p = np.array(p)
fig = plt.figure(figsize=(10, 10))
labelsize_ = 14
camera = Camera(fig)

for i in p:
    ax0 = fig.add_subplot(2, 1, 1)
    leg = ax0.plot(xs.T.flatten(), ys[i].flatten(), color='r', label=str(i))
    ax0.scatter(given_year, given_percentage, color='b', marker='x', s=44)
    ax0.vlines(given_year.T, ymin=given_percentage.T, ymax=cl_list[i],
               linestyle="dashed", color='r', alpha=0.3)
    ax0.legend(leg, [f'epochs: {i}'], loc='upper right', fontsize=15)
    ax0.set_title("Linear fit", fontsize=25)
    ax0.tick_params(axis='both', which='major', labelsize=labelsize_)
    ax0.set_xlabel("x", fontsize=25, labelpad=10)
    ax0.set_ylabel("y", fontsize=25, labelpad=10)
    ax0.tick_params(axis='both', which='major', labelsize=labelsize_)
    ax0.set_ylim([-20, 10])

    ax1 = fig.add_subplot(2, 2, 3)
    ax1.plot(w[i], c[i], marker='x', markersize=13, color="orangered")
    ax1.plot(np.array(w_list).flatten(), np.array(c_list).flatten(),
             linestyle='dashed', color="blue")
    ax1.set_xlabel("w", fontsize=25)
    ax1.set_ylabel("costs", fontsize=25, labelpad=10)
    ax1.tick_params(axis='both', which='major', labelsize=labelsize_)

    ax2 = fig.add_subplot(2, 2, 4, sharey=ax1)
    ax2.plot(b[i], c[i], marker='x', markersize=13, color="orangered")
    ax2.plot(np.array(b_list).flatten(), np.array(c_list).flatten(),
             linestyle='dashed', color="red")
    ax2.set_xlabel("b", fontsize=25)
    ax2.tick_params(axis='both', which='major', labelsize=labelsize_)

    plt.tight_layout()
    camera.snap()

animation = camera.animate(interval=5,
                           repeat=False, repeat_delay=500)
animation.save('SimpleLinReg_2.gif', writer='imagemagick')


def cost_3d(x, y, w, b):
    pred = x @ w.T + b
    e = y - pred
    return np.mean(e ** 2)


ws = np.linspace(-5, 5.0, 10)
bs = np.linspace(-5, 5, 10)
M, B = np.meshgrid(ws, bs)

zs = np.array([cost_3d(given_year, given_percentage,
                       np.array([[wp]]), np.array([[bp]]))
               for wp, bp in zip(np.ravel(M), np.ravel(B))])
Z = zs.reshape(M.shape)
