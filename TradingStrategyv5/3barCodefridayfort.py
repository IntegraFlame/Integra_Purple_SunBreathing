def ascii_bar_chart(data, width=50):
    max_val = max(data)
    min_val = min(data)
    for i, val in enumerate(data):
        bar_len = int((val / max_val) * width)
        bar = '█' * bar_len
        print(f"Wk {i+1:02d} | {bar} ${val:,.2f}")

weeks = list(df['Total_Equity'])
ascii_bar_chart(weeks)