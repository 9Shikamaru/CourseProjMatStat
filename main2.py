import algorithms as alg
import distribution3 as distr2
import file_functions as ff


INPUT_PATH  = "input/"
OUTPUT_PATH = "output/task2/"

# �������� ����� ������� ������ ������
TESTS_FILENAME = "tests_settings2.txt"

# �������� ����� �������� ������
TESTS_RESULT = "tests_result.txt"

# �������� ������ �������� ������ ����������/��������
HISTOGRAM = "histogram.png"
CHART     = "chart.png"

# ������� �������� ��� �������� �������������
HISTOGRAM_TITLE = "������� ��������� ������������� "
CHART_TITLE     = "������� ������������� "


# ������ ������ ��� ����������� ������
def read_tests_settings(filename):
    try:
        f = open(filename, "r")
    except IOError:
        print("���������� ������� ����: {0}".format(filename))
        ff.exit()
    # ����� ������������������
    n_list = [int(val) for val in f.readline().split()]
    # �������� �������� ��� ������ ������������
    correction_n = int(f.readline())
    # �������� ������������� �����
    sigm = float(f.readline())
    # ������� ����������
    alpha = float(f.readline())
    # �������� ����������
    precision = int(f.readline())
    histogram_run = ff.str_to_bool(f.readline().rstrip('\n'))
    chart_run = ff.str_to_bool(f.readline().rstrip('\n'))
    f.close()
    return n_list, correction_n, sigm, alpha, precision, histogram_run, chart_run


def main():
    # ������ ������ ������
    n_list, correction_n, sigm, alpha, precision, histogram_run, chart_run = read_tests_settings(INPUT_PATH + TESTS_FILENAME)
    # ������������� ���������� ��� ���������� ���������� �������������
    DISTR_COUNT    = 2
    DISTR_TITLE    = ["�����", "�����������"]
    DISTR_FILENAME = ["rayleigh", "norm"]
    EMPIRIC_DISTR  = [distr2.rayleigh_distribution, distr2.normal_distribution]
    THEOR_DISTR    = [distr2.rayleigh.cdf, distr2.norm.cdf]
    # �������������� �������� loc ��� ������������� �����
    ARGS_LIST      = [[0, sigm, correction_n], [correction_n]]
    ARGS_LABEL     = [["_", "sigm", "correction_n"], ["correction_n"]]
    for i in range(DISTR_COUNT):
        for j in range(len(n_list)):
            # ������������ ������������������
            sequence, modeling_time = alg.make_sequence(n_list[j], EMPIRIC_DISTR[i], *ARGS_LIST[i])
            # ������������ ����������
            intervals, intervals_width = alg.get_intervals(sequence)
            hits, v = alg.interval_hits(sequence, intervals)
            # ���� �������� ��-�������
            chi2_r, chi2_S, chi2_PSS, chi2_passed = alg.chi2_test(n_list[j], intervals, hits, alpha, THEOR_DISTR[i], *ARGS_LIST[i][:-1])
            # ���� �������� �������-������-�������
            cms_S, cms_PSS, cms_passed = alg.cms_test(sequence, alpha, THEOR_DISTR[i], *ARGS_LIST[i][:-1])
            ff.write_tests_results(OUTPUT_PATH + ff.get_filename(DISTR_FILENAME[i], TESTS_RESULT, n_list[j]), precision, 
                                   ARGS_LIST[i][1:], ARGS_LABEL[i][1:], alpha, sequence, intervals, hits, modeling_time,
                                   chi2_r, chi2_S, chi2_PSS, chi2_passed, cms_S, cms_PSS, cms_passed)
            if histogram_run:
                alg.make_histogram(OUTPUT_PATH + ff.get_filename(DISTR_FILENAME[i], HISTOGRAM, n_list[j]), 
                                   HISTOGRAM_TITLE + DISTR_TITLE[i], intervals, intervals_width, v, THEOR_DISTR[i], *ARGS_LIST[i][:-1])
        if chart_run:
            alg.make_chart(OUTPUT_PATH + ff.get_filename(DISTR_FILENAME[i], CHART), 
                           CHART_TITLE + DISTR_TITLE[i], THEOR_DISTR[i], *ARGS_LIST[i][:-1])


if __name__ == "__main__":
    main()