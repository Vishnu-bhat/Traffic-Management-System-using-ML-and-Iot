import cv2
from models.yolo_model import YOLOModel
from trackers.vehicle_tracker import Tracker
from utils.video_utils import draw_boxes, display_vehicle_count, count_vehicles, categorize_detections
from config.config import VIDEO_PATH, CLASS_FILE, CY1, OFFSET

def process_video(video_path, model, class_list, trackers, line_y, offset):
    cap = cv2.VideoCapture(video_path)
    vehicle_ids = {vtype: [] for vtype in trackers.keys()}

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (1020, 500))
        detections = model.predict(frame)
        detection_by_class = categorize_detections(detections, class_list)

        for vehicle_type, tracker in trackers.items():
            tracks = tracker.update(frame, detection_by_class[vehicle_type])
            draw_boxes(frame, tracks, label=vehicle_type)
            count_vehicles(vehicle_ids[vehicle_type], tracks, line_y, offset)

        display_vehicle_count(frame, {vtype: len(ids) for vtype, ids in vehicle_ids.items()})

        cv2.line(frame, (405, line_y), (580, line_y), (255, 255, 255), 2)
        cv2.imshow("Traffic Detection", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    # Load class list
    with open(CLASS_FILE, "r") as f:
        class_list = f.read().splitlines()

    # Initialize YOLO model
    model = YOLOModel(model_path='best.pt')

    # Define the trackers for each vehicle type
    trackers = {
        "bus": Tracker(),
        "car": Tracker(),
        "auto-rikshaw": Tracker(),
        "motorcycle": Tracker()
    }

    # Process video
    process_video(VIDEO_PATH, model, class_list, trackers, line_y=CY1, offset=OFFSET)

if __name__ == "__main__":
    main()
