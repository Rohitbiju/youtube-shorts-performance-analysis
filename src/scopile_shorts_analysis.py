"""
YouTube Shorts Performance Analysis — SCOPILE Intelligence V0.1

Analyzes exported YouTube Analytics data for SCOPILE VIRAL Shorts.
Built by Rohith Biju.
"""

import pandas as pd
import numpy as np
df = pd.read_csv("Table data.csv")
df = df[df["Content"] != "Total"]
df["content_type"] = np.where(
    df["Duration"] < 90,
    "Short",
    "Long-form"
)
shorts_df = df[df["content_type"] == "Short"].copy()
shorts_df = shorts_df.rename(columns={
    "Content": "video_id",
    "Video title": "video_title",
    "Video publish time": "video_publish_time",
    "Duration": "duration",
    "Engaged views": "engaged_views",
    "Average percentage viewed (%)": "average_percentage_viewed",
    "Views": "views",
    "Watch time (hours)": "watch_time_hours",
    "Subscribers": "subscribers",
    "Estimated revenue (USD)": "estimated_revenue_usd",
    "Average view duration": "average_view_duration",
    "content_type": "content_type"
})
shorts_df = shorts_df.drop(columns=[
    "estimated_revenue_usd"
])
shorts_df["duration"] = shorts_df["duration"].astype(int)
shorts_df["video_publish_time"] = pd.to_datetime(
    shorts_df["video_publish_time"]
)
shorts_df=shorts_df[shorts_df["average_view_duration"].notnull()]
shorts_df["average_view_duration"] = (
    pd.to_timedelta(shorts_df["average_view_duration"])
    .dt.total_seconds()
    .astype(int)
)
shorts_df["engaged_view_rate"] = ((shorts_df["engaged_views"] / shorts_df["views"]) * 100).round(2)
shorts_df["subscriber_conversion_rate"] = ((shorts_df["subscribers"] / shorts_df["views"]) * 100).round(2)
# Subscribers gained per 1,000 views
shorts_df["subscribers_per_1000_views"] = (
    (shorts_df["subscribers"] / shorts_df["views"]) * 1000
).round(2)


# Watch time generated per view, converted from hours to seconds
shorts_df["watch_time_per_view_seconds"] = (
    (shorts_df["watch_time_hours"] * 3600) / shorts_df["views"]
).round(2)

# Group Shorts based on duration
shorts_df["duration_bucket"] = pd.cut(
    shorts_df["duration"],
    bins=[0, 10, 20, 30, 45, 60, 89],
    labels=[
        "0-10 sec",
        "11-20 sec",
        "21-30 sec",
        "31-45 sec",
        "46-60 sec",
        "61-89 sec"
    ],
    include_lowest=True
)
def get_recommendation(row):

    if (
        row["engaged_view_rate"] >= 45
        and row["average_percentage_viewed"] >= 100
    ):
        return "Strong hook + strong retention. Repeat this style."

    elif (
        row["engaged_view_rate"] >= 45
        and row["average_percentage_viewed"] >= 80
    ):
        return "Strong hook + good retention. Keep this structure and test similar topics."

    elif (
        row["engaged_view_rate"] >= 45
        and row["average_percentage_viewed"] < 80
    ):
        return "Strong initial interest, but retention is weak. Improve pacing/content."

    elif (
        row["engaged_view_rate"] < 40
        and row["average_percentage_viewed"] >= 100
    ):
        return "Weak initial pull, but viewers who stay watch well. Improve opening/hook."

    elif row["subscriber_conversion_rate"] >= 0.05:
        return "Strong subscriber conversion. Study why this Short attracts followers."

    else:
        return "Average performance. Test stronger hook, topic, or format."
shorts_df["recommendation"] = shorts_df.apply(
    get_recommendation,
    axis=1
) 

# Get publishing weekday from publish date
shorts_df["publish_weekday"] = (
    shorts_df["video_publish_time"].dt.day_name()
)
# Top views uses the full cleaned Shorts dataset.
top_views = shorts_df.sort_values(
    by="views",
    ascending=False
).head(10)

# Require enough evidence before a Short can be called "best" for rate-based metrics.
# The threshold adapts to the dataset: only Shorts at or above the 75th percentile of views qualify.
min_views = shorts_df["views"].quantile(0.75)

qualified_shorts = shorts_df[
    shorts_df["views"] >= min_views
].copy()

top_engagement = qualified_shorts.sort_values(
    by="engaged_view_rate",
    ascending=False
).head(10)

top_retention = qualified_shorts.sort_values(
    by="average_percentage_viewed",
    ascending=False
).head(10)

top_subscriber_conversion = qualified_shorts.sort_values(
    by="subscriber_conversion_rate",
    ascending=False
).head(10)

