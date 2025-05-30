// mediapipe/modules/holistic_landmark/calculators/roi_tracking_calculator.cc

// Add error handling for invalid rectangles
bool RectRequirementsSatisfied(const NormalizedRect& prev_rect,
                             const NormalizedRect& curr_rect,
                             const std::pair<int, int>& image_size,
                             float max_rotation_degrees,
                             float max_translation,
                             float max_scale) {
  if (!prev_rect.has_x_center() || !prev_rect.has_y_center() ||
      !curr_rect.has_x_center() || !curr_rect.has_y_center()) {
    return false;
  }
  // Rest of implementation...
}

// gesture_calculator.py

import mediapipe as mp
import cv2
import numpy as np

class GestureCalculator:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
    def process_frame(self, frame):
        # Convert to RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame
        results = self.hands.process(frame_rgb)
        
        # Handle gesture detection
        if results.multi_hand_landmarks:
            return self.analyze_gestures(results.multi_hand_landmarks)
            
        return None

// mediapipe/tasks/cc/vision/holistic_landmarker/holistic_face_tracking.cc

Stream<NormalizedRect> TrackFaceRoi(
    Stream<NormalizedLandmarkList> prev_landmarks,
    Stream<NormalizedRect> roi,
    Stream<std::pair<int, int>> image_size,
    Graph& graph) {
    
    // Add robust error handling
    auto& tracking_node = graph.AddNode("RoiTrackingCalculator");
    auto& tracking_node_opts = 
        tracking_node.GetOptions<RoiTrackingCalculatorOptions>();
        
    // Improve tracking parameters
    auto* rect_requirements = tracking_node_opts.mutable_rect_requirements();
    rect_requirements->set_rotation_degrees(15.0);  // Reduced from 40.0
    rect_requirements->set_translation(0.15);       // Adjusted for stability
    rect_requirements->set_scale(0.3);             // More conservative scaling
    
    // Add validation
    if (!prev_landmarks || !roi || !image_size) {
        return nullptr;
    }
    
    return tracking_node.Out("TRACKING_RECT").Cast<NormalizedRect>();
}