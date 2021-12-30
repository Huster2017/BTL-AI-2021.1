# BTL-AI-2021.1
bài tập lớn môn trí tuệ nhân tạo

###############

Dự Án này gồm 3 phần chính:
1. Detect by yolo
2. Tracking object
3. Check speed

################

Trong phần 1, để có thể nhận dạng và phát hiện một phương tiện giao thông (cụ thể là 'car' trong dự án này). Tôi sử dụng mô hình YOLOv5 để có thể nhận dạng. Mô hình được tham khảo từ https://github.com/ultralytics/yolov5. Để có thể chạy thành công dự án, bạn nên tải các tệp mô hình, đào tạo từ https://github.com/ultralytics/yolov5.

Trong phần 2, để theo dõi 1 đối tượng cụ thể, chúng tôi sử dụng điểm tâm của đối tượng để tiến hành theo dõi. Khoảng cách giữa các điểm tâm qua mỗi khung hình của từng đối tượng sẽ là giá trị nhỏ nhất trong danh sách.

Trong phần 3, lợi dụng danh sách tracking có sẵn, ta có thể dễ dàng xác định vận tốc của đối tượng qua 2 đường môc cụ thể như hình dưới:
![image](https://user-images.githubusercontent.com/96712651/147739915-9e801620-176b-45db-91ec-2313aa3bb587.png)

