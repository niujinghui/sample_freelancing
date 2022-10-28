from .chronology import *
import datetime
import pytz
from dateutil import tz, parser
import pytest

#
#
#
#
# test "2018-02-28":
def test_parsing_most_strict_date_str():
    assert UniversalTimePoint("2018-02-28").utcified_python_datetime == datetime.date(2018, 2, 28)
#
#
#
#
# test "yyyy/mm/dd", "yyyy.mm.dd":
@pytest.mark.parametrize("date_str, expected_date_obj", [
    ("2018.02.28", datetime.date(2018, 2, 28)),
    ("2018/02/28", datetime.date(2018, 2, 28)),
    ("20180228", datetime.date(2018, 2, 28)),
    ("02/28/2018", datetime.date(2018, 2, 28)),
    ("28/02/2018", datetime.date(2018, 2, 28))
])
def test_parsing_strict_date_str(date_str, expected_date_obj):
    with pytest.raises(ValueError): # expected to fail for all cases below:
        assert UniversalTimePoint(date_str).utcified_python_datetime == expected_date_obj


@pytest.mark.parametrize("date_info_tup, expected_date_obj", [
    (("2018.02.28", None), datetime.date(2018, 2, 28)),
    (("2018/02/28", None), datetime.date(2018, 2, 28)),
    (("2018/02/28", None), datetime.date(2018, 2, 28)),
    (("2018/02/28", None), datetime.date(2018, 2, 28)),
    (("2018/02/28", None), datetime.date(2018, 2, 28))
])
def test_parsing_date_in_tuple(date_info_tup, expected_date_obj):
    assert UniversalTimePoint(date_info_tup).utcified_python_datetime == expected_date_obj
















@pytest.fixture(scope="class")
def baseline_date():
    print('opening baseline_date fixture ...')
    fixture_obj = {}
    fixture_obj['non_ambiguous'] = datetime.date(2018, 2, 28)
    fixture_obj['ambiguous'] = datetime.date(2018, 2, 1)
    yield fixture_obj
    print('closing baseline_date fixture ...')


class Test_parse_dateString:

    func_to_be_tested = staticmethod(
        parse_dateString)  # mount on the testing target function

    def test_parse_dateString_ISO(self, baseline_date):
        assert self.func_to_be_tested(
            "2018-02-28") == baseline_date['non_ambiguous']
        assert self.func_to_be_tested(
            "2018-02-01") == baseline_date['ambiguous']
        with pytest.raises(ValueError):
            self.func_to_be_tested('2018-13-32')

    def test_parse_dateString_slash_separated(self, baseline_date):
        assert self.func_to_be_tested(
            "2018/02/28") == baseline_date['non_ambiguous']
        assert self.func_to_be_tested("2018/02/01") == baseline_date[
            'ambiguous']  # 只要是 YYYY 在最前面，就不会产生歧义。
        with pytest.raises(ValueError):
            self.func_to_be_tested('2018/13/32')

    def test_parse_dateString_dot_separated(self, baseline_date):
        assert self.func_to_be_tested(
            "2018.02.28") == baseline_date['non_ambiguous']
        assert self.func_to_be_tested("2018.02.01") == baseline_date[
            'ambiguous']  # 只要是 YYYY 在最前面，就不会产生歧义。
        with pytest.raises(ValueError):
            self.func_to_be_tested('2018.13.32')

    def test_parse_dateString_nothing_separated(self, baseline_date):
        assert self.func_to_be_tested(
            "20180228") == baseline_date['non_ambiguous']
        assert self.func_to_be_tested("20180201") == baseline_date[
            'ambiguous']  # 只要是 YYYY 在最前面，就不会产生歧义。
        with pytest.raises(ValueError):
            self.func_to_be_tested('20181332')

    def test_parse_dateString_american(self, baseline_date):
        with pytest.raises(ValueError):
            # american style:
            assert self.func_to_be_tested(
                "02/28/2018") == baseline_date['non_ambiguous']
        with pytest.raises(ValueError):
            assert self.func_to_be_tested(
                "02/01/2018") == baseline_date['ambiguous']
        with pytest.raises(ValueError):
            # european style:
            assert self.func_to_be_tested(
                "28/02/2018") == baseline_date['non_ambiguous']

    def test_parse_dateString_input_wrongType(self):
        with pytest.raises(AssertionError):
            self.func_to_be_tested(20180201)

    def test_parse_dateString_input_withWhiteSpaces(self, baseline_date):
        assert self.func_to_be_tested(
            "   2018-02-28 \n") == baseline_date['non_ambiguous']

    def test_parse_dateString_strictness(self):
        with pytest.raises(ValueError):
            self.func_to_be_tested(
                "2018-02-28 13:22:56"
            )  # 在 strict_date_format 设置为True的模式下，连 datetime 都不认可，必须是 date!


@pytest.fixture(scope="class")
def baseline_datetime():
    print('opening baseline_datetime fixture ...')
    timezone_obj = pytz.timezone('Canada/Pacific')
    a_timezone_naive_datetime = datetime.datetime(2018, 7, 28, 22, 30, 23)
    a_timezone_aware_datetime = timezone_obj.localize(
        a_timezone_naive_datetime, is_dst=None)
    yield a_timezone_aware_datetime
    print('closing baseline_datetime fixture ...')


class Test_parse_datetimeString:

    def test_parse_dateString_UTC(self, baseline_datetime):
        assert UniversalTimePoint(
            "2018-07-29 05:30:23+00:00").utcified_python_datetime == baseline_datetime


# def test_UniversalTimePoint():
#     assert 0
