import face_recognition
import cv2
import numpy as np
import os
import time



class VideoCamera:
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        if self.video_capture is None or not self.video_capture.isOpened():
            print('Warning: unable to open video source: ')

    def __del__(self):
        self.video_capture.release()
        cv2.destroyAllWindows()


    def face_checking(self,username, id):
        start = time.time()
        base_path = os.getcwd()
        db_image = face_recognition.load_image_file(f"{base_path}\\static\\images\\Attendance_database\\{username}_{id}\\{username}.jpg")
        db_face_encoding = face_recognition.face_encodings(db_image)[0]
        detected = False
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        known_face_encodings = [
            db_face_encoding,
        ]
        known_face_names = [
            username,
        ]
        process_this_frame = True
        while True:
            end = time.time()
            time_diff = int(end - start)
            # Grab a single frame of video
            ret, frame = self.video_capture.read()
            # Resize frame of video to 1/4 size for faster face recognition processing
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            # Only process every other frame of video to save time
            if process_this_frame:
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"
                    # If a match was found in known_face_encodings, just use the first one.
                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]
                        detected = True
                    face_names.append(name)
            process_this_frame = not process_this_frame
            # Display the results
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # Draw a box around the face
                edge_color = (255, 64, 92) if detected else (25, 182, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), edge_color, 2)
                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), edge_color, cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                ## time left
                cv2.putText(frame, str(time_diff)+' s', (20, 30), font, 1.0, (255, 255, 255), 1)
            cv2.imshow('Video', frame)
            if detected and time_diff>3:
                time.sleep(1)
                self.__del__()
                return detected
            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def cam_stream(self, name=None):
        name = "Nouveau user detecter"
        while True:
            # Grab a single frame of video
            ret, frame = self.video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            for (top, right, bottom, left) in face_locations:
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 64, 92), 2)
                # Draw a label with a name below the face
                # cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            # ret, jpeg = cv2.imencode('.jpg', frame)
            # return jpeg.tobytes()
            # Display the resulting image
            cv2.imshow('Video', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def shoot(self,username,id):
        # create the folder if not exists
        time_diff = 0
        start = time.time()

        name = "Nouveau user detecter"
        while True:
            end = time.time()
            time_diff = int(end - start)

            ret, frame = self.video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = face_recognition.face_locations(rgb_small_frame)
            font = cv2.FONT_HERSHEY_DUPLEX
            phrase = f'you have 20 seconds to register : {str(time_diff)}'
            cv2.putText(frame,phrase, (20, 30), font, 0.7, (255, 255, 255), 1)
            for (top, right, bottom, left) in face_locations:
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 64, 92), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (25, 182, 255), 1)
            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            if time_diff > 3 and face_locations != []:
                print('shooting')
                image_path = f"{os.getcwd()}\static\images\Attendance_database\{username}_{id}"

                if not os.path.isdir(image_path):
                    os.mkdir(image_path)

                image_path = f"{os.getcwd()}\static\images\Attendance_database\{username}_{id}\{username}.jpg"
                image_path = image_path.replace("\\","\\\\")
                return_value, image = self.video_capture.read()
                cv2.imwrite(image_path, image)
                if os.path.exists(image_path):
                    time.sleep(3)
                    self.__del__()
                    return True
                else:
                    time.sleep(3)
                    self.__del__()
                    return False
            if time_diff > 20:
                self.__del__()
                return False
            # if face_locations != []:
            #     phrase = 'be ready'
            #     cv2.putText(frame,phrase, (20, 15), font, 0.7, (255, 255, 255), 1)


                
                    
