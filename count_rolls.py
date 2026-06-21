import cv2
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt
import torch

def count_rolls_final(image_path, model_path='best.pt'):
    # 1. لود مدل
    model = YOLO(model_path)
    
    # 2. اینفرنس
    results = model(image_path, verbose=False)
    boxes = results[0].boxes
    
    if boxes is None or len(boxes) == 0:
        print("⚠️ هیچ تشخیصی یافت نشد.")
        return 0

    # 3. استخراج باکس‌ها
    xyxy = boxes.xyxy.cpu().numpy()
    confs = boxes.conf.cpu().numpy()
    
    # --- 🔧 مرحله حیاتی: فیلتر کردن ---
    
    # الف) فیلتر کانفیدنس (حذف نویز)
    # از 0.1 به 0.45 ارتقا دادیم تا فقط رول‌های مطمئن شمرده شوند
    valid_idx = confs > 0.1
    xyxy = xyxy[valid_idx]
    confs = confs[valid_idx]

    # ب) فیلتر مساحت (حذف سوراخ وسط و کل کامیون)
    img_h, img_w = cv2.imread(image_path).shape[:2]
    total_area = img_h * img_w
    
    valid_boxes = []
    for box in xyxy:
        x1, y1, x2, y2 = box
        area = (x2 - x1) * (y2 - y1)
        
        # شرط مساحت: باکس باید بین 0.5% تا 5% کل تصویر باشد
        # (اعداد را بر اساس ابعاد عکس خود تنظیم کنید)
        if area > total_area * 0.005 and area < total_area * 0.05:
            valid_boxes.append(box)
            
    valid_boxes = np.array(valid_boxes)
    
    if len(valid_boxes) == 0:
        print("⚠️ باکس معتبری با مساحت مناسب یافت نشد.")
        return 0

    # 4. اعمال NMS (Non-Maximum Suppression) واقعی
    # این تابع باکس‌های تداخلی را حذف می‌کند
    # iou_threshold=0.3 یعنی اگر 30% تداخل داشتند، یکی را حذف کن
    if len(valid_boxes) > 0:
        # تبدیل به تنسور برای NMS
        boxes_tensor = torch.tensor(valid_boxes)
        nms_indices = torch.ops.torchvision.nms(boxes_tensor, torch.ones(len(valid_boxes)), iou_threshold=0.3)
        final_boxes = valid_boxes[nms_indices.numpy()]
    else:
        final_boxes = valid_boxes

    # 5. نمایش نتیجه
    output = cv2.imread(image_path).copy()
    for i, box in enumerate(final_boxes):
        x1, y1, x2, y2 = map(int, box)
        # رسم باکس نهایی
        cv2.rectangle(output, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(output, f"#{i+1}", (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    plt.figure(figsize=(15, 10))
    plt.imshow(cv2.cvtColor(output, cv2.COLOR_BGR2RGB))
    plt.title(f"✅ تعداد نهایی (دقیق): {len(final_boxes)}")
    plt.axis('off')
    plt.show()
    
    return len(final_boxes)

# --- اجرا ---
# توجه: مدل اختصاصی خودتان را جایگزین کنید
count = count_rolls_final("0005.jpg", model_path="models/YOLO26s-1920-150epoch.pt")
print(f"🔢 نتیجه نهایی: {count} رول")

