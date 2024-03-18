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

    st.title("Selecione um exercício")
    if st.session_state['page'] == "Home":
        exercicios_gifs = {
            "Desenvolvimento": "https://www.mundoboaforma.com.br/wp-content/uploads/2020/12/desenvolvimento-para-ombros-com-halteres.gif",
            "Rosca direta": "https://www.mundoboaforma.com.br/wp-content/uploads/2022/09/rosca-biceps-direta-com-halteres.gif",
            "Agachamento livre": "https://www.mundoboaforma.com.br/wp-content/uploads/2020/11/agachamento-livre-1.gif",
        }

        # Opções de exercícios
        opcoes = ["Desenvolvimento", "Rosca direta", "Agachamento livre"]

        # Coluna para exibir o GIF
        col1, col2 = st.columns(2)

        # Exibe o GIF do exercício selecionado
        with col1:
            option = st.radio(
                "Opções",
                opcoes,
                key="exercicio_selecionado",
            )

        with col2:
            if option:
                st.image(exercicios_gifs[option])
                st.write(f"Exercício selecionado: {option}")

        # Direcionamento para página específica do exercício
        if option:
            if option == "Desenvolvimento":
                st.session_state['movimento'] = "Desenvolvimento"
            elif option == "Rosca direta":
                st.session_state['movimento'] = "RoscaDireta"
            elif option == "Agachamento livre":
                st.session_state['movimento'] = "AgachamentoLivre"

            # Track if the button has been clicked
            button_clicked = st.button("Iniciar")

            # Check if the button has been clicked and change page accordingly
            if button_clicked:
                st.session_state['page'] = "Webcam"
                st.rerun()

    if st.session_state['page'] == "Webcam":
        st.title("Clique em iniciar para começar sua sessão")
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
