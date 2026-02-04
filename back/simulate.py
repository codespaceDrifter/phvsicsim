"""
Master simulation script - runs all example world simulations.
"""
from example_worlds import simulate_three_body, simulate_billard_ball


def main():
    print("=== Running Three Body Simulation ===")
    simulate_three_body()

    print("\n=== Running Billard Ball Simulation ===")
    simulate_billard_ball()

    print("\n=== All simulations complete ===")


if __name__ == '__main__':
    main()
