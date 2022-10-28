#!/usr/bin/env python3

HOME_TIMEZONE = "Canada/Pacific"


from my_utility_scripts.logging_tools import my_logger, logging_callstacks
my_logger.info(f"开始运行module:{__name__}, 其文件位置在: {__file__}")

import datetime
import dateutil.parser
import dateutil.relativedelta
from dateutil.zoneinfo import getzoneinfofile_stream, ZoneInfoFile
from dateutil.tz import gettz
import pytz

# 下一个版本中会删除：
Vancouver_timezone = pytz.timezone('Canada/Pacific')
Beijing_timezone = pytz.timezone('Asia/Shanghai')
UTC_timezone = pytz.timezone('UTC')

tzname_chart = {
    "PDT": ("Vancouver", Vancouver_timezone),
    "PST": ("Vancouver", Vancouver_timezone),
    "CST": ("Beijing", Beijing_timezone)
}
##

all_timezones_set = ZoneInfoFile(getzoneinfofile_stream()).zones.keys()


# helper functions
def _naive_to_aware(naive_datetimepoint, timezone_stamp):
    """
    INPUT >>>>> naive_datetimepoint: a naive datetime object;
                timezone_stamp: a dateutil.tz timezone instance.
    OUTPUT >>>> an aware datetime object with the timezone corresponding to the given input
                human intervention may be needed: requires a input for ambiguous daylight saving time.
    """
    assert isinstance(naive_datetimepoint, datetime.datetime)
    try:
        assert naive_datetimepoint.tzinfo is None# 确保这个datetime的确是naive
    except AssertionError as e:
        new_e = type(e)(f' 肇事的naive_datetimepoint是：{str(naive_datetimepoint)}')
        raise new_e
    timezone_obj = pytz.timezone(timezone_stamp)
    # timezone_obj = dateutil.tz.gettz(timezone_stamp)
    # is_dst set to None, so that any ambiguous DTP involving daylight saving
    # time will raise an error and requires human intervention
    AWARE_datetimepoint = timezone_obj.localize(naive_datetimepoint, is_dst=None)
    # AWARE_datetimepoint = naive_datetimepoint.replace(tzinfo=timezone_obj)
    return AWARE_datetimepoint


def _utc_to_local(utc_datetimepoint_aware, local_timezone_stamp):
    """
    input:
           utc_datetimepoint_aware --- an instance of datetime.datetime representing utc timepoint, with tzinfo set to UTC
           local_timezone_stamp --- e.g. 'Canada/Pacific'

    output:
            local datetimepoint with proper timezone info
    """
    assert isinstance(utc_datetimepoint_aware, datetime.datetime)
    assert 'UTC' in utc_datetimepoint_aware.tzname()
    assert local_timezone_stamp in all_timezones_set
    local_datetimepoint_aware = utc_datetimepoint_aware.astimezone(tz=dateutil.tz.gettz(local_timezone_stamp))
    return local_datetimepoint_aware


def _local_to_utc(local_datetimepoint):
    """
        input>>>>>>>>>>>> must be an aware timepoint with local timezone attached.
        output>>>>>>>>>>>> corresponding utc timepoint with utc timezone attached.
    """
    assert isinstance(local_datetimepoint, datetime.datetime)
    assert _check_Is_timezone_aware(local_datetimepoint), "必须是一个timezone aware的输入量"
    utc_datetimepoint_aware = local_datetimepoint.astimezone(tz=dateutil.tz.UTC)
    return utc_datetimepoint_aware

def _check_Is_timezone_aware(datetimeObj):
    assert isinstance(datetimeObj, datetime.datetime)
    if (datetimeObj.tzinfo is not None) and (datetimeObj.tzinfo.utcoffset(datetimeObj) is not None):
        return True
    return False


# public API:
def today_date():
    return datetime.datetime.now().date()

def local_now():
    return datetime.datetime.now(tz=gettz(HOME_TIMEZONE))

def parse_dateString(dateString):
    """returns a <datetime.date> instance"""
    assert isinstance(dateString, str), "输入参数需要是<str>！"
    dateString = dateString.strip()
    for fmt in ["%Y-%m-%d", "%Y/%m/%d", "%Y.%m.%d", "%Y%m%d"]: # "YYYY-MM-DD", "YYYY/MM/DD", "YYYY.MM.DD". "YYYYMMDD"
        try:
            dObj = datetime.datetime.strptime(dateString, fmt).date()
            return dObj
        except ValueError as ve:
            pass
    raise ValueError('Not a valid date!')


class FuzzyTimePoint:
    """
        '1981-04-**(--FUZZY--)鸡年4月份'
        '199*-**-**(--FUZZY--)90年代'
    """

    def __init__(self, representative_point, original_datetime_descriptionString):
        # datetime.datetime 或者 datetime.date
        assert isinstance(representative_point,
                          (datetime.date, datetime.datetime))
        if isinstance(representative_point, datetime.datetime):#datetime.date的话不用理会，但如果是datetime.datetime,则需要：
            assert _check_Is_timezone_aware(representative_point), "需要一个timezone aware的代表时间点！"
            representative_point = self.UTCify(representative_point)
        self.original_datetime_descriptionString = original_datetime_descriptionString
        self.representative_point = representative_point

    def __lt__(self, other):
        return self.representative_point < other.representative_point

    def __gt__(self, other):
        return self.representative_point > other.representative_point

    def __eq__(self, other):
        return self.representative_point == other.representative_point

    def UTCify(self, dtp):
        return _local_to_utc(dtp)




