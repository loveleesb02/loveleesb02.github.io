import argparse
import csv
import sys
from pathlib import Path


def to_letter(avg):
    if avg >= 90:
        return "A"
    if avg >= 80:
        return "B"
    if avg >= 70:
        return "C"
    if avg >= 60:
        return "D"
    return "F"


def read_rows(path):
    # 엑셀 등에서 저장한 CSV는 UTF-8(BOM) 또는 CP949일 수 있으므로 순서대로 시도
    for encoding in ("utf-8-sig", "cp949"):
        try:
            with open(path, newline="", encoding=encoding) as f:
                return list(csv.reader(f, skipinitialspace=True))
        except UnicodeDecodeError:
            continue
    raise ValueError(f"{path} 파일의 인코딩을 읽을 수 없습니다.")


def save_subject_chart(subjects, averages, out_path):
    # --chart 없이 실행할 때는 matplotlib이 없어도 동작하도록 여기서 import
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["font.family"] = "Malgun Gothic"  # 한글 라벨이 네모로 깨지지 않도록

    fig, ax = plt.subplots()
    bars = ax.bar(subjects, averages)
    ax.bar_label(bars, fmt="%.1f")
    ax.set_ylim(0, 100)
    ax.set_title("과목별 평균")
    ax.set_ylabel("점수")
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main():
    # Windows에서 출력이 파이프/Git Bash로 갈 때 CP949로 인코딩되어 한글이 깨지는 것을 방지
    sys.stdout.reconfigure(encoding="utf-8")

    parser = argparse.ArgumentParser(description="학생별 평균과 학점을 출력합니다.")
    parser.add_argument("csv", nargs="?", type=Path, default=Path(__file__).with_name("grades.csv"))
    parser.add_argument("--chart", nargs="?", const="subject_averages.png", metavar="PATH",
                        help="과목별 평균 막대 그래프를 PNG로 저장 (기본: subject_averages.png)")
    args = parser.parse_args()

    rows = [row for row in read_rows(args.csv) if row]
    header, records = rows[0], rows[1:]
    subjects = header[1:]
    totals = [0.0] * len(subjects)

    print(f"{'이름':<6}" + "".join(f"{s:>6}" for s in subjects) + f"{'평균':>8}{'학점':>5}")
    for row in records:
        name, scores = row[0], [float(x) for x in row[1:]]
        avg = sum(scores) / len(scores)
        totals = [t + s for t, s in zip(totals, scores)]
        print(f"{name:<6}" + "".join(f"{s:>8.0f}" for s in scores) + f"{avg:>9.2f}{to_letter(avg):>5}")

    if args.chart:
        save_subject_chart(subjects, [t / len(records) for t in totals], args.chart)
        print(f"\n과목별 평균 그래프 저장: {args.chart}")


if __name__ == "__main__":
    main()
