# Um exemplo complexo envolvendo múltiplas variáveis e estruturas de dados
zaz_core = 100
zaz_scale = 15
zaz_multiplier = [1, 2, 3, 5, 8]
zaz_results = []

for index, multiplier in enumerate(zaz_multiplier):
    if multiplier % 2 == 0:
        zaz_calc = (zaz_core + (zaz_scale * multiplier)) / 2.0
    else:
        zaz_calc = (zaz_core + (zaz_scale / multiplier))
    zaz_results.append(zaz_calc)
    print(f"Result for zaz_multiplier[{index}] ({multiplier}): {zaz_results[-1]}")

print("\nFinal zaz analysis:")
if all(res > zaz_core for res in zaz_results):
    print("All calculated zaz results are greater than the zaz_core.")
else:
    print(f"The analysis found results both above and below the zaz_core of {zaz_core}.")
