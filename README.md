# YouTube Shorts Performance Analysis — SCOPILE Intelligence V0.1

A Python and Pandas data analysis project built to understand performance patterns across **75 YouTube Shorts** from the SCOPILE VIRAL channel.

Rather than ranking videos only by views, this project cleans exported YouTube Analytics data, creates creator-focused performance metrics, compares duration ranges and publishing days, and produces simple recommendations from engagement and retention signals.

## Questions explored

- Which Shorts attracted the strongest engagement?
- Which videos converted viewers into subscribers most effectively?
- Which duration range performed best?
- Which publishing day produced the strongest engaged-view rate?
- Which successful patterns may be worth repeating?

## Dataset

The analysis was performed on a YouTube Analytics export from **SCOPILE VIRAL**. After cleaning and filtering, the working dataset contained **75 Shorts**.

The raw channel export is not included in this public repository. To run the project with your own export, place a compatible YouTube Analytics CSV named `Table data.csv` in the project root.

## Analysis workflow

The script:

1. Removes the YouTube Analytics `Total` row.
2. Separates Shorts from long-form videos using duration.
3. Renames and cleans columns and converts dates/durations to useful data types.
4. Creates custom metrics:
   - `engaged_view_rate`
   - `subscriber_conversion_rate`
   - `subscribers_per_1000_views`
   - `watch_time_per_view_seconds`
   - `duration_bucket`
   - `publish_weekday`
5. Ranks videos by views, engagement, retention, and subscriber conversion.
6. Groups Shorts by duration and publishing weekday.
7. Generates rule-based recommendations from engagement, retention, and subscriber-conversion signals.

## More reliable rate comparisons

Percentage metrics can look unusually strong when a video has very few views. To reduce this effect, rate-based video rankings only consider Shorts at or above the **75th percentile of views** in the dataset.

The views ranking still uses the full cleaned Shorts dataset.

For duration comparisons, a bucket must contain at least **5 Shorts** before it can qualify as the best duration range.

## Key findings from the development dataset

- **Top Short by Views:** 6,780
- **Best Qualified Engaged View Rate:** 52.19%
- **Best Average Percentage Viewed:** 133.03%
- **Best Subscriber Conversion Rate:** 0.17%
- **Best Duration Range:** 21–30 seconds
- **Best Publishing Day by Engaged View Rate:** Tuesday — 44.83%

These findings describe this specific SCOPILE VIRAL dataset. They are not intended as universal rules for YouTube Shorts.

## Project structure

```text
youtube-shorts-performance-analysis/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── README.md
├── outputs/
│   └── README.md
└── src/
    └── scopile_shorts_analysis.py
```

## Run the project

Install the dependencies:

```bash
pip install -r requirements.txt
```

Place a compatible YouTube Analytics export named `Table data.csv` in the project root, then run:

```bash
python src/scopile_shorts_analysis.py
```

The script prints the strongest-performing Shorts, best qualified duration range, best publishing day, and recommendations for top videos.

## Tools used

- Python
- Pandas
- NumPy

## Skills demonstrated

Data cleaning, data type conversion, feature engineering, Pandas filtering/grouping, aggregation, sorting and ranking, row-wise `apply`, threshold-based comparison, and translating performance metrics into practical creator recommendations.

## Limitation

The duration analysis requires at least five Shorts in a bucket before it can be called the best duration range. The weekday ranking currently does **not** apply an equivalent minimum-sample rule, so the publishing-day result should be interpreted with that limitation in mind.

## Author

**Rohith Biju**  
Data Science learner and creator behind SCOPILE VIRAL.

Built from my own creator analytics as a practical data-analysis project rather than a tutorial dataset.
