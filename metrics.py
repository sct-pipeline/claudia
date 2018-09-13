#!/usr/bin/env python
#
# This script extracts the computed metrics along the entire spinal cord,
# and save them as excels or plots.
#
# Charley Gros 2018-05-17
# Modified: 2018-09-12

import sys
import os
import pandas as pd
import numpy as np
import operator
import sys
import matplotlib.pyplot as plt
from matplotlib import rcParams

import spinalcordtoolbox.image as msct_image

rcParams.update({'font.size': 18})
CMAP_CERV = plt.get_cmap('Greens')(np.linspace(0.5, 1, 7))
CMAP_THOR = plt.get_cmap('Blues')(np.linspace(0.5, 1, 12))
CMAP_LUMB = plt.get_cmap('Reds')(np.linspace(0.5, 1, 5))

SCALE_PLOT_DCT = {'csa': [0, 100],
                    'RL_diameter': [0, 20],
                    'AP_diameter': [0, 15],
                    'eccentricity': [0, 1.1],
                    'equivalent_diameter': [0, 15],
                    'orientation': [-90, 90],
                    'ratio_minor_major': [0, 1.1],
                    'solidity': [0, 1.1],
                    'symmetry': [0, 1.1]}


def total_volume_cord(values, subject_id, output_fname):
    """
    Compute the volume of the entire spinal cord.
    :param path_subject: with a '/' at the end
    :param subject_id: subject folder name
    :param output_fname: filename of the csv file used to save the results
    """
    # check if output_fname file already exist
    if os.path.isfile(output_fname):
        tvc_pd = pd.read_csv(output_fname)[['subject_id', 'total_volume_cord']]
    else:
        tvc_pd = pd.DataFrame.from_dict({'subject_id': [], 'total_volume_cord': []})

    tvc = np.sum(values)

    # if the subject already in the output_fname file, the value is updated, otherwise the new subject is appended
    idx_pd = len(tvc_pd.index) if subject_id not in tvc_pd['subject_id'].values else tvc_pd[tvc_pd['subject_id'] == subject_id].index[0]
    tvc_pd.loc[idx_pd, 'subject_id'] = subject_id
    tvc_pd.loc[idx_pd, 'total_volume_cord'] = tvc
    tvc_pd.to_csv(output_fname)


def plot_profile(metric, pd2plot, subject_id, fname_out):
    '''
    Plots the profile of a given metric along the Superior-to-Inferior axis.
    '''
    toPlot_pd = pd2plot[['lvl', metric]]
    toPlot_pd = toPlot_pd.dropna(subset=[metric])
    toPlot_pd = toPlot_pd.reset_index(drop=True)

    lvl_lst = list(set(toPlot_pd.lvl))
    colors = np.vstack((CMAP_CERV, CMAP_THOR, CMAP_LUMB))

    plt.figure(figsize=(16, 6))
    for i, (lvl, color) in enumerate(zip(lvl_lst, colors[:len(lvl_lst)]), 1):
        toPlot_pd_cur = toPlot_pd[toPlot_pd['lvl'] == lvl]
        plt.scatter(toPlot_pd_cur.index.values,
                    toPlot_pd_cur[metric].values,
                    edgecolors='none', s=15,
                    label=str(lvl), c=color)
    plt.xlim([0, len(toPlot_pd.index)])
    plt.ylim(SCALE_PLOT_DCT[metric])
    plt.grid()
    plt.xlabel('slice along the Superior-to-Inferior axis')
    plt.ylabel(metric)
    plt.title('Subject: ' + subject_id)
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.15), ncol=12, fontsize=12)
    plt.savefig(fname_out, bbox_inches="tight")


def find_maxVert_perScan(data_folder):
    '''
    Opens each labelled image and find the max vertebral level available.
    Return a dictionary with the scan_name as key, the max vert as value.
    '''
    scan_max_vert_dct = {}
    for scan_foldname in os.listdir(data_folder):
        path_labeled_cord_img = os.path.join(data_folder, scan_foldname, scan_foldname + '_seg_manual_labeled.nii.gz')
        if not os.path.isfile(path_labeled_cord_img):
            path_labeled_cord_img = os.path.join(data_folder, scan_foldname, scan_foldname + '_seg_labeled.nii.gz')
        if os.path.isfile(path_labeled_cord_img):
            scan_max_vert_dct[scan_foldname] = np.max(np.unique(msct_image.Image(path_labeled_cord_img).data))
    return scan_max_vert_dct


