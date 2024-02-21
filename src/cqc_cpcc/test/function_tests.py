import datetime as DT
from cqc_cpcc.utilities.date import get_datetime



def test_1():
    today = DT.date.today()
    yesterday = today - DT.timedelta(days=2)
    week_ago = yesterday - DT.timedelta(days=7)
    middle_of_week = week_ago + DT.timedelta(days=3)

    print('Week agp: %s' % week_ago.strftime("%m-%d-%Y"))
    print('Middle of Week: %s' % middle_of_week.strftime("%m-%d-%Y"))
    print('Yesterday: %s' % yesterday.strftime("%m-%d-%Y"))

    proper_open_date = get_datetime('1/29/24')

    print('Proper Open Date: %s' % proper_open_date.strftime("%m-%d-%y"))

    if week_ago <= proper_open_date.date() <= yesterday:
        print("TRUE")
    else:
        print("FALSE")



if __name__ == '__main__':
    test_1()