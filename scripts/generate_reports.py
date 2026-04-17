import pandas as pd
import matplotlib.pyplot as plt
import os
import json
from datetime import datetime, timedelta

def get_project_report(project_name: str, mode: str = "daily"):
    file_path = f"assets/{project_name}/bug_tracking_db.xlsx"
    output_dir = f"assets/{project_name}/outputs"
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(file_path):
        return json.dumps({"error": f"Không tìm thấy file tracking lỗi cho {project_name}."})

    try:
        df = pd.read_excel(file_path)
        # Ép kiểu cột Date để so sánh
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Lấy ngày hiện tại
        now = datetime.now()
        today = pd.to_datetime(now.strftime("%Y-%m-%d"))
        today_str = now.strftime("%Y-%m-%d")
        
        if mode == "daily":
            df_filtered = df[df['Date'] == today]
            chart_title = f"Daily Bug Count per Module - {project_name.upper()} ({today_str})"
            # Đã thêm f-string để tự động gán ngày vào tên file chart
            chart_filename = f"daily_report_chart_{today_str}.png"
            
        elif mode == "weekly":
            # Tính thứ 2 và thứ 6 của tuần hiện tại (dựa theo Calendar)
            # Hàm weekday() trả về: 0 là Thứ 2, 6 là Chủ nhật
            monday = today - timedelta(days=today.weekday())
            friday = monday + timedelta(days=4)
            
            # Lọc dữ liệu từ Thứ 2 đến Thứ 6
            df_filtered = df[(df['Date'] >= monday) & (df['Date'] <= friday)]
            
            monday_str = monday.strftime("%Y-%m-%d")
            friday_str = friday.strftime("%Y-%m-%d")
            
            chart_title = f"Weekly Bug Count per Module - {project_name.upper()} ({monday_str} to {friday_str})"
            # Gắn luôn khoảng thời gian vào tên file weekly để quản lý dễ hơn
            chart_filename = f"weekly_report_chart_{monday_str}_to_{friday_str}.png"
            
        else:
            return json.dumps({"error": "Mode không hợp lệ (chỉ hỗ trợ daily/weekly)."})

        if df_filtered.empty:
            return json.dumps({"message": f"Không có bug nào được log trong thời gian này ({mode})."})

        # Đếm số lượng bug theo Module
        module_counts = df_filtered['Module'].value_counts()
        
        # Vẽ biểu đồ
        plt.figure(figsize=(10, 6))
        module_counts.plot(kind='bar', color='#4A90E2')
        plt.title(chart_title)
        plt.xlabel('Module')
        plt.ylabel('Number of Bugs')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        chart_path = f"{output_dir}/{chart_filename}"
        plt.savefig(chart_path)
        plt.close()

        # Tổng hợp dữ liệu trả về cho AI
        stats = {
            "total_bugs": len(df_filtered),
            "by_module": module_counts.to_dict(),
            "by_severity": df_filtered['Severity'].value_counts().to_dict(),
            "by_type": df_filtered['Type'].value_counts().to_dict(),
            "chart_path": chart_path
        }
        return json.dumps(stats, ensure_ascii=False)
        
    except Exception as e:
        return json.dumps({"error": f"Lỗi xử lý file Excel: {str(e)}"})