import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
import cv2

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


class VideoProcessor:
    def recv(self, frame):
        frm = frame.to_ndarray(format="bgr24")

        faces = cascade.detectMultiScale(
            cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY), 1.1, 3)

        for x, y, w, h in faces:
            cv2.rectangle(frm, (x, y), (x+w, y+h), (0, 255, 0), 3)

        return av.VideoFrame.from_ndarray(frm, format='bgr24')


def main():
    if 'page' not in st.session_state:
        st.session_state['page'] = "Home"

    if st.session_state['page'] == "Home":
        st.title("Selecione um exercício")
        option = st.radio(
            "Opções", ["Desenvolvimento", "Rosca direta", "Agachamento livre"])

        # Track if the button has been clicked
        button_clicked = st.button("Iniciar")

        # Check if the button has been clicked and change page accordingly
        if button_clicked:
            st.session_state['page'] = "Webcam"
            st.rerun()

    if st.session_state['page'] == "Webcam":
        st.title("Clique em iniciar para começar a gravação")
        webrtc_streamer(key="key", video_processor_factory=VideoProcessor,
                        rtc_configuration=RTCConfiguration(
                            {"iceServers": [
                                {"urls": ["stun:stun.l.google.com:19302"]}]}
                        )
                        )
        if st.button("Voltar ao menu"):
            st.session_state['page'] = "Home"
            st.rerun()


if __name__ == "__main__":
    main()
