from varasto import Varasto


def main():
    mehua = Varasto(100.0)
    olutta = Varasto(100.0, 20.2)

    print(f"Luonnin jälkeen: \n Mehuvarasto: {mehua} \n Olutvarasto: {olutta}")

    print(f"Olut getterit: \n saldo = {olutta.saldo}")
    print(f"saldo = {olutta.saldo}")
    print(f"tilavuus = {olutta.tilavuus}")
    print(f"paljonko_mahtuu = {olutta.paljonko_mahtuu()}")

if __name__ == "__main__":
    main()
