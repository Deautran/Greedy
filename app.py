from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = []
optimal = []

# Đổi giờ sang phút
def time_to_minutes(hhmm):
    h, m = map(int, hhmm.split(":"))
    return h*60 + m

# Truyền 2 danh sách tasks (tất cả công việc) và optimal (tạo lịch) ra giao diện.
@app.route("/")
def index():
    return render_template("index.html", tasks=tasks, optimal=optimal)

#Thêm công việc
@app.route("/add", methods=["POST"])
def add():
    date = request.form["date"]
    name = request.form["name"]
    # Nhập giờ + phút
    start_hour = int(request.form["start_hour"])
    start_minute = int(request.form["start_minute"])
    end_hour = int(request.form["end_hour"])
    end_minute = int(request.form["end_minute"])

    start = f"{start_hour:02d}:{start_minute:02d}"
    end = f"{end_hour:02d}:{end_minute:02d}"

    tasks.append({"date": date, "name": name, "start": start, "end": end})
    return redirect(url_for("index"))

# Xóa công việc
@app.route("/delete/<int:idx>")
def delete(idx):
    if 0 <= idx < len(tasks):
        tasks.pop(idx)
    return redirect(url_for("index"))

# Tạo lịch
@app.route("/optimize", methods=["POST"])
def optimize():
    global optimal
    optimal = []
    last_end_by_date = {}
    # Sắp xếp theo ngày, start tăng dần, nếu trùng start thì end tăng dần
    sorted_tasks = sorted(
        tasks,
        key=lambda x: (
            x["date"],
            time_to_minutes(x["start"]),
            time_to_minutes(x["end"])
        )
    )
    for t in sorted_tasks:
        date = t["date"]
        start_min = time_to_minutes(t["start"])
        last_end_min = time_to_minutes(last_end_by_date.get(date, "00:00"))
        # Chọn công việc nếu không trùng thời gian kết thúc
        if start_min >= last_end_min:
            optimal.append(t)
            last_end_by_date[date] = t["end"]
    return redirect(url_for("index"))

# Chạy chương trình
if __name__ == "__main__":
    app.run(debug=True)
