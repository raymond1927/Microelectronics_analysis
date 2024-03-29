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

# store data in these variables
positions = []
energy_deposition_depth = []
step_length_tracks = []
secondaries = []
energies_over_range = []

position_of_secondaries = []

pp = pprint.PrettyPrinter(indent=4)

fig = plt.figure()


def main():
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
                            if float(row[z_col]) + 2000 < 600 and float(row[z_col]) + 2000 > 300:
                                energies_over_range[count].append(float(row[kinetic_energy_col]))
        count += 1
    
    mean_pos = []
    energies = range(1, 31)
    for pos in position_of_secondaries:
        # print(pos)
        if len(pos) > 0:
            mean_pos.append(mean(pos) + 2000)
        else:
            mean_pos.append(0)
    plt.scatter(energies, mean_pos)
    plt.title('Average depth of secondary generation')
    plt.xlabel('Particle beam Energy (keV)')
    plt.ylabel('Depth (nm)')
    plt.show()

    mean_energy = []
    for eng in energies:
        energies_at = energies_over_range[eng-1]
        if len(energies_at) > 0:
            mean_energy.append(sum(energies_at)/(eng*1000*1000))
        else:
            mean_energy.append(0)
    plt.scatter(energies, mean_energy)
    plt.title('Percentage of energy transferred to secondaries within depletion region')
    plt.xlabel('Particle beam energy (keV)')
    plt.ylabel('Percentage of energy transferred')
    plt.show()


    for micro_file in micro_files[20]:
        with open(micro_file) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                # ignore header lines
                if len(row) > 1:
                    count_particle(row)
                    count_process(row)
                    tracking_position(row)
                    track_energy_deposition(row)
                    track_step_length(row)
                    track_secondaries(row)

    print('Summary of simulation')
    print('Particle event count')
    pp.pprint(particle_count)
    print('Process event count')
    pp.pprint(process_count)
    print('Position which events occurred')
    graph_positions(positions)
    print('Energy deposited in depth')
    graph_energy_deposition(energy_deposition_depth)
    print('Step length of electrons')
    graph_step_length(step_length_tracks)
    print('Secondaries')
    graph_secondaries(secondaries)
    # pp.pprint(secondaries)


def count_particle(row):
    if row[particle_col] == flag_particle['e-']:
        particle_count['electron'] += 1
    elif row[particle_col] == flag_particle['proton']:
        particle_count['proton'] += 1
    elif row[particle_col] == flag_particle['GenericIon']:
        particle_count['ion'] += 1


def count_process(row):
    if row[process_col] == flag_process['msc']:
        process_count['msc'] += 1
    elif row[process_col] == flag_process['e-_G4MicroElecElastic']:
        process_count['e_elastic'] += 1
    elif row[process_col] == flag_process['e-_G4MicroElecInelastic']:
        process_count['e_inelastic'] += 1
    elif row[process_col] == flag_process['eCapture']:
        process_count['e_capture'] += 1
    elif row[process_col] == flag_process['p_G4MicroElecInelastic']:
        process_count['p_inelastic'] += 1
    elif row[process_col] == flag_process['ion_G4MicroElecInelastic']:
        process_count['ion_inelastic'] += 1
    elif row[process_col] == flag_process['hIoni']:
        process_count['h_ionisation'] += 1
    elif row[process_col] == flag_process['eIoni']:
        process_count['e_ionisation'] += 1


def tracking_position(row):
    pos = (row[x_col], row[y_col], row[z_col], row[particle_col])
    positions.append(pos)


def graph_positions(positions):
    ax = plt.subplot(221, projection='3d')

    elec_pos = [[], [], []]
    proton_pos = [[], [], []]
    ion_pos = [[], [], []]
    for pos in positions:
        particle_type = pos[3]

        # remove if z is below zero, outside
        # if (float(pos[2]) >= 0):
        if particle_type == flag_particle['e-']:
            elec_pos[0].append(float(pos[0]))
            elec_pos[1].append(float(pos[1]))
            elec_pos[2].append(float(pos[2]))
        elif particle_type == flag_particle['proton']:
            proton_pos[0].append(float(pos[0]))
            proton_pos[1].append(float(pos[1]))
            proton_pos[2].append(float(pos[2]))
        elif particle_type == flag_particle['GenericIon']:
            ion_pos[0].append(float(pos[0]))
            ion_pos[1].append(float(pos[1]))
            ion_pos[2].append(float(pos[2]))

    # graph different particle positions
    ax.scatter(elec_pos[0], elec_pos[1], elec_pos[2], marker='o')
    ax.scatter(proton_pos[0], proton_pos[1], proton_pos[2], marker='^')
    ax.scatter(ion_pos[0], ion_pos[1], ion_pos[2], marker='.')

    ax.set_title('Position of energy interaction')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    plt.show()