duration_analysis = shorts_df.groupby(
    "duration_bucket",
    observed=True
).agg(
    total_views=("views", "sum"),
    total_engaged_views=("engaged_views", "sum"),
    total_subscribers=("subscribers", "sum"),
    average_percentage_viewed=("average_percentage_viewed", "mean"),
    shorts_count=("video_id", "count")
)

duration_analysis["engaged_view_rate"] = (
    duration_analysis["total_engaged_views"]
    / duration_analysis["total_views"]
    * 100
).round(2)

duration_analysis["subscriber_conversion_rate"] = (
    duration_analysis["total_subscribers"]
    / duration_analysis["total_views"]
    * 100
).round(2)

duration_analysis["average_percentage_viewed"] = (
    duration_analysis["average_percentage_viewed"].round(2)
)

# Only duration buckets with at least 5 Shorts can qualify as the "best" duration range.
qualified_duration = duration_analysis[
    duration_analysis["shorts_count"] >= 5
].copy()

weekday_analysis = shorts_df.groupby("publish_weekday").agg(
    total_views=("views", "sum"),
    total_engaged_views=("engaged_views", "sum"),
    total_subscribers=("subscribers", "sum"),
    average_percentage_viewed=("average_percentage_viewed", "mean"),
    shorts_count=("video_id", "count")
)

weekday_analysis["engaged_view_rate"] = (
    weekday_analysis["total_engaged_views"]
    / weekday_analysis["total_views"]
    * 100
).round(2)

weekday_analysis["subscriber_conversion_rate"] = (
    weekday_analysis["total_subscribers"]
    / weekday_analysis["total_views"]
    * 100
).round(2)

weekday_analysis["average_percentage_viewed"] = (
    weekday_analysis["average_percentage_viewed"].round(2)
)

   

print("\n" + "=" * 60)
print("CREATOR ANALYTICS INTELLIGENCE V0.1")
print("=" * 60)
print("YouTube Shorts Performance Analyzer")
print("Tested on SCOPILE VIRAL")
print("Built by Rohith Biju")

print(f"\nTOTAL SHORTS ANALYZED: {len(shorts_df)}")
print(f"MINIMUM VIEWS FOR RATE-BASED RANKINGS: {int(min_views)}")

best_views = top_views.iloc[0]
best_engagement = top_engagement.iloc[0]
best_retention = top_retention.iloc[0]
best_subscriber = top_subscriber_conversion.iloc[0]

print("\nTOP SHORT BY VIEWS")
print(f"Title: {best_views['video_title']}")
print(f"Views: {best_views['views']}")
print(f"Engaged View Rate: {best_views['engaged_view_rate']}%")

print("\nBEST ENGAGEMENT")
print(f"Title: {best_engagement['video_title']}")
print(f"Engaged View Rate: {best_engagement['engaged_view_rate']}%")
print(f"Views: {best_engagement['views']}")

print("\nBEST RETENTION")
print(f"Title: {best_retention['video_title']}")
print(
    f"Average Percentage Viewed: "
    f"{best_retention['average_percentage_viewed']}%"
)

print("\nBEST SUBSCRIBER CONVERSION")
print(f"Title: {best_subscriber['video_title']}")
print(
    f"Subscriber Conversion Rate: "
    f"{best_subscriber['subscriber_conversion_rate']}%"
)
best_duration = qualified_duration.sort_values(
    by="engaged_view_rate",
    ascending=False
).iloc[0]

best_weekday = weekday_analysis.sort_values(
    by="engaged_view_rate",
    ascending=False
).iloc[0]

print("\nBEST DURATION RANGE")
print(f"Duration: {best_duration.name}")
print(f"Engaged View Rate: {best_duration['engaged_view_rate']}%")
print(f"Shorts Count: {int(best_duration['shorts_count'])}")

print("\nBEST POSTING DAY")
print(f"Day: {best_weekday.name}")
print(f"Engaged View Rate: {best_weekday['engaged_view_rate']}%")
print(f"Shorts Count: {int(best_weekday['shorts_count'])}")
print("\nTOP 5 SHORTS + RECOMMENDATIONS")

for _, row in top_views.head(5).iterrows():
    print("\n" + "-" * 40)
    print(f"Title: {row['video_title']}")
    print(f"Views: {row['views']}")
    print(f"Engaged View Rate: {row['engaged_view_rate']}%")
    print(
        f"Average Percentage Viewed: "
        f"{row['average_percentage_viewed']}%"
    )
    print(
        f"Subscriber Conversion Rate: "
        f"{row['subscriber_conversion_rate']}%"
    )
    print(f"Recommendation: {row['recommendation']}")
