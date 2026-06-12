"""lion_step.py -- compact Lion optimizer step.

Faithful to the scalar core of the Lion optimizer: exponential momentum,
sign update, and decoupled weight decay. Fixed-size arrays keep the demoniC
translation close without classes or dynamic containers.
"""


def sign(x):
    if x < 0.0:
        return -1.0
    if x > 0.0:
        return 1.0
    return 0.0


def lion_step(w, m, g, lr=0.03, beta1=0.9, beta2=0.99, weight_decay=0.02):
    for i in range(len(w)):
        w[i] -= lr * weight_decay * w[i]
        update = beta1 * m[i] + (1.0 - beta1) * g[i]
        w[i] -= lr * sign(update)
        m[i] = beta2 * m[i] + (1.0 - beta2) * g[i]


def main():
    w = [0.80, -0.40, 1.25, -1.75]
    m = [0.0, 0.0, 0.0, 0.0]
    grads = [
        [0.30, -0.10, 0.00, 0.20],
        [0.25, -0.15, -0.05, 0.10],
        [-0.10, -0.20, -0.08, 0.05],
    ]

    for step, g in enumerate(grads, 1):
        lion_step(w, m, g)
        print("step %d" % step)
        print("  w=" + " ".join("%.6f" % x for x in w))
        print("  m=" + " ".join("%.6f" % x for x in m))


if __name__ == "__main__":
    main()
