#!/usr/bin/env python
#
# This script extracts the computed metrics along the entire spinal cord.
#
# Charley Gros 2018-05-17

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
    """
    Compute the volume of the entire spinal cord.
    :param path_subject: with a '/' at the end
    :param subject_id: subject folder name
    :param section_folder_name_lst: list of the image folders (e.g. ['t2_cerv', 't2_thor', 't2_lumb'])
    """
    # check if output_fname file already exist
    if os.path.isfile(output_fname):
        tvc_pd = pd.read_csv(output_fname)[['subject_id', 'total_volume_cord']]
    else:
        tvc_pd = pd.DataFrame.from_dict({'subject_id': [], 'total_volume_cord': []})

    # loop across the cord sections
    tvc = 0.
    for section_folder_name in section_folder_name_lst:
        volume_pkl = os.path.join(path_subject, section_folder_name, 'metrics', 'csa_volume.pickle')
        tvc += pd.read_pickle(volume_pkl)['MEAN across slices']
    cvc = pd.read_pickle(os.path.join(path_subject, section_folder_name_lst[0], 'metrics', 'csa_volume.pickle'))['MEAN across slices']

    # if the subject already in the output_fname file, the value is updated, otherwise the new subject is appended
    print subject_id, tvc_pd[tvc_pd['subject_id'] == subject_id].index[0]
    idx_pd = len(tvc_pd.index) if subject_id not in tvc_pd['subject_id'].values else tvc_pd[tvc_pd['subject_id'] == subject_id].index[0]
    tvc_pd.loc[idx_pd, 'subject_id'] = subject_id
    tvc_pd.loc[idx_pd, 'total_volume_cord'] = tvc
    tvc_pd.loc[idx_pd, 'cervical_volume_cord'] = cvc
    tvc_pd.to_csv(output_fname)


def extract_info_from_metric_file(csa_shape, path_folder, metric_name=None, file_prefixe=None):
    """
    Open the appropriated file (from sct_process_segmentation).
    :param csa_shape: 'csa' or 'shape'
    :param path_folder: with a '/' at the end
    :param metric_name: one of the column name of the file *_shape.csv output by sct_process_segmentation (needed of csa_shape=='shape')
    :param file_prefixe: prefixe of the file *_shape.csv output by sct_process_segmentation (needed of csa_shape=='shape')
    :return : pandasdataframe
    """
    if csa_shape == 'csa':
        csa_pkl = path_folder + 'csa_per_slice.pickle'
        csa_section_pd = pd.read_pickle(csa_pkl)[['CSA (mm^2)', 'Slice (z)']]
        return csa_section_pd.rename(columns={'CSA (mm^2)': 'raw_metric', 'Slice (z)': 'raw_z'})
    elif csa_shape == 'shape':
        shape_csv = path_folder + file_prefixe + '_shape.csv'
        shape_section_pd = pd.read_csv(shape_csv)[['Unnamed: 0', metric_name]]
        return shape_section_pd.rename(columns={metric_name: 'raw_metric', 'Unnamed: 0': 'raw_z'})


