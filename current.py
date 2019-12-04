import csv
import pprint

from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean

micro_files = [
    [
        '1kt0.csv',
        '1kt1.csv'
    ],
    [
        '2kt0.csv',
        '2kt1.csv'
    ],
    [
        '3kt0.csv',
        '3kt1.csv'
    ],
    [
        '4kt0.csv',
        '4kt1.csv'
    ],
    [
        '5kt0.csv',
        '5kt1.csv'
    ],
    [
        '6kt0.csv',
        '6kt1.csv'
    ],
    [
        '7kt0.csv',
        '7kt1.csv'
    ],
    [
        '8kt0.csv',
        '8kt1.csv'
    ],
    [
        '9kt0.csv',
        '9kt1.csv'
    ],
    [
        '10kt0.csv',
        '10kt1.csv'
    ],
    [
        '11kt0.csv',
        '11kt1.csv'
    ],
    [
        '12kt0.csv',
        '12kt1.csv'
    ],
    [
        '13kt0.csv',
        '13kt1.csv'
    ],
    [
        '14kt0.csv',
        '14kt1.csv'
    ],
    [
        '15kt0.csv',
        '15kt1.csv'
    ],
    [
        '16kt0.csv',
        '16kt1.csv'
    ],
    [
        '17kt0.csv',
        '17kt1.csv'
    ],
    [
        '18kt0.csv',
        '18kt1.csv'
    ],
    [
        '19kt0.csv',
        '19kt1.csv'
    ],
    [
        '20kt0.csv',
        '20kt1.csv'
    ],
    [
        '21kt0.csv',
        '21kt1.csv'
    ],
    [
        '22kt0.csv',
        '22kt1.csv'
    ],
    [
        '23kt0.csv',
        '23kt1.csv'
    ],
    [
        '24kt0.csv',
        '24kt1.csv'
    ],
    [
        '25kt0.csv',
        '25kt1.csv'
    ],
    [
        '26kt0.csv',
        '26kt1.csv'
    ],
    [
        '27kt0.csv',
        '27kt1.csv'
    ],
    [
        '28kt0.csv',
        '28kt1.csv'
    ],
    [
        '29kt0.csv',
        '29kt1.csv'
    ],
    [
        '30kt0.csv',
        '30kt1.csv'
    ]
]

flag_particle = {
    'e-': '1',
    'proton': '2',
    'GenericIon': '3'}

flag_process = {
    'msc': '10',
    'e-_G4MicroElecElastic': '11',
    'e-_G4MicroElecInelastic': '12',
    'eCapture': '13',
    'p_G4MicroElecInelastic': '14',
    'ion_G4MicroElecInelastic': '15',
    'hIoni': '16',
    'eIoni': '17'}

particle_col = 0
process_col = 1
x_col = 2
y_col = 3
z_col = 4
total_energy_col = 5
step_length_col = 6
kinetic_energy_col = 7

particle_count = {
    'electron': 0,
    'proton': 0,
    'ion': 0
}

process_count = {
    'msc': 0,
    'e_elastic': 0,
    'e_inelastic': 0,
    'e_capture': 0,
    'p_inelastic': 0,
    'ion_inelastic': 0,
    'h_ionisation': 0,
    'e_ionisation': 0,
}

position_of_secondaries = []
energies_over_range = []

count = 0
for micro_file in micro_files:
    # get the average position
    position_of_secondaries.append([])
    energies_over_range.append([])
    for mfile in micro_file:
        with open(mfile) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) > 1:
                    if row[particle_col] == flag_particle['e-'] and row[process_col] == flag_process['eIoni']:
                        position_of_secondaries[count].append(float(row[z_col]))
                        if float(row[z_col]) + 2000 < 500 and float(row[z_col]) + 2000 > 400:
                            eng = float(row[kinetic_energy_col])
                            if eng < 1500:
                                energies_over_range[count].append(eng)
    count += 1

currents = []
ehp_energy = 4.2

for energies in energies_over_range:
    # n, bins, patches = plt.hist(x=energies, bins='auto')
    # plt.show()
    ehp = sum(energies)/ehp_energy
    current = 1000 * 1.6 * 10 ** -19 * ehp
    currents.append(current)

energy_range = range(1,31)
plt.plot(energy_range, currents)
plt.title('Current')
plt.xlabel('Energy (keV)')
plt.ylabel('Current (A)')
plt.show()

# if __name__ == '__main__':
#     main()