class UniversalTimePoint:
    """ 
        在数据库中存储的只有3种类别:
            1) Datetime: an aware datetime.datetime: e.g. "2010-05-13 09:05:00+00:00", 无论是何时区，内部存储的时候一律转化为UTC时间;
            2) Date: datetime.date: e.g. "2010-05-13";
            3) FuzzyTimePoint: YYYY-MM-DD HH:MM:SS+00:00(--FUZZY--)ORIGINAL_STRING
    """
    
    def __init__(self, datetime_info):
        """ 
            <str> 只有可能读自数据库，严格格式
            
            <str tuple>: 
                    (datetime_string, timezone_stamp)
                    (datetime_string, original_fuzzy_string)
            
            <datetime.datetime>: 必须带有timezone
            
            <datetime.date>:
            
            <FuzzyTimePoint>:
        """
        # my_logger.info("我收到的 datetime_info 是：{0}, 它的<type>是：{1}".format(datetime_info, type(datetime_info)))
        assert isinstance(datetime_info, (str, tuple)), "非法的 <type>: datetime_info ！"
        parsing_handlers = {
            str: self._string_in_three_forms,
            tuple: self._datetime_info_tuple,
            datetime.datetime: _local_to_utc,
            datetime.date: lambda date_obj: date_obj,
            FuzzyTimePoint: lambda fuzzytimepoint_obj: fuzzytimepoint_obj
        }
        handler_to_use = parsing_handlers[type(datetime_info)]
        self.utcified_python_datetime = handler_to_use(datetime_info) # UTCified datetime
    
    def _string_in_three_forms(self, datetime_string):
        """只接受完全符合database储存标准的 datetime_string"""
        
        assert isinstance(datetime_string, str), "datetime_string 需要是<str>！"
        
        utcdatetime_database_standard = "%Y-%m-%d %H:%M:%S+00:00"
        try:
            timepoint_obj = datetime.datetime.strptime(datetime_string, utcdatetime_database_standard)
            timepoint_obj = _naive_to_aware(timepoint_obj, 'UTC')
            return timepoint_obj
        except ValueError:
            my_logger.info(f"Just tried to parse <{datetime_string}> assuming it is utc datetime, apparently it's not.")
        
        date_standard = "%Y-%m-%d"
        try:
            date_obj = datetime.datetime.strptime(datetime_string, date_standard).date()
            return date_obj
        except ValueError:
            my_logger.info(f"Just tried to parse <{datetime_string}> assuming it is date, apparently it's not.")
        
        fuzzy_database_standard = "" # 待完成
        
        raise ValueError(f'读取的字符为非法的日期时间格式：{datetime_string}')
        
    
    def _datetime_info_tuple(self, datetime_info_tuple):
        assert type(datetime_info_tuple[0]) == str
        
        possible_date_string = datetime_info_tuple[0]
        try:
            date_obj = parse_dateString(possible_date_string)
            return date_obj
        except ValueError:
            my_logger.info(f"Just tried to parse <{possible_date_string}> in tuple, assuming it is date, apparently it's not.")
            
        if datetime_info_tuple[1] in all_timezones_set:
            # tuple 的第二项是 timezone， 说明是要生成 <datetime.datetime>:
            (datetime_string, timezone) = datetime_info_tuple
            datetime_string = datetime_string.strip()
            datetime_naive = dateutil.parser.parse(datetime_string, ignoretz=True)
            datetime_aware = datetime_naive.replace(tzinfo=dateutil.tz.gettz(timezone))
            return _local_to_utc(datetime_aware)
        else:
            # tuple 的第二项是普通字符， 说明是要生成 <FuzzyTimePoint>:
            return FuzzyTimePoint(datetime_info_tuple[0], datetime_info_tuple[1])
    
    def __str__(self):
        return f"<UniversalTimePoint object @ {id(self)} representing: {self.timepoint_string_in_database}>"
    
    def __eq__(self, other):
        return self.utcified_python_datetime == other.utcified_python_datetime
    
    @property
    def chronological_type(self):
        type_switch = {
            datetime.datetime: "datetime",
            datetime.date: "date",
            FuzzyTimePoint: "fuzzy"
        }
        return type_switch(type(self.utcified_python_datetime))
    
    @property
    def timepoint_string_in_database(self):
        """ polymophism string output"""
        stringify_handlers = {
            datetime.datetime: lambda datetime_obj: datetime_obj.strftime("%Y-%m-%d %H:%M:%S+00:00"),
            datetime.date: lambda date_obj : date_obj.isoformat(),
            FuzzyTimePoint: lambda fuzzytimepoint_obj: str(fuzzytimepoint_obj)
        }
        type_of_this_timepoint = type(self.utcified_python_datetime)
        handler_to_use = stringify_handlers[type_of_this_timepoint]
        return handler_to_use(self.utcified_python_datetime)
    
    def report_local_timepoint_string(self, local_timezone_stamp=None):
        assert (local_timezone_stamp is None) \
                    or local_timezone_stamp in all_timezones_set 
        parsers_switch = {
            datetime.datetime: lambda: _utc_to_local(self.utcified_python_datetime, local_timezone_stamp).strftime("%Y-%m-%d %H:%M:%S"),
            datetime.date: lambda: self.utcified_python_datetime.isoformat(),
            FuzzyTimePoint: lambda: str(self.utcified_python_datetime) # 待完成
        }
        return parsers_switch[type(self.utcified_python_datetime)]()