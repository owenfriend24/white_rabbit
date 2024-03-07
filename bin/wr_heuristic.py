"""Heuristic file for converting fMRI data using HeuDiConv."""


def create_key(template, outtype=("nii.gz",), annotation_classes=None):
    if template is None or not template:
        raise ValueError("Template must be a valid format string")
    return template, outtype, annotation_classes


def infotodict(seqinfo):
    """Heuristic evaluator for determining which runs belong where

    allowed template fields - follow python string module:

    item: index within category
    subject: participant id
    seqitem: run number during scanning
    subindex: sub index within group
    """
    # anatomicals
    key_T1w = create_key("sub-{subject}/anat/sub-{subject}_T1w")
    key_T2w = create_key("sub-{subject}/anat/sub-{subject}_T2w_run={item}")

    key_fm_ap = create_key("sub-{subject}/fmap/sub-{subject}_dir-AP_run-{item}_epi")
    key_fm_pa = create_key("sub-{subject}/fmap/sub-{subject}_dir-PA_run-{item}_epi")

    key_phasediff = create_key("sub-{subject}/fmap/sub-{subject}_run-{item:02d}_phasediff")
    key_imagine = create_key('sub-{subject}/func/sub-{subject}_task-imagine_run-{item:02d}_bold')
    key_imagine_sbref = create_key('sub-{subject}/func/sub-{subject}_task-imagine_run-{item:02d}_sbref')
    
    

    # sort scans into file types
    info = {
        key_T1w: [],
        key_T2w: [],
        key_fm_ap: [],
        key_fm_pa: [],
        key_phasediff: [],
        key_imagine: [],
        key_imagine_sbref: []

    }
    n_fieldmap = 0
    n_phase = 0
    n_magnitude = 0
    n_T2 = 0
    n_T1 = 0
    
    
    p = None
    for s in seqinfo:
        """
        The namedtuple `s` contains the following fields:

        * total_files_till_now
        * example_dcm_file
        * series_id
        * dcm_dir_name
        * unspecified2
        * unspecified3
        * dim1
        * dim2
        * dim3
        * dim4
        * TR
        * TE
        * protocol_name
        * is_motion_corrected
        * is_derived
        * patient_id
        * study_description
        * referring_physician_name
        * series_description
        * image_type
        """
        if s.series_description == 'mprage':
            # T1 highres anatomical
            info[key_T1w].append(s.series_id)
            n_T1 +=1
            print(f'INSIDE::{s.series_id}::{n_T1}::{s.series_files}')
            
        elif 'T2' in s.series_description:
            # T2 coronal anatomical
            info[key_T2w].append(s.series_id)
            n_T2 += 1
            print(f'INSIDE::{s.series_id}::{n_T2}::{s.series_files}')
                
            
        elif s.series_description == "cmrr_mbep2d_se_ap":
            info[key_fm_ap].append(s.series_id)
        elif s.series_description == "cmrr_mbep2d_se_pa":
             info[key_fm_pa].append(s.series_id)

        # functional scans
        elif s.series_description == 'imagine' and s.series_files > 20:
            info[key_imagine].append(s.series_id)
            if p.series_description == 'imagine_SBRef':
                info[key_imagine_sbref].append(p.series_id)
        p = s
    return info