def extract_metrics_scans_asPanda(data_folder, scan_max_vert_dct, shape_metrics_lst):
    '''
    Loops across each scan results and extract the values, per vertebral level.
    Returns a list of panda dataframes, one per scan with the following column: z_idx, lvl, csa and the shape_metrics_lst
    '''
    scan_results_pd_lst = []
    for scan_foldname, max_vert in sorted(scan_max_vert_dct.items(), key=operator.itemgetter(1)):
        path_scan_folder = os.path.join(data_folder, scan_foldname)
        if os.path.isdir(path_scan_folder):
            path_labeled_cord_img = os.path.join(path_scan_folder, scan_foldname + '_seg_manual_labeled.nii.gz')
            if not os.path.isfile(path_labeled_cord_img):
                path_labeled_cord_img = os.path.join(path_scan_folder, scan_foldname + '_seg_labeled.nii.gz')

            path_shape_csv = os.path.join(path_scan_folder, 'metrics', scan_foldname + '_seg_manual_shape.csv')
            if not os.path.isfile(path_shape_csv):
                path_shape_csv = os.path.join(path_scan_folder, 'metrics', scan_foldname + '_seg_shape.csv')

            path_csa_pickle = os.path.join(path_scan_folder, 'metrics', 'csa_per_slice.pickle')

            if os.path.isfile(path_labeled_cord_img) and os.path.isfile(path_shape_csv) and os.path.isfile(path_csa_pickle):
                labeled_cord_img = msct_image.Image(path_labeled_cord_img)
                shape_pd = pd.read_csv(path_shape_csv)[[u'Unnamed: 0'] + shape_metrics_lst]
                shape_pd = shape_pd.rename(columns={u'Unnamed: 0': 'z_idx'})
                csa_pd = pd.read_pickle(path_csa_pickle)[[u'CSA (mm^2)', u'Slice (z)']]
                csa_pd = csa_pd.rename(columns={u'Slice (z)': 'z_idx', u'CSA (mm^2)': 'csa'})

                scan_results_tmp_dct = {}
                for m in ['z_idx', 'csa', 'lvl'] + shape_metrics_lst:
                    scan_results_tmp_dct[m] = []
                scan_results_tmp_pd = pd.DataFrame.from_dict(scan_results_tmp_dct)

                for zz in range(labeled_cord_img.dim[1]):
                    lvl = np.max(np.unique(labeled_cord_img.data[:, zz, :]))
                    if lvl:
                        idx_tmp = len(scan_results_tmp_pd.index.values)
                        scan_results_tmp_pd.loc[idx_tmp, 'z_idx'] = zz
                        scan_results_tmp_pd.loc[idx_tmp, 'csa'] = csa_pd[csa_pd.z_idx == zz].csa.values[0]
                        scan_results_tmp_pd.loc[idx_tmp, 'lvl'] = lvl
                        for m_s in shape_metrics_lst:
                            if len(shape_pd[shape_pd.z_idx == zz][m_s].values):
                                scan_results_tmp_pd.loc[idx_tmp, m_s] = shape_pd[shape_pd.z_idx == zz][m_s].values[0]

                scan_results_pd_lst.append(scan_results_tmp_pd)
                if max_vert == max(scan_max_vert_dct.values()):
                    break
    return scan_results_pd_lst


def remove_duplicated_vert(pd_lst, shape_metrics_lst):
    '''
    Because of the possible overlap between the scans of a subjects, we remove here the duplicated measures.
    Returns one panda data frame covering the entire spinal cord.
    '''
    pd_out = pd_lst[0]
    for scan_result_cur in pd_lst[1:]:
        lvl_cur = scan_result_cur.lvl.values
        lvl_saved = pd_out.lvl.values
        intersec = list(set(lvl_cur) & set(lvl_saved))
        print '\tOverlap detected for the vert. levels: ' + ' '.join([str(int(l)) for l in intersec])
        if len(intersec):
            for lvl_intersec in intersec:
                lvl_intersec_pd_saved = pd_out[pd_out.lvl == lvl_intersec]
                lvl_intersec_pd_cur = scan_result_cur[scan_result_cur.lvl == lvl_intersec]
                if len(lvl_intersec_pd_saved.index.values) < len(lvl_intersec_pd_cur.index.values):
                    pd_out = pd_out.drop(lvl_intersec_pd_saved.index)
                    pd_out = pd_out.append(lvl_intersec_pd_cur, ignore_index=True)
        pd_out = pd_out.append(scan_result_cur[scan_result_cur.lvl > max(lvl_saved)], ignore_index=True)

    lvl_available = [int(l) for l in list(set(pd_out.lvl.values))]
    if sorted(lvl_available) != range(min(lvl_available), max(lvl_available)+1):
        sys.exit('Charley, there is a pb with the available vert: ' + ' '.join([str(l) for l in lvl_available]))

    pd_out = pd_out.sort_values(['lvl', 'z_idx'], ascending=[True, False])

    pd_out = pd_out[['lvl', 'csa'] + shape_metrics_lst + ['z_idx'] ]

    return pd_out


def run_main(path_data_folder, subject_id, path_results_folder):
    path_subject_folder = os.path.join(path_data_folder, subject_id)
    path_subject_result_folder = os.path.join(path_results_folder, subject_id)
    if not os.path.isdir(path_subject_result_folder):
        os.makedirs(path_subject_result_folder)

    shape_metrics_lst = ['AP_diameter', 'RL_diameter', 'eccentricity', 'equivalent_diameter', 'orientation', 'ratio_minor_major', 'solidity', 'symmetry']

    scan_max_vert_dct = find_maxVert_perScan(path_subject_folder)

    scan_results_pd_lst = extract_metrics_scans_asPanda(path_subject_folder, scan_max_vert_dct, shape_metrics_lst)

    scan_results_pd = remove_duplicated_vert(scan_results_pd_lst, shape_metrics_lst)
    scan_results_pd.to_csv(os.path.join(path_subject_result_folder, 'measures.csv'), index=False)

    total_volume_cord(values=scan_results_pd[(scan_results_pd.lvl >= 1.0)&(scan_results_pd.lvl <= 24.0)].csa.values,
                        subject_id=subject_id,
                        output_fname=path_results_folder + 'total_volume_cord.csv')

    for metric in SCALE_PLOT_DCT.keys():
        profile_filename = os.path.join(path_subject_result_folder, metric + '_profile.png')
        plot_profile(metric, scan_results_pd, subject_id, profile_filename)


if __name__ == '__main__':
    path_data, subject, path_results = sys.argv[1:]
    run_main(path_data, subject[:-1], path_results)
