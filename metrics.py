#!/usr/bin/env python

import sys
import os
import pandas as pd
from msct_image import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams.update({'font.size': 18})
cmap = plt.get_cmap('Set2')

def total_volume_cord(path_subject, subject_id, section_folder_name_lst, output_fname):
    if os.path.isfile(output_fname):
        tvc_pd = pd.read_csv(output_fname)[['subject_id', 'total_volume_cord']]
    else:
        tvc_pd = pd.DataFrame.from_dict({'subject_id': [], 'total_volume_cord': []})

    tvc = 0.
    for section_folder_name in section_folder_name_lst:
        volume_pkl = os.path.join(path_subject, section_folder_name, 'metrics', 'csa_volume.pickle')
        tvc += pd.read_pickle(volume_pkl)['MEAN across slices']

    idx_pd = len(tvc_pd.index) if subject_id not in tvc_pd['subject_id'].values else tvc_pd[tvc_pd['subject_id'] == subject_id].index[0]
    tvc_pd.loc[idx_pd, 'subject_id'] = subject_id
    tvc_pd.loc[idx_pd, 'total_volume_cord'] = tvc

    tvc_pd.to_csv(output_fname)

def csa_profile(path_subject, subject_id, vert_info_dct, output_prefixe):
    csa_out_pd = pd.DataFrame.from_dict({'vert_level': [], 'csa': [], 'z_slice': [], 'section': []})

    for section in vert_info_dct:
        section_folder_name = vert_info_dct[section]['folder_name']
        im_folder = os.path.join(path_subject, section_folder_name)
        seg_suffixe = '_seg_labeled.nii.gz' if os.path.isfile(os.path.join(im_folder, section_folder_name + '_seg_labeled.nii.gz')) else '_seg_manual_labeled.nii.gz'
        labeled_seg_filename = os.path.join(im_folder, section_folder_name + seg_suffixe)
        labeled_seg_data = Image(labeled_seg_filename).data

        csa_pkl = os.path.join(im_folder, 'metrics', 'csa_per_slice.pickle')
        csa_section_pd = pd.read_pickle(csa_pkl)[['CSA (mm^2)', 'Slice (z)']]

        for vert_label in vert_info_dct[section]['vert_label']:
            idx_vert_section = vert_label - min(vert_info_dct[section]['vert_label']) + 1
            z_vert_lst = sorted(list(set(np.where(labeled_seg_data == vert_label)[1])))
            csa_vert_lst = csa_section_pd[csa_section_pd['Slice (z)'].isin(z_vert_lst)]['CSA (mm^2)'].values
            vert_name_lst = [vert_info_dct[section]['vert_section_initial'] + str(idx_vert_section) for vv in range(len(csa_vert_lst))]
            csa_vert_pd = pd.DataFrame.from_dict({'vert_level': vert_name_lst, 'csa': csa_vert_lst, 'z_slice': z_vert_lst, 'section': [section for vv in range(len(csa_vert_lst))]})
            csa_out_pd = pd.concat([csa_out_pd, csa_vert_pd])

    csa_out_pd = pd.concat([csa_out_pd[csa_out_pd['section'] == 'cervical'], csa_out_pd[csa_out_pd['section'] == 'thoracic'], csa_out_pd[csa_out_pd['section'] == 'lumbar']])
    csa_out_pd['superior_to_inferior_idx'] = range(len(csa_out_pd.index))
    vert_name_ordered = [vert_info_dct[section]['vert_section_initial'] + str(v) for section in ['cervical', 'thoracic', 'lumbar'] for v in range(1, len(vert_info_dct[section]['vert_label'])+1)]
    colors = cmap(np.linspace(0, 1, len(vert_name_ordered)))

    plt.figure(figsize=(16, 6))
    for i, (name, color) in enumerate(zip(vert_name_ordered, colors), 1):
        csa_out_ver_pd = csa_out_pd[csa_out_pd['vert_level'] == name]
        plt.scatter(csa_out_ver_pd['superior_to_inferior_idx'].values,
                    csa_out_ver_pd['csa'].values,
                    edgecolors='none', s=15,
                    label=name, c=color)

    plt.xlim([0, len(csa_out_pd.index)])
    plt.ylim([0, 100])
    plt.xlabel('slice along the Superior-to-Inferior axis')
    plt.ylabel('CSA (mm^2)')
    plt.title('CSA along the Superior-to-Inferior axis - Subject: ' + subject_id)
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.15), ncol=12, fontsize=12)
    plt.savefig(output_prefixe + '.png', bbox_inches="tight")

    csa_out_pd.to_csv(output_prefixe + '.csv')


def run_main(path_data_folder, subject_id, path_results_folder):
    path_subject_folder = os.path.join(path_data_folder, subject_id)

    cord_section_dct = {
                        'cervical': {'folder_name': 't2_sag_cerv', 'vert_label': range(1,8), 'vert_section_initial': 'C'},
                        'thoracic': {'folder_name': 't2_sag_thor', 'vert_label': range(8,20), 'vert_section_initial': 'T'},
                        'lumbar': {'folder_name': 't2_sag_lumb', 'vert_label': range(20,25), 'vert_section_initial': 'L'}
                        }

    total_volume_cord_csv_filename = os.path.join(path_results_folder, 'total_volume_cord.csv')
    total_volume_cord(path_subject=path_subject_folder,
                      subject_id=subject_id,
                      section_folder_name_lst=[cord_section_dct[section]['folder_name'] for section in cord_section_dct],
                      output_fname=total_volume_cord_csv_filename
                        )

    csa_profile_suffixe = path_results_folder + subject_id.split('/')[0] + 'csa_profile'
    csa_profile(path_subject=path_subject_folder,
                subject_id=subject_id,
                vert_info_dct=cord_section_dct,
                output_prefixe=csa_profile_suffixe)


if __name__ == '__main__':
    path_data, subject, path_results = sys.argv[1:]
    run_main(path_data, subject, path_results)