def track_energy_deposition(row):
    # only worry about energy deposited from electrons
    if (row[particle_col] == flag_particle['e-']):
        energy_deposition_depth.append(
            (row[z_col], row[total_energy_col], row[kinetic_energy_col]))


def graph_energy_deposition(energy_deposition_depth):
    depth = []
    energy = []

    for depth_energy in energy_deposition_depth:
        depth_pos = float(depth_energy[0])
        if depth_pos > 0:
            depth.append(depth_pos)
            energy.append(float(depth_energy[1]))

    ax2 = plt.subplot(222)

    ax2.scatter(depth, energy)

    ax2.set_title('Energy deposited over depth')
    ax2.set_xlabel('Depth (nm)')
    ax2.set_ylabel('Energy (eV)')


def track_step_length(row):
    # only consider electrons
    # comparison of step length and depth
    # comparison of step length and energy deposition
    if row[particle_col] == flag_particle['e-']:
        step_length_tracks.append(
            (row[z_col], row[step_length_col], row[total_energy_col]))


def graph_step_length(step_length_tracks):
    depths = []
    step_lengths = []
    energy_depositions = []

    for step_length_track in step_length_tracks:
        depth = float(step_length_track[0])

        if depth > 0:
            step_length = float(step_length_track[1])/(1*10**9)
            energy_deposition = float(step_length_track[2])

            depths.append(depth)
            step_lengths.append(step_length)
            energy_depositions.append(energy_deposition)

    ax3 = plt.subplot(223)
    ax3.scatter(depths, step_lengths)
    ax3.set_title('Step length at depth')
    ax3.set_xlabel('Depth (um)')
    ax3.set_ylabel('Step length (nm)')
    plt.show()
    plt.scatter(depths, step_lengths)
    plt.title('Step length throughout depth')
    plt.xlabel('Depth (nm)')
    plt.ylabel('Step length (nm)')
    plt.show()

    ax4 = plt.subplot(224)
    ax4.scatter(step_lengths, energy_depositions)
    ax4.set_title('Energy deposition for different step length')
    ax4.set_xlabel('Step length (nm)')
    ax4.set_ylabel('Energy deposited (eV)')
    plt.show()
    plt.scatter(step_lengths, energy_depositions)
    plt.title('Energy deposition for different step length')
    plt.xlabel('Step length (nm)')
    plt.ylabel('Energy deposited (eV)')
    plt.show()


def track_secondaries(row):
    if row[particle_col] == flag_particle['e-'] and row[process_col] == flag_process['eIoni']:
        secondaries.append(row)


def graph_secondaries(secondaries):
    ax = plt.subplot(211, projection='3d')

    x_pos = []
    y_pos = []
    z_pos = []
    energies = []
    step_length = []
    kin_energies = []
    for secondary in secondaries:
        # remove if z is below zero, outside
        if (float(secondary[z_col]) >= 0 or True):
            energies.append(float(secondary[total_energy_col]))
            x_pos.append(float(secondary[x_col]))
            y_pos.append(float(secondary[y_col]))
            z_pos.append(float(secondary[z_col]))
            step_length.append(float(secondary[step_length_col]))

        kin_energies.append(float(secondary[kinetic_energy_col]))

    print("Average of the list =", mean(kin_energies))

    # graph different particle positions
    ax.scatter(x_pos, y_pos, z_pos, marker='o')

    ax.set_title('Position of energy interaction')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax2 = plt.subplot(212)

    ax2.scatter(z_pos, kin_energies)
    ax2.set_title('Energy transferred to secondaries')
    ax2.set_ylabel('Kinetic energy transferred (eV)')
    ax2.set_xlabel('Depth (nm)')

    plt.show()

    ax = plt.subplot(111)

    ax.set_title('Step length throughout depth')
    ax.set_xlabel('Depth (nm)')
    ax.set_ylabel('Step length (nm)')
    ax.scatter(z_pos, step_length)

    plt.show()


if __name__ == '__main__':
    main()
    plt.show()
