import logging
import os
import unittest

import nose.tools

import test_utils
from ece2cmor3 import cmor_source, cmor_target, cmor_task, ifs2cmor, postproc

logging.basicConfig(level=logging.DEBUG)
ifs2cmor.ifs_gridpoint_file_ = "ICMGG+199003"
ifs2cmor.ifs_spectral_file_ = "ICMSH+199003"


class ifs2cmor_tests(unittest.TestCase):

    @staticmethod
    def test_postproc_gridmean():
        abspath = test_utils.get_table_path()
        targets = cmor_target.create_targets(abspath, "CMIP6")
        source = cmor_source.ifs_source.create(79, 128)
        target = [t for t in targets if t.variable == "clwvi" and t.table == "CFday"][0]
        task = cmor_task.cmor_task(source, target)
        postproc.mode = postproc.skip
        ifs2cmor.temp_dir_ = os.getcwd()
        setattr(task, cmor_task.filter_output_key, ["ICMGG+199003"])
        ifs2cmor.postprocess([task])
        path = os.path.join(os.getcwd(), "clwvi_CFday.nc")
        nose.tools.eq_(getattr(task, cmor_task.output_path_key), path)
        nose.tools.eq_(getattr(task, "cdo_command"), "-setgridtype,regular -daymean -selcode,79")

    @staticmethod
    def test_postproc_gridmeans():
        abspath = test_utils.get_table_path()
        targets = cmor_target.create_targets(abspath, "CMIP6")
        source1 = cmor_source.ifs_source.create(79, 128)
        target1 = [t for t in targets if t.variable == "clwvi" and t.table == "CFday"][0]
        task1 = cmor_task.cmor_task(source1, target1)
        source2 = cmor_source.ifs_source.create(164, 128)
        target2 = [t for t in targets if t.variable == "clt" and t.table == "day"][0]
        task2 = cmor_task.cmor_task(source2, target2)
        postproc.mode = postproc.skip
        ifs2cmor.temp_dir_ = os.getcwd()
        setattr(task1, cmor_task.filter_output_key, ["ICMGG+199003"])
        setattr(task2, cmor_task.filter_output_key, ["ICMGG+199003"])
        ifs2cmor.postprocess([task1, task2])
        path = os.path.join(os.getcwd(), "clt_day.nc")
        nose.tools.eq_(getattr(task2, cmor_task.output_path_key), path)
        nose.tools.eq_(getattr(task1, "cdo_command"), "-setgridtype,regular -daymean -selcode,79")

    @staticmethod
    def test_postproc_specmean():
        testdata = os.path.dirname(__file__) + "/test_data/ifsdata/6hr/ICMSHECE3+199001"
        if test_utils.is_lfs_ref(testdata):
            logging.info("Skipping test_postproc_specmean, download test data from lfs first")
            return
        abspath = test_utils.get_table_path()
        targets = cmor_target.create_targets(abspath, "CMIP6")
        source = cmor_source.ifs_source.create(130, 128)
        target = [t for t in targets if t.variable == "ta" and t.table == "Amon"][0]
        task = cmor_task.cmor_task(source, target)
        postproc.mode = postproc.skip
        ifs2cmor.temp_dir_ = os.getcwd()
        ifs2cmor.ifs_spectral_file_ = testdata
        setattr(task, cmor_task.filter_output_key, [testdata])
        ifs2cmor.postprocess([task])
        path = os.path.join(os.getcwd(), "ta_Amon.nc")
        nose.tools.eq_(getattr(task, cmor_task.output_path_key), path)
        nose.tools.eq_(getattr(task, "cdo_command"), "-sp2gpl -monmean -sellevel,100000.,92500.,85000.,70000.,"
                                                     "60000.,50000.,40000.,30000.,25000.,20000.,15000.,10000.,7000.,"
                                                     "5000.,3000.,2000.,1000.,500.,100. "
                                                     "-selzaxis,pressure -selcode,130")

    @staticmethod
    def test_postproc_daymax():
        abspath = test_utils.get_table_path()
        targets = cmor_target.create_targets(abspath, "CMIP6")
        source = cmor_source.ifs_source.create(165, 128)
        target = [t for t in targets if t.variable == "sfcWindmax" and t.table == "day"][0]
        task = cmor_task.cmor_task(source, target)
        postproc.mode = postproc.skip
        ifs2cmor.temp_dir_ = os.getcwd()
        setattr(task, cmor_task.filter_output_key, ["ICMGG+199003"])
        ifs2cmor.postprocess([task])
        path = os.path.join(os.getcwd(), "sfcWindmax_day.nc")
        nose.tools.eq_(getattr(task, cmor_task.output_path_key), path)
        nose.tools.eq_(getattr(task, "cdo_command"), "-daymax -setgridtype,regular -selcode,165")

    @staticmethod
    def test_postproc_tasmax():
        abspath = test_utils.get_table_path()
        targets = cmor_target.create_targets(abspath, "CMIP6")
        source = cmor_source.ifs_source.create(201, 128)
        target = [t for t in targets if t.variable == "tasmax" and t.table == "Amon"][0]
        task = cmor_task.cmor_task(source, target)
        postproc.mode = postproc.skip
        ifs2cmor.temp_dir_ = os.getcwd()
        setattr(task, cmor_task.filter_output_key, ["ICMGG+199003"])
        ifs2cmor.postprocess([task])
        path = os.path.join(os.getcwd(), "tasmax_Amon.nc")
        nose.tools.eq_(getattr(task, cmor_task.output_path_key), path)
        nose.tools.eq_(getattr(task, "cdo_command"), "-monmean -daymax -setgridtype,regular -selcode,201")

    @staticmethod
    def test_postproc_windspeed():
        abspath = test_utils.get_table_path()
        targets = cmor_target.create_targets(abspath, "CMIP6")
        source = cmor_source.ifs_source.read("var88=sqrt(sqr(var165)+sqr(var166))")
        target = [t for t in targets if t.variable == "sfcWind" and t.table == "6hrPlevPt"][0]
        task = cmor_task.cmor_task(source, target)
        postproc.mode = postproc.skip
        ifs2cmor.temp_dir_ = os.getcwd()
        setattr(task, cmor_task.filter_output_key, ["ICMGG+199003"])
        ifs2cmor.postprocess([task])
        path = os.path.join(os.getcwd(), "sfcWind_6hrPlevPt.nc")
        nose.tools.eq_(getattr(task, cmor_task.output_path_key), path)
        nose.tools.eq_(getattr(task, "cdo_command"),
                       "-expr,'var88=sqrt(sqr(var165)+sqr(var166))' -setgridtype,regular -selhour,0,6,12,18 -selcode,"
                       "165,166")

    @staticmethod
    def test_postproc_max_windspeed():
        abspath = test_utils.get_table_path()
        targets = cmor_target.create_targets(abspath, "CMIP6")
        source = cmor_source.ifs_source.read("var88=sqrt(sqr(var165)+sqr(var166))")
        target = [t for t in targets if t.variable == "sfcWindmax" and t.table == "day"][0]
        task = cmor_task.cmor_task(source, target)
        postproc.mode = postproc.skip
        ifs2cmor.temp_dir_ = os.getcwd()
        setattr(task, cmor_task.filter_output_key, ["ICMGG+199003"])
        ifs2cmor.postprocess([task])
        path = os.path.join(os.getcwd(), "sfcWindmax_day.nc")
        nose.tools.eq_(getattr(task, cmor_task.output_path_key), path)
        nose.tools.eq_(getattr(task, "cdo_command"),
                       "-daymax -expr,'var88=sqrt(sqr(var165)+sqr(var166))' -setgridtype,regular -selcode,165,166")