def metric_profile(path_subject, subject_id, vert_info_dct, section_lst, output_fname, metric_name, y_lim_lst):
    """
    Compute the Superior-to-Inferior profile of a metric, and plot it per vertebral level.
    :param path_subject: with a '/' at the end
    :param subject_id: subject folder name
    :param vert_info_dct:
    :param section_lst: list of cord section sorted in the superiror to inferior axis
    :param output_fname: filename of the saved profile plot
    :param metric_name:
    :param y_lim_lst: extrem values of the plot along the y axis
    :return : pandas dataframe
    """
    metric_out_pd = pd.DataFrame.from_dict({'vert_level': [], metric_name: [], 'z_slice_raw_im': [], 'cord_section': []})

    # loop over the different cord sections (e.g. cerv, thor, lumb)
    for section in section_lst:
        section_folder_name = vert_info_dct[section]['folder_name']
        im_folder = os.path.join(path_subject, section_folder_name)

        # Use the labeled segmentation file to match a z_slice_idx with a vertebral level value
        seg_suffixe = '_seg_labeled.nii.gz' if os.path.isfile(os.path.join(im_folder, section_folder_name + '_seg_labeled.nii.gz')) else '_seg_manual_labeled.nii.gz'
        labeled_seg_filename = os.path.join(im_folder, section_folder_name + seg_suffixe)
        labeled_seg_data = Image(labeled_seg_filename).data

        # extract values from file output by sct_process_segmentation
        raw_csv_pd = extract_info_from_metric_file(csa_shape='csa' if metric_name == 'csa' else 'shape',
                                                path_folder=os.path.join(im_folder, 'metrics', ''),
                                                metric_name=metric_name,
                                                file_prefixe=section_folder_name + seg_suffixe.split('_labeled')[0])

        # loop over the vertebral levels in the current cord section
        for vert_label in vert_info_dct[section]['vert_label']:
            idx_vert_section = vert_label - min(vert_info_dct[section]['vert_label']) + 1
            z_vert_lst = sorted(list(set(np.where(labeled_seg_data == vert_label)[1])))[::-1]
            metric_slice_pd = raw_csv_pd[raw_csv_pd['raw_z'].isin(z_vert_lst)][['raw_metric', 'raw_z']]
            vert_name_lst = [vert_info_dct[section]['vert_section_initial'] + str(idx_vert_section) for vv in range(len(z_vert_lst))]
            metric_vert_pd = pd.DataFrame.from_dict({'vert_level': vert_name_lst,
                                                    metric_name: metric_slice_pd['raw_metric'].values,
                                                    'z_slice_raw_im': metric_slice_pd['raw_z'].values,
                                                    'cord_section': [section for vv in range(len(z_vert_lst))]})
            metric_vert_pd = metric_vert_pd.sort_values(by=['z_slice_raw_im'], ascending=False)
            metric_out_pd = pd.concat([metric_out_pd, metric_vert_pd])

    # plot the profile along the superior to inferior axis
    metric_out_pd['superior_to_inferior_idx'] = range(len(metric_out_pd.index))
    vert_name_ordered = [vert_info_dct[section]['vert_section_initial'] + str(v) for section in ['cervical', 'thoracic', 'lumbar'] for v in range(1, len(vert_info_dct[section]['vert_label'])+1)]
    colors = cmap(np.linspace(0, 1, len(vert_name_ordered)))
    plt.figure(figsize=(16, 6))
    for i, (name, color) in enumerate(zip(vert_name_ordered, colors), 1):
        metric_out_ver_pd = metric_out_pd[metric_out_pd['vert_level'] == name]
        plt.scatter(metric_out_ver_pd['superior_to_inferior_idx'].values,
                    metric_out_ver_pd[metric_name].values,
                    edgecolors='none', s=15,
                    label=name, c=color)
    plt.xlim([0, len(metric_out_pd.index)])
    plt.ylim(y_lim_lst)
    plt.grid()
    plt.xlabel('slice along the Superior-to-Inferior axis')
    plt.ylabel(metric_name)
    plt.title(metric_name + ' along the Superior-to-Inferior axis - Subject: ' + subject_id)
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.15), ncol=12, fontsize=12)
    plt.savefig(output_fname, bbox_inches="tight")

    return metric_out_pd[['cord_section', 'vert_level', 'z_slice_raw_im', 'superior_to_inferior_idx', metric_name]]


def run_main(path_data_folder, subject_id, path_results_folder):
    path_subject_folder = os.path.join(path_data_folder, subject_id)

    cord_section_dct = {'cervical': {'folder_name': 't2_sag_cerv', 'vert_label': range(1,8), 'vert_section_initial': 'C'},
                        'thoracic': {'folder_name': 't2_sag_thor', 'vert_label': range(8,20), 'vert_section_initial': 'T'},
                        'lumbar': {'folder_name': 't2_sag_lumb', 'vert_label': range(20,25), 'vert_section_initial': 'L'}}
    cord_section_sorted_lst = ['cervical', 'thoracic', 'lumbar'] # sorted from superior to inferior

    total_volume_cord_csv_filename = os.path.join(path_results_folder, '_total_volume_cord.csv')
    total_volume_cord(path_subject=path_subject_folder,
                      subject_id=subject_id.split('/')[0],
                      section_folder_name_lst=[cord_section_dct[section]['folder_name'] for section in cord_section_sorted_lst],
                      output_fname=total_volume_cord_csv_filename)

    # path_subject_result_folder = path_results_folder + subject_id
    # if not os.path.isdir(path_subject_result_folder):
    #     os.makedirs(path_subject_result_folder)

    # metric_dct = {'csa': [0, 100], 'RL_diameter': [0, 30], 'AP_diameter': [0, 20], 'ratio_minor_major': [0, 1]}
    # shape_pd = pd.DataFrame.from_dict({})
    # for metric in metric_dct:
    #     profile_filename = path_subject_result_folder + metric + '_profile.png'
    #     profile_pd = metric_profile(path_subject=path_subject_folder,
    #                                     subject_id=subject_id,
    #                                     vert_info_dct=cord_section_dct,
    #                                     section_lst=cord_section_sorted_lst,
    #                                     output_fname=profile_filename,
    #                                     metric_name=metric,
    #                                     y_lim_lst=metric_dct[metric])
    #     if shape_pd.empty:
    #         shape_pd = profile_pd
    #     else:
    #         shape_pd = pd.concat([shape_pd, profile_pd[metric]], axis=1)

    # shape_csv_filename = path_subject_result_folder + '_shape.csv'
    # shape_pd.to_csv(shape_csv_filename)


if __name__ == '__main__':
    path_data, subject, path_results = sys.argv[1:]
    run_main(path_data, subject, path_results)
