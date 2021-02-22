import argparse
import numpy as np


parser = argparse.ArgumentParser(
    description="run_simulation -n number_of_samples")
parser.add_argument('-n', '--number', required=True, type=int,
                    help="Number of samples")


def main():
    """Calling the Monte-Carlo method."""
    # read the command line arguments
    args = parser.parse_args()
    samples = args.number
    approx_pi = compute_pi(samples)
    write_results(approx_pi, samples)

    
def compute_pi(samples: int) -> float:
    """Compute the pi number using the Monte-Carlo method.
    Measure  the ratio between points that are inside a circle of radius 1
    and a square of size 1.
    """
    # Take random x and y cartesian coordinates
    xs = np.random.uniform(size=samples)
    ys = np.random.uniform(size=samples)

    # Count the points inside the circle
    rs = np.sqrt(xs**2 + ys**2)
    inside = rs[rs < 1.0]

    # compute pi
    approx_pi = (float(inside.size) / samples) * 4

    return approx_pi


def write_results(result: float, samples: int):
    """Write the results simulation in CSV format."""
    data = f"""result, samples
{result}, {samples}
"""
    with open("result.csv", 'w') as handler:
        handler.write(data)


if __name__ == "__main__":
    main()
