import filecmp
import os
import json
import log_wrapper as nl

logger = nl.setup_logger('first_logger', 'first_logfile.log')


def are_dir_trees_equal(dir1, dir2, datetime_tag):
    """
        #Data integrity maintained - list of corrupt files/dirs
        Is there any junk (file/dir) copied in dst
        Any missing file/dir in dst
    """

    do_match = ''
    result = dict()

    dirs_cmp = filecmp.dircmp(dir1, dir2)

    if len(dirs_cmp.left_only)>0 or len(dirs_cmp.right_only)>0 or len(dirs_cmp.funny_files)>0:

        do_match = False
    (_, mismatch, errors) =  filecmp.cmpfiles(
        dir1, dir2, dirs_cmp.common_files, shallow=False)

    if len(mismatch)>0 or len(errors)>0:
        logger.info("RESULT " + str(result))
        result["reason"] = "MISMATCH" + " ".join(mismatch)
        do_match = False
        logger.info("RESULT " + str(result))

    src_files = [f for f in os.listdir(dir1) if os.path.isfile(f)]

    for file in src_files:

        if os.path.exists(os.path.join(dir2, file)):
            do_compare = filecmp.cmp(os.path.join(dir1, file), os.path.join(dir2, file))
            if not do_compare:
                do_match = False
                logger.info("RESULT " + str(result))
                result["reason"] = f"{dir1} and {file} are not equal."
        else:
            do_match = False
            result["reason"] = f"{dir2} and {file} files does not exist."
            logger.info("RESULT " + str(result))

    for common_dir in dirs_cmp.common_dirs:
        new_dir1 = os.path.join(dir1, common_dir)
        new_dir2 = os.path.join(dir2, common_dir)
        if not are_dir_trees_equal(new_dir1, new_dir2, datetime_tag):
            do_match = False
            result["reason"] = f"{new_dir1} and {new_dir2} are not equal."
            logger.info("RESULT " + str(result))

    logger.info("RESULTfinal " + str(result))
    if len(result) > 0:
        write_results(result, f'test_details_{datetime_tag}.json')

    return do_match


def write_results(result, file_name):
    """

    :param result:
    :param datetime_tag:
    :return:
    """
    with open(file_name, 'a') as fp:
        json.dump(result, fp, indent=4)
