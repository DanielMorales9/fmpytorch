import numpy as np
from divmachines.topk.mmr import MF_MMR
from divmachines.logging import TrainingLogger as TLogger
from divmachines.utility.helper import cartesian

interactions = np.array([[100, 10, 0, 1, 5],
                         [200, 10, 0, 1, 1],
                         [100, 20, 1, 1, 2],
                         [200, 20, 1, 1, 4],
                         [100, 30, 1, 0, 3],
                         [200, 30, 1, 0, 2],
                         [100, 40, 1, 1, 4],
                         [200, 40, 1, 1, 4]])

n_users = 2
n_items = 4
train = np.zeros((n_users*n_items, 3), dtype=np.int)
train[:, :2] = interactions[:, :2]
train[:, -1] = interactions[:, -1]

logger = TLogger()

model = MF_MMR(n_iter=100,
               n_jobs=2,
               n_factors=4,
               learning_rate=.3,
               logger=logger)


print("Number of users: %s" % n_users)
print("Number of items: %s" % n_items)

x = train[:, :-1]
y = train[:, -1]

model.fit(x, y, n_users=n_users, n_items=n_items)

# plt.plot(logger.epochs, logger.losses)
# plt.show()
users = np.array(np.unique(x[:, 0]))
values = cartesian(users, np.unique(x[:, 1]))
top = 3
table = np.zeros((users.shape[0], top+1), dtype=np.int)
table[:, 0] = users
table[:, 1:] = model.predict(values, top=top, b=0.5)
print(table)
