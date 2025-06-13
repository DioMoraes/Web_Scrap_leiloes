import sys,os
import time

PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir
    )
)
sys.path.append(PROJECT_ROOT)

from src.Runner import run
def main():
    print('-'*100)
    print("\nINICIANDO CAPTURA DE DADOS\n")
    print('-'*100)

    run()

    print('-'*100)
    print("\nCAPTURA DE DADOS FINALIZADA\n")
    print('-'*100)
    time.sleep(15)
    
if __name__ == "__main__":
    main()