import numpy as np
from numpy import random
from matplotlib import pyplot as plt
import pandas as pd

from hjelpefunksjoner import *

### Denne fila inneholder følgende:

# En funksjon (modeller_last) som utfører lastmodelleringen basert på Tønne sin algoritme.


def modeller_last(last, startdag, år, alt, fordeling_avvik="felles", plot=True):
    """ Funksjon for modellering av last 
    Steg 1: Temperaturkorriger last 
    Steg 2: Fremkall variasjonskurver 
    Steg 3: Beregn profil for estimert maks-effekt
    Steg 4: Beregn relativt avvik 
    Steg 5: Modeller last ut fra estimert maks og relativt avvik
    Steg 6: Evauler stokatisk modell 
    Args: 
        last [numpy array, 8760 verdier]: målt/faktisk forbruk, effektserie med timesoppløsning 
        startdag [int]: indikerer startdag 
        år [int]: indikerer antall år lasten går over
        alt: Alternativ for variasjonskurver, A 3, B 24
        fordeling_avvik: fordeling av avvik, felles eller individuell 
        plot (default: True): sannhetsvariabel for plot
    Return: 
        mod_last: modellert last
    """

    ############
    ## Steg 1 ##
    ############

    ### Temperaturkorriger last

    gammel_last = last
    last = temp_korriger_last(last, år, plot_bool=plot)
    print("Målt maks-effekt etter temperaturkorrigering er", max(last), "kW.")

    if plot:
        # plot last før og etter temperatur-korrigering
        plot_temp_last(gammel_last, last)

    ############
    ## Steg 2 ##
    ############

    ### Generer variasjonskurver for måned, hverdag, helg

    # Fremkall variasjonskurver

    if alt == "A":
        max_mnd = find_monthly_max(last, år)
        ukedag_var = finn_var(last, startdag)
        helg_var = finn_var(last, startdag, ukedag=False)

        # Normaliser variasjonskurvene
        max_P = max(last)
        max_mnd = max_mnd / max_P
        ukedag_var = ukedag_var / max_P
        helg_var = helg_var / max_P

        if plot:
            # plot variasjonskurver
            plot_mnd_var_kurve(max_mnd)
            plot_dag_var_kurve(ukedag_var, helg_var)

    elif alt == "B":  # Alternativ B
        max_P = max(last)
        var_kurver_hverdag = finn_var_alt_B(last, startdag, år)
        var_kurver_helg = finn_var_alt_B(last, startdag, år, ukedag=False)

        # Normaliser variasjonskurvene
        var_kurver_hverdag = var_kurver_hverdag / max_P
        var_kurver_helg = var_kurver_helg / max_P

        if plot:
            # plot variasjonskurver
            plot_var_kurve_alt_B(var_kurver_hverdag)
            plot_var_kurve_alt_B(var_kurver_helg, ukedag=False)

    else:
        print("Ingen alternativ for beregning av variasjonskurver valgt.")

    ############
    ## Steg 3 ##
    ############

    ### Beregn estimert maks

    if alt == "A":
        est_maks = estimer_maks_profil(
            max_mnd, ukedag_var, helg_var, max_P, år, startdag
        )
        if plot:
            # Plot en uke med estimert maks
            plot_estimert_maks(est_maks, startdag)
    elif alt == "B":
        est_maks = estimer_maks_profil_alt_B(
            var_kurver_hverdag, var_kurver_helg, max_P, år, startdag
        )
        if plot:
            plot_est_maks_alt_B(var_kurver_hverdag, var_kurver_helg, startdag)
    else:
        print("Ingen alternativ for beregning av variasjonskurver valgt.")

    ############
    ## Steg 4 ##
    ############

    ### Beregn relativt avvik ("avvik")

    last = np.array(last)
    est_maks = np.array(est_maks)
    if fordeling_avvik == "felles":
        avvik = (last - est_maks) / est_maks  # relativt avvik
    elif fordeling_avvik == "individuell":
        avvik = fordel_avvik(last, est_maks)

    if plot:
        # Plot målt (temp-korrigert), estimert maks og relativt avvik
        plot_pre_mod(last, est_maks, avvik, år)

        # plot relativt avvik som serie
        plot_rel_avvik(avvik)

        # plot relativt avvik som histogram
        if fordeling_avvik == "felles":
            plot_rel_avvik_hist(avvik, startdag)
        elif fordeling_avvik == "individuell":
            print("ikke implementert")

    # (valgfri) Finn sannsynlighetsfordeling for relative avvik

    ############
    ## Steg 5 ##
    ############

    ### Modeller last

    mod_last = np.zeros(shape=(8760 * år,))
    for t in range(len(mod_last)):
        if fordeling_avvik == "felles":
            random_number = np.random.choice(avvik)
        elif fordeling_avvik == "individuell":
            time_nr = int(t % 24)
            random_number = np.random.choice(avvik[time_nr])
        mod_last[t] = est_maks[t] * (1 + random_number)

    ############
    ## Steg 6 ##
    ############

    ### Evaluer modell

    # Avvik mellom modellert last og faktisk last

    eva_arr = (mod_last - last) / est_maks

    if plot:
        # plot modellert last for en gitt tid
        plot_post_mod(last, mod_last, tid=len(mod_last))
        plot_post_mod(last, mod_last, tid=744)

        # plot evaluering av modell
        plot_mod_evaluering(eva_arr)

    return max(mod_last), sum(abs(eva_arr))