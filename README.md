# **Mô hình lớp học ảo**
## Yêu cầu hệ điều hành Ubuntu và ngôn ngữ lập trình Python<br>
![A test](../main/model.png)
## Hướng dẫn chạy
**Bước 1:** Cài đặt **v4l2loopback** (hướng dẫn cài đặt và sử dụng [v4l2loopback](https://github.com/umlaeute/v4l2loopback))<br>

**Bước 2:** Cài đặt **backgroud blur function** (hướng dẫn cài đặt và sử dụng [Linux-Fake-Background-Webcam](https://github.com/fangfufu/Linux-Fake-Background-Webcam))<br>

**Bước 3:** Cài đặt [face_lib](https://github.com/a-akram-98/face_lib?ref=pythonawesome.com) và các thư viện liên quan khác trong phần khai báo thư viện trong face_detection.py và fake recognition.py.<br>

**Bước 4:** Tạo các host camera ảo trên thiết bị bằng câu lệnh<br>

```sudo modprobe v4l2loopback video_nr=2,3,4,5 card_label="backgroud-blur","face-detect","recogition","backup"```

*Mặc định trên ubuntu sẽ có 1 host là /dev/video0 là kênh để webcam trả dữ liệu cho máy. Câu lệnh này sẽ tạo ra các host camera ảo bằng v4l2loopback (/dev/video2, /dev/video3, ...).*<br>

**Bước 5:** Tạo luồng stream qua các NFV.<br>
*Chú ý:*
* Thay đổi nguồn của video đến tại: ```vid = cv2.VideoCapture(source_video)```
* Thay đổi đích của luồng stream tại: ```cam = pyfakewebcam.FakeWebcam('host_camera',int(width), int(height))``` với host_camera='/dev/video*'
* Khi sử dụng chức năng backgroud cần setup đúng độ phân giải của video ```python3 fake.py --webcam-path "source_host" --no-foreground --no-background --width width_value --height height_value --fps fps_number```<br>
 *Ví dụ:* ```python3 fake.py --webcam-path "/dev/video3" --no-foreground --no-background --width 856 --height 480 --fps 60```<br>
 **Host camera đích mặc định của background blur là '/dev/video2' còn các function khác cần phải setup**<br>
 
 **Bước 6:** Cuối cùng thử tạo một luồng stream tới 1 máy khác bằng ffmpeg với đầu vào là host của function cuối cùng trong chuỗi.
 
 
