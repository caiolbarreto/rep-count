# streamlit_app.py
import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration, VideoTransformerBase
from pose_detection import pose_detection, exercises


class VideoTransformer(VideoTransformerBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        return pose_detection(exercises[0], img)


def main():
    if "page" not in st.session_state:
        st.session_state["page"] = "Home"

    st.title("Selecione um exercício")
    if st.session_state["page"] == "Home":
        exercicios_gifs = {
            "Desenvolvimento": "https://www.mundoboaforma.com.br/wp-content/uploads/2020/12/desenvolvimento-para-ombros-com-halteres.gif",
            "Rosca direta": "https://www.mundoboaforma.com.br/wp-content/uploads/2022/09/rosca-biceps-direta-com-halteres.gif",
            "Agachamento livre": "https://www.mundoboaforma.com.br/wp-content/uploads/2020/11/agachamento-livre-1.gif",
        }

        opcoes = ["Desenvolvimento", "Rosca direta", "Agachamento livre"]

        col1, col2 = st.columns(2)

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

        if option:
            if option == "Desenvolvimento":
                st.session_state["movimento"] = 0
            elif option == "Rosca direta":
                st.session_state["movimento"] = 1
            elif option == "Agachamento livre":
                st.session_state["movimento"] = 2

            button_clicked = st.button("Iniciar")

            if button_clicked:
                st.session_state["page"] = "Webcam"
                st.session_state["selected_exercise"] = option
                st.rerun()

    if st.session_state["page"] == "Webcam":
        st.title("Clique em iniciar para começar sua sessão")
        selected_exercise = st.session_state.get("selected_exercise")
        if selected_exercise:
            exercise_index = None
            if selected_exercise == "Desenvolvimento":
                exercise_index = 0
            elif selected_exercise == "Rosca direta":
                exercise_index = 1
            elif selected_exercise == "Agachamento livre":
                exercise_index = 2

            if exercise_index is not None:
                webrtc_streamer(
                    key="pose-detection",
                    video_processor_factory=VideoTransformer,
                    rtc_configuration=RTCConfiguration(
                        {"iceServers": [
                            {"urls": ["stun:stun.l.google.com:19302"]}]}
                    ),
                    media_stream_constraints={"video": True, "audio": False},
                )
        if st.button("Voltar ao menu"):
            st.session_state["page"] = "Home"
            st.rerun()


if __name__ == "__main__":
    main